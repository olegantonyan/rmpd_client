# -*- coding: utf-8 -*-

import logging
import threading

import remotecontrol.protocol.incoming.base_command as base_command
import system.service_upload as service_upload

log = logging.getLogger(__name__)


class RequestServiceUpload(base_command.BaseCommand):
    def call(self):
        return WorkerThread(onfinished_callback=self._onfinished, sequence=self._sequence).start()

    def _onfinished(self, ok, seq):
        self._ack(ok, 'service upload', seq)


class WorkerThread(threading.Thread):
    def __init__(self, onfinished_callback, sequence):
        super().__init__()
        self._sequence = sequence
        self._onfinished_callback = onfinished_callback
        self.daemon = True

    def run(self):
        ok = True
        try:
            service_upload.ServiceUpload().call()
        except:
            log.exception('error running service upload')
            ok = False
        finally:
            self._onfinished_callback(ok, self._sequence)