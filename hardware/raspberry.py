# -*- coding: utf-8 -*-

import sys

import hardware
import utils.shell
import utils.threads
import utils.files as files
import system.control as control


class PlatformRaspberry(hardware.Platform):
    @property
    def __name__(self):
        return "raspberry"

    def __init__(self):
        super().__init__()
        self._network_pin = 22
        self._player_pin = 21
        self._blink_network = False
        self._init_timer_once = False

    def initialize(self):
        try:
            r, o, e = utils.shell.execute("gpio -v")
            if r != 0:
                sys.exit(
                    "WiringPI gpio does not work properly: 'gpio -v' result: {r}, stdout: {o}, stderr: {e}\nPlease, install it http://wiringpi.com\nTerminated".format(
                        r=r, o=o, e=e))
        except OSError:
            sys.exit("No wiringPI gpio utility \nPlease, install it http://wiringpi.com\nTerminated")
        self._setup_pins([self._network_pin, self._player_pin])
        self.fix_file_permissions('/tmp')
        control.Control().set_system_time_from_hwclock()
    
    def get_webui_interface(self):
        return 'eth0:0'
    
    def get_main_interface(self):
        return 'eth0'
    
    def restart_networking(self):
        hardware.log.warning("restarting network")
        (r, o, e) = utils.shell.execute("sudo /etc/init.d/networking restart")
        if r != 0:
            hardware.log.error("error restarting network: " + o + ", " + e)
            return False
        return True
    
    def set_network_led(self, state):
        hardware.log.debug("Raspberry Pi platform, network: {s}".format(s=state))
        self._write_pin(self._network_pin, 1 if state else 0)
    
    def set_player_led(self, state):
        hardware.log.debug("Raspberry Pi platform, player: {s}".format(s=state))
        self._write_pin(self._player_pin, 1 if state else 0)
        
    def set_all_leds_disabled(self):
        hardware.log.debug("Raspberry Pi platform, disable all leds")
        self._write_pin(self._player_pin, 0)
        self._write_pin(self._network_pin, 0)
    
    def set_network_blink_led(self, state):
        hardware.log.debug("Raspberry Pi platform, network blink: {s}".format(s=state))
        self._blink_network = state
        if not self._init_timer_once:
            self._blink_network_pin()
            self._init_timer_once = True
            
    def _blink_network_pin(self):
        if self._blink_network:
            if self._read_pin(self._network_pin) == 1:
                self._write_pin(self._network_pin, 0)
            else:
                self._write_pin(self._network_pin, 1)
        utils.threads.run_after_timeout(0.4, self._blink_network_pin)
                    
    def _setup_pins(self, pins):
        for i in pins:
            utils.shell.execute("gpio export {pin} out".format(pin=i))
            
    def _write_pin(self, pin, state):
        utils.shell.execute("gpio -g write {pin} {st}".format(pin=pin, st=state))
        
    def _read_pin(self, pin):
        (r, o, e) = utils.shell.execute("gpio -g read {pin}".format(pin=pin))
        return int(o)

    def fix_file_permissions(self, path):
        files.chown_to_current(path)
        files.chmod(path, '777')  # can't solve this on OS level
