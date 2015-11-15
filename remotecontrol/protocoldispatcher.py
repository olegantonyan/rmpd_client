# -*- coding: utf-8 -*-

import traceback
import logging

import remotecontrol.controlwrapper
import utils.singleton
import utils.config
import remotecontrol.protocol.receiver
import remotecontrol.protocol.sender

log = logging.getLogger(__name__)


class ProtocolDispatcher(object, metaclass=utils.singleton.Singleton):
    def __init__(self):
        self._control_wrapper = remotecontrol.controlwrapper.ControlWrapper(utils.config.Config().server_url(),
                                                                            utils.config.Config().login(),
                                                                            utils.config.Config().password(),
                                                                            self.onmessage)
        self.send('power_on')

    def onmessage(self, msg, seq):
        try:
            remotecontrol.protocol.receiver.Receiver(self._control_wrapper, msg, seq).call()
        except Exception as e:
            log.error("error processing message '{m}': {e}\n{t}".format(m=str(msg), e=str(e), t=traceback.format_exc()))

    def send(self, command_type, **kwargs):
        return remotecontrol.protocol.sender.Sender(self._control_wrapper, command_type).call(**kwargs)

