#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bottle import template, run, get, post, auth_basic, abort, request, static_file, TEMPLATE_PATH, redirect
from os import path
from logging import getLogger

log = getLogger(__name__)

import webui.models.status
import webui.models.password
import webui.models.address
import webui.models.system

@get('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root=path.join(path.dirname(path.abspath(__file__)), "views", "static"))

def check_pass(username, password):
    ok = webui.models.password.Password.authenticate(username, password)
    if ok:
        log.info("accepted user '" + username + "'")
    else:
        log.warning("refused user '" + username + "'")
    return ok
    
def global_variables():
    return {'rmpd_login': webui.models.status.Status.login(),
            'rmpd_version': webui.models.status.Status.version() }
    
def home_variables():
    return {'g': global_variables()}

def status_variables():
    addr_webui = webui.models.address.Address(webui.models.address.Address.iface_name_webui())
    addr_main = webui.models.address.Address(webui.models.address.Address.iface_name_main())
    return {'g': global_variables(),
            'online': webui.models.status.Status.online(),
            'now_playing': webui.models.status.Status.current_track_name(),
            'webui_ip': addr_webui.addr_summary(),
            'main_ip': addr_main.addr_summary() }
    
def settings_variables():
    a = webui.models.address.Address(webui.models.address.Address.iface_name_main())
    dhcp = True if a.addr_configured().get('source', '') == 'dhcp' else False
    if dhcp:
        f = a.addr_actual
    else:
        f = a.addr_configured
    return {'g': global_variables(),
            'addr_form_values': {'dhcp': dhcp, 
                                 'addr': f().get('addr', ''), 
                                 'netmask': f().get('netmask', ''), 
                                 'gateway': f().get('gateway', ''), 
                                 'nameservers': ', '.join(f().get('nameservers', [])) 
                                 } 
            }

@get("/")
@auth_basic(check_pass, "default: admin/admin")
def home():
    return template("home.html", home_variables())

@get("/settings")
@auth_basic(check_pass, "default: admin/admin")
def settings():
    return template("settings.html", settings_variables())

@get("/status")
@auth_basic(check_pass, "default: admin/admin")
def status():
    return template("status.html", status_variables())

@post("/settings/change_password")
@auth_basic(check_pass, "default: admin/admin")
def change_password_form_handler():
    current_password = request.forms.get('current_password')
    new_password = request.forms.get('new_password')
    pw = webui.models.password.Password(current_password, new_password)
    if pw.save():
        redirect("/settings")
    abort(403, pw.errors())
    
@post("/settings/change_address")
@auth_basic(check_pass, "default: admin/admin")
def change_address_form_handler():
    addr_main = webui.models.address.Address(webui.models.address.Address.iface_name_main())
    use_dhcp = request.forms.get('use_dhcp')
    if use_dhcp:
        addr_main.set_addr({'source': 'dhcp'})
    else:
        addr_main.set_addr({'source': 'static', 
                            'addr': request.forms.get('addr'), 
                            'netmask': request.forms.get('netmask'), 
                            'gateway': request.forms.get('gateway'),
                            'nameservers': request.forms.get('nameservers').split(',')})
    if addr_main.save():
        webui.models.system.System().restart_network()
        redirect("/settings")
    abort(403, addr_main.error())
    
@post("/reboot")
@auth_basic(check_pass, "default: admin/admin")
def reboot():
    webui.models.system.System().reboot()
    redirect("/")

def start(host, port):
    log.debug("starting on {h}:{p}".format(h=host, p=port))
    TEMPLATE_PATH.append(path.join(path.dirname(path.abspath(__file__)), "views"))
    run(host=host, port=port, debug=False, reloader=False)
    