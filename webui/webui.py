# -*- coding: utf-8 -*-

from bottle import template, run, get, post, auth_basic, abort, request, static_file, TEMPLATE_PATH, redirect
import os
import logging

import webui.models.status
import webui.models.password
import webui.models.address
import webui.models.system

log = logging.getLogger(__name__)


@get('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views", "static"))


def check_pass(username, password):
    ok = webui.models.password.Password.authenticate(username, password)
    if ok:
        log.info("accepted user '" + username + "'")
    else:
        log.warning("refused user '" + username + "'")
    return ok


def global_variables():
    return {'rmpd_login': webui.models.status.Status.login(),
            'rmpd_version': webui.models.status.Status.version()}


def home_variables():
    return {'g': global_variables()}


def status_variables():
    addr_static = webui.models.address.Address(webui.models.address.Address.iface_name_static())
    addr_eth = webui.models.address.Address(webui.models.address.Address.iface_name_ethernet())
    addr_wifi = webui.models.address.Address(webui.models.address.Address.iface_name_wifi())
    return {'g': global_variables(),
            'online': webui.models.status.Status.online(),
            'now_playing': webui.models.status.Status.current_track_name(),
            'static_ip': addr_static.addr_summary(),
            'ethernet_ip': addr_eth.addr_summary(),
            'wifi_ip': addr_wifi.addr_summary()}


def settings_variables():
    eth = webui.models.address.Address(webui.models.address.Address.iface_name_ethernet())
    eth_dhcp = True if eth.addr_configured().get('source', '') == 'dhcp' else False
    if eth_dhcp:
        eth_f = eth.addr_actual
    else:
        eth_f = eth.addr_configured
    result = {'g': global_variables()}
    result['ethernet_addr_form_values'] = {
        'dhcp': eth_dhcp,
        'addr': eth_f().get('addr', '') or '',
        'netmask': eth_f().get('netmask', '') or '',
        'gateway': eth.addr_configured().get('gateway', '') or '',
        'nameservers': ', '.join(eth.addr_configured().get('nameservers', []))
    }

    wifi = webui.models.address.Address(webui.models.address.Address.iface_name_wifi())
    wifi_dhcp = True if wifi.addr_configured().get('source', '') == 'dhcp' else False
    if wifi_dhcp:
        wifi_f = wifi.addr_actual
    else:
        wifi_f = wifi.addr_configured
    result['wifi_addr_form_values'] = {
        'dhcp': wifi_dhcp,
        'addr': wifi_f().get('addr', '') or '',
        'netmask': wifi_f().get('netmask', '') or '',
        'gateway': wifi.addr_configured().get('gateway', '') or '',
        'nameservers': ', '.join(wifi.addr_configured().get('nameservers', [])),
        'psk': wifi.addr_configured().get('psk', '') or '',
        'ssid': wifi.addr_configured().get('ssid', '') or ''
    }
    return result


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


@post("/settings/change_ethernet_address")
@auth_basic(check_pass, "default: admin/admin")
def change_ethernet_address_form_handler():
    model = webui.models.address.Address(webui.models.address.Address.iface_name_ethernet())
    use_dhcp = request.forms.get('use_dhcp')
    if use_dhcp:
        model.set_addr({'source': 'dhcp'})
    else:
        model.set_addr({'source': 'static',
                        'addr': request.forms.get('addr'),
                        'netmask': request.forms.get('netmask'),
                        'gateway': request.forms.get('gateway'),
                        'nameservers': request.forms.get('nameservers').split(',')})
    if model.save():
        webui.models.system.System().restart_network()
        redirect("/settings")
    abort(403, model.error())


@post("/settings/change_wifi_address")
@auth_basic(check_pass, "default: admin/admin")
def change_wifi_address_form_handler():
    model = webui.models.address.Address(webui.models.address.Address.iface_name_wifi())
    use_dhcp = request.forms.get('use_dhcp')
    addr = {}
    if use_dhcp:
        addr['source'] = 'dhcp'
    else:
        addr['source'] = 'static'
        addr['addr'] = request.forms.get('addr')
        addr['netmask'] = request.forms.get('netmask')
        addr['gateway'] = request.forms.get('gateway')
        addr['nameservers'] = request.forms.get('nameservers').split(',')

    addr['ssid'] = request.forms.get('ssid')
    addr['psk'] = request.forms.get('psk')
    model.set_addr(addr)
    if model.save():
        webui.models.system.System().restart_network()
        redirect("/settings")
    abort(403, model.error())


@post("/reboot")
@auth_basic(check_pass, "default: admin/admin")
def reboot():
    webui.models.system.System().reboot()
    redirect("/")


def start(host, port):
    log.debug("starting on {h}:{p}".format(h=host, p=port))
    TEMPLATE_PATH.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"))
    run(host=host, port=port, debug=False, reloader=False)
