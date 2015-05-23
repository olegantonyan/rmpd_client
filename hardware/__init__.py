#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from platform import machine
from logging import getLogger

log = getLogger(__name__)

class Platform(object):
    @property
    def __name__(self):
        return "stub"
    
    def set_network_led(self, state):
        print("stub platform, network: {s}".format(s=state))
    
    def set_player_led(self, state):
        print("stub platform, player: {s}".format(s=state))
        
    def set_all_leds_disabled(self):
        print("stub platform, disable all")
        
    def set_network_blink_led(self, state):
        print("stub platform, network blink: {s}".format(s=state))
        
    def get_webui_interface(self):
        return "(stub webui iface)"
    
    def get_main_interface(self):
        return "(stub main iface)"
    
    def restart_networking(self):
        print("restart network stub")
    
platfrom = Platform()
    
for i in ["i386", "i486", "i586", "i686", "x86", "x86-64", "x86_64", "x64"]:
    if i in machine():
        import hardware.pc  # @UnresolvedImport
        platfrom = hardware.pc.PlatformPc()
        break
    
for i in ["arm"]:
    if i in machine():
        import hardware.raspberry  # @UnresolvedImport
        platfrom = hardware.raspberry.PlatformRaspberry()  # @UndefinedVariable
        break