# -*- coding: utf-8 -*-

import traceback
import logging

import remotecontrol.controlwrapper as controlwrapper
import utils.singleton as singleton
import utils.config as config
import remotecontrol.protocol.receiver as receiver
import remotecontrol.protocol.sender as sender

log = logging.getLogger(__name__)


class ProtocolDispatcher(object, metaclass=singleton.Singleton):
    def __init__(self):
        self._control_wrapper = controlwrapper.ControlWrapper(config.Config().server_url(),
                                                              config.Config().login(),
                                                              config.Config().password(),
                                                              self.onmessage)
        self.send('power_on')

    def onmessage(self, msg, seq):
        try:
            receiver.Receiver(self._control_wrapper, msg, seq).call()
        except Exception as e:
            log.error("error processing message '{m}': {e}\n{t}".format(m=str(msg), e=str(e), t=traceback.format_exc()))

    def send(self, command_type, **kwargs):
        return sender.Sender(self._control_wrapper, command_type).call(**kwargs)

