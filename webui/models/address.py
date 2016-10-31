# -*- coding: utf-8 -*-

import netifaces
import socket
import logging

import webui.models.debinterface.constants
import webui.models.debinterface.interfaces
import hardware
import system.systeminfo
import system.control
import system.rw_fs as rw_fs

log = logging.getLogger(__name__)


if 'debian' not in system.systeminfo.linux_disto():
    webui.models.debinterface.constants.INTERFACES = '/home/oleg/Desktop/interfaces'
    webui.models.debinterface.constants.BACKUP = '/home/oleg/Desktop/interfaces.old'


class Address(object):
    def __init__(self, iface):
        self._iface = iface
        self._all_ifaces = webui.models.debinterface.interfaces.interfaces()
        self._iface_actual = self._get_ifaces_actual().get(self._iface, None)
        self._iface_config = self._get_ifaces_config().get(self._iface, None)
        self._error = ''
        self._iface_config_changed = False

    @staticmethod
    def iface_name_webui():
        return hardware.platfrom.get_webui_interface()

    @staticmethod
    def iface_name_main():
        return hardware.platfrom.get_main_interface()

    def addr_configured(self):
        return self._iface_config

    def addr_actual(self):
        return self._iface_actual

    def addr_summary(self):
        if self._iface_actual:
            if self._iface_actual.get('addr', None):
                return self._iface_actual.get('addr', 'none') + " (" + (self._iface_config.get('source', 'unknown') if self._iface_config else 'not configured') + ")"

    def set_addr(self, addr):
        if self._iface_config != addr:
            self._iface_config = addr
            self._iface_config_changed = True

    def save(self):
        if not self._iface_config:
            self._error = "Not configured address"
            return False
        if not self._iface_config_changed:
            self._error = "Not changed"
            return True
        with rw_fs.Root():
            try:
                for i in self._all_ifaces.adapters:
                    if self._iface == i.ifAttributes.get('name', ''):
                        if self._iface_config['source'] not in ['dhcp', 'static']:
                            self._error = "Invalid address source"
                            return False
                        i.ifAttributes['source'] = self._iface_config['source']
                        if not i.ifAttributes['source'] == 'dhcp':
                            if self._validate_ip(self._iface_config['addr']):
                                i.ifAttributes['address'] = self._iface_config['addr']
                            else:
                                self._error = "No static IP address specified"
                                return False
                            if self._validate_ip(self._iface_config['netmask']):
                                i.ifAttributes['netmask'] = self._iface_config['netmask']
                            else:
                                self._error = "No netmask specified"
                                return False
                            if self._validate_ip(self._iface_config['gateway']):
                                i.ifAttributes['gateway'] = self._iface_config['gateway']
                            else:
                                self._error = "No gateway specified"
                                return False
                            if len(self._iface_config['nameservers']) > 0 and len(self._iface_config['nameservers'][0]) > 0:
                                i.ifAttributes['dns-nameservers'] = ' '.join(self._iface_config['nameservers'])
                            else:
                                i.ifAttributes['dns-nameservers'] = i.ifAttributes['gateway']
                self._all_ifaces.writeInterfaces()
                log.warning("new network configuration written")
                return True
            except Exception as e:
                self._error = "Error saving IP addr: " + str(e)
                log.exception("error saving ip addr")
                return False

    def error(self):
        return self._error

    def _get_ifaces_config(self):
        res = {}
        for i in self._all_ifaces.adapters:
            if i.ifAttributes.get('name', None) is not None:
                res[i.ifAttributes.get('name', None)] = {'source': i.ifAttributes.get('source', ''),
                                                         'addr': i.ifAttributes.get('address', ''),
                                                         'netmask': i.ifAttributes.get('netmask', ''),
                                                         'gateway': i.ifAttributes.get('gateway', ''),
                                                         'nameservers': i.ifAttributes.get('dns-nameservers', '').split(' ')
                                                         }
        return res

    def _get_ifaces_actual(self):
        res = {}
        for iface_name in netifaces.interfaces():
            addr = netifaces.ifaddresses(iface_name)[netifaces.AF_INET][0]['addr']
            netmask = netifaces.ifaddresses(iface_name)[netifaces.AF_INET][0]['netmask']
            res[iface_name] = {'addr': addr, 'netmask': netmask}
        return res

    def _validate_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
