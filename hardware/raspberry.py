#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit

import hardware
import utils.shell
import utils.threads


class PlatformRaspberry(hardware.Platform):
    @property
    def __name__(self):
        return "raspberry"
    
    def __init__(self):
        hardware.Platform.__init__(self)
        self.__network_pin = 22
        self.__player_pin = 21
        try:
            r, o, e = utils.shell.execute("gpio -v")
            if r != 0:
                exit("WiringPI gpio does not work properly: 'gpio -v' result: {r}, stdout: {o}, stderr: {e}\nPlease, install it http://wiringpi.com\nTerminated".format(r=r, o=o, e=e))
        except OSError:
            exit("No wiringPI gpio utility \nPlease, install it http://wiringpi.com\nTerminated")
        self.__setup_pins([self.__network_pin, self.__player_pin])
        self.__blink_network = False
        self.__init_timer_once = False
    
    def get_webui_interface(self):
        return 'eth0:0'
    
    def get_main_interface(self):
        return 'eth0'
    
    def restart_networking(self):
        hardware.log.warning("restarting network")
        (r,o,e) = utils.shell.execute("sudo /etc/init.d/networking restart")
        if r != 0:
            hardware.log.error("error restarting network: " + o.decode('utf-8') + ", " + e.decode('utf-8'))
            return False
        return True
    
    def set_network_led(self, state):
        hardware.log.debug("Raspberry Pi platform, network: {s}".format(s=state))
        self.__write_pin(self.__network_pin, 1 if state else 0)
    
    def set_player_led(self, state):
        hardware.log.debug("Raspberry Pi platform, player: {s}".format(s=state))
        self.__write_pin(self.__player_pin, 1 if state else 0)
        
    def set_all_leds_disabled(self):
        hardware.log.debug("Raspberry Pi platform, disable all leds")
        self.__write_pin(self.__player_pin, 0)
        self.__write_pin(self.__network_pin, 0)
    
    def set_network_blink_led(self, state):
        hardware.log.debug("Raspberry Pi platform, network blink: {s}".format(s=state))
        self.__blink_network = state
        if not self.__init_timer_once:
            self.__blink_network_pin()
            self.__init_timer_once = True
            
    def __blink_network_pin(self):
        if self.__blink_network:
            if self.__read_pin(self.__network_pin) == 1:
                self.__write_pin(self.__network_pin, 0)
            else:
                self.__write_pin(self.__network_pin, 1)
        utils.threads.run_after_timeout(0.4, self.__blink_network_pin)
                    
    def __setup_pins(self, pins):
        for i in pins:
            utils.shell.execute("gpio export {pin} out".format(pin=i))
            
    def __write_pin(self, pin, state):
        utils.shell.execute("gpio -g write {pin} {st}".format(pin=pin, st=state))
        
    def __read_pin(self, pin):
        (r, o, e) = utils.shell.execute("gpio -g read {pin}".format(pin=pin))  # @UnusedVariable
        return int(o)