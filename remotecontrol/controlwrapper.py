# -*- coding: utf-8 -*-

import logging
import traceback
import json

import remotecontrol.httpclient
import remotecontrol.messagequeue
import utils.threads
import system.status

log = logging.getLogger(__name__)


class ControlWrapper(object):
    def __init__(self, server_url, login, password, receive_protocol_callback):
        self._proto = remotecontrol.httpclient.HttpClient(server_url, login, password, self.onreceive)
        self._receive_protocol_callback = receive_protocol_callback
        self._queue = remotecontrol.messagequeue.MessageQueue()
        self._check_queue()

    def send(self, msg, queued=False, seq=0):
        log.debug("sending message ({q}): '{s}'".format(s=str(msg), q=("queued" if queued else "immed")))
        if queued:
            data = {'msg': msg, 'seq': seq}
            self._queue.enqueue(json.dumps(data))
            return True
        else:
            # XXX possible thread-safety problem here
            try:
                self._proto.send(msg, seq)
                self._set_online_status(True)
                return True
            except:
                log.error("error sending message: '{s}'".format(s=str(msg)))
                log.debug(traceback.format_exc())
                self._set_online_status(False)
                return False

    def onreceive(self, msg, seq):
        log.debug("received message: '%s'", str(msg))
        utils.threads.run_in_thread(target=self._receive_protocol_callback, args=(msg, seq), daemon=True)

    def _check_queue(self):
        messageid, data = self._queue.dequeue()
        if data is not None and messageid is not None and len(data) > 0:
            parsed_data = json.loads(data)
            if self.send(parsed_data["msg"], False, parsed_data["seq"]):
                self._queue.remove(messageid)

        utils.threads.run_after_timeout(0.2, self._check_queue)

    def _set_online_status(self, status):
        system.status.Status().online = status
