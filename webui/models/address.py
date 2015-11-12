#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netifaces import interfaces, ifaddresses, AF_INET  # @UnresolvedImport
from socket import inet_aton, error
from logging import getLogger

log = getLogger(__name__)

import webui.models.debinterface.constants  # @UnusedImport
import webui.models.debinterface.interfaces
import hardware
import system.systeminfo

if 'debian' not in system.systeminfo.linux_disto():
    webui.models.debinterface.constants.INTERFACES = '/home/flysnake/Desktop/interfaces'
    webui.models.debinterface.constants.BACKUP = '/home/flysnake/Desktop/interfaces.old'


class Address(object):
    def __init__(self, iface):
        self.__iface = iface
        self.__all_ifaces = webui.models.debinterface.interfaces.interfaces()
        self.__iface_actual = self.__get_ifaces_actual().get(self.__iface, None)
        self.__iface_config = self.__get_ifaces_config().get(self.__iface, None)
        self.__error = ''
        self.__iface_config_changed = False

    @staticmethod
    def iface_name_webui():
        return hardware.platfrom.get_webui_interface()

    @staticmethod
    def iface_name_main():
        return hardware.platfrom.get_main_interface()

    def addr_configured(self):
        return self.__iface_config

    def addr_actual(self):
        return self.__iface_actual

    def addr_summary(self):
        if self.__iface_actual:
            if self.__iface_actual.get('addr', None):
                return self.__iface_actual.get('addr', 'none') + " (" + (self.__iface_config.get('source', 'unknown') if self.__iface_config else 'not configured') + ")"

    def set_addr(self, addr):
        if self.__iface_config != addr:
            self.__iface_config = addr
            self.__iface_config_changed = True

    def save(self):
        if not self.__iface_config:
            self.__error = "Not configured address"
            return False
        if not self.__iface_config_changed:
            return True
            self._error = "Not changed"
        try:
            for i in self.__all_ifaces.adapters:
                if self.__iface == i.ifAttributes.get('name', ''):
                    if self.__iface_config['source'] not in ['dhcp', 'static']:
                        self.__error = "Invalid address source"
                        return False
                    i.ifAttributes['source'] = self.__iface_config['source']
                    if not i.ifAttributes['source'] == 'dhcp':
                        if self.__validate_ip(self.__iface_config['addr']):
                            i.ifAttributes['address'] = self.__iface_config['addr']
                        else:
                            self.__error = "No static IP address specified"
                            return False
                        if self.__validate_ip(self.__iface_config['netmask']):
                            i.ifAttributes['netmask'] = self.__iface_config['netmask']
                        else:
                            self.__error = "No netmask specified"
                            return False
                        if self.__validate_ip(self.__iface_config['gateway']):
                            i.ifAttributes['gateway'] = self.__iface_config['gateway']
                        else:
                            self.__error = "No gateway specified"
                            return False
                        if len(self.__iface_config['nameservers']) > 0 and len(self.__iface_config['nameservers'][0]) > 0:
                            i.ifAttributes['dns-nameservers'] = ' '.join(self.__iface_config['nameservers'])
                        else:
                            i.ifAttributes['dns-nameservers'] = i.ifAttributes['gateway']
            self.__all_ifaces.writeInterfaces()
            log.warning("new network configuration written")
            return True
        except Exception as e:
            self.__error = "Error saving IP addr: " + str(e)
            log.exception("error saving ip addr")
            return False

    def error(self):
        return self.__error

    def __get_ifaces_config(self):
        res = {}
        for i in self.__all_ifaces.adapters:
            if i.ifAttributes.get('name', None) is not None:
                res[i.ifAttributes.get('name', None)] = {'source': i.ifAttributes.get('source', ''),
                                                         'addr': i.ifAttributes.get('address', ''),
                                                         'netmask': i.ifAttributes.get('netmask', ''),
                                                         'gateway': i.ifAttributes.get('gateway', ''),
                                                         'nameservers': i.ifAttributes.get('dns-nameservers', '').split(' ')
                                                         }
        return res

    def __get_ifaces_actual(self):
        res = {}
        for iface_name in interfaces():
            addr = ifaddresses(iface_name)[AF_INET][0]['addr']
            netmask = ifaddresses(iface_name)[AF_INET][0]['netmask']
            res[iface_name] = {'addr': addr, 'netmask': netmask}
        return res

    def __validate_ip(self, ip):
        try:
            inet_aton(ip)
            return True
        except error:
            return False
