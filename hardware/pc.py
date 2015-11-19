# -*- coding: utf-8 -*-

import hardware


class PlatformPc(hardware.Platform):
    @property
    def __name__(self):
        return "pc"
    
    def get_webui_interface(self):
        return 'eth0'
    
    def get_main_interface(self):
        return 'eth0'

    def set_network_led(self, state):
        hardware.log.debug("PC platform, network: {s}".format(s=state))
    
    def set_player_led(self, state):
        hardware.log.debug("PC platform, player: {s}".format(s=state))
        
    def set_all_leds_disabled(self):
        hardware.log.debug("PC platform, disable all leds")
        
    def set_network_blink_led(self, state):
        hardware.log.debug("PC platform, network blink: {s}".format(s=state))
        
    def restart_networking(self):
        hardware.log.debug("PC platform, restart networking")  