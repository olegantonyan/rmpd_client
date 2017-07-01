# -*- coding: utf-8 -*-

import platform
import logging

log = logging.getLogger(__name__)


class Platform(object):
    @property
    def __name__(self):
        return "stub"

    def initialize(self):
        pass
    
    def set_network_led(self, state):
        print("stub platform, network: {s}".format(s=state))
    
    def set_player_led(self, state):
        print("stub platform, player: {s}".format(s=state))
        
    def set_all_leds_disabled(self):
        print("stub platform, disable all")
        
    def set_network_blink_led(self, state):
        print("stub platform, network blink: {s}".format(s=state))
        
    def get_static_interface(self):
        return "(stub static iface)"
    
    def get_ethernet_interface(self):
        return "(stub ethernet iface)"

    def get_wifi_interface(self):
        return "(stub wifi iface)"
    
    def restart_networking(self):
        print("restart network stub")

    def fix_file_permissions(self, path):
        print("stub fix_file_permissions " + path)
    
platfrom = Platform()
    
for i in ["i386", "i486", "i586", "i686", "x86", "x86-64", "x86_64", "x64"]:
    if i in platform.machine():
        import hardware.pc
        platfrom = hardware.pc.PlatformPc()
        break
    
for i in ["arm"]:
    if i in platform.machine():
        import hardware.raspberry
        platfrom = hardware.raspberry.PlatformRaspberry()
        break
