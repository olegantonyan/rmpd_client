# -*- coding: utf-8 -*-

import logging
import traceback
import json

import remotecontrol.httpclient as httpclient
import remotecontrol.messagequeue as messagequeue
import utils.threads as threads
import system.status as status

log = logging.getLogger(__name__)


class ControlWrapper(object):
    def __init__(self, server_url, login, password, receive_protocol_callback):
        self._reset_log_errors_count()
        self._proto = httpclient.HttpClient(server_url, login, password, self.onreceive)
        self._receive_protocol_callback = receive_protocol_callback
        self._queue = messagequeue.MessageQueue()
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
                self._reset_log_errors_count()
                return True
            except:
                self._log_error(msg)
                log.debug(traceback.format_exc())
                self._set_online_status(False)
                return False

    def onreceive(self, msg, seq):
        log.debug("received message: '%s'", str(msg))
        threads.run_in_thread(target=self._receive_protocol_callback, args=(msg, seq))

    def _check_queue(self):
        messageid, data = self._queue.dequeue()
        if data is not None and messageid is not None and len(data) > 0:
            parsed_data = json.loads(data)
            if self.send(parsed_data["msg"], False, parsed_data["seq"]):
                self._queue.remove(messageid)

        threads.run_after_timeout(0.01, self._check_queue)

    def _set_online_status(self, stat):
        status.Status().online = stat

    def _log_error(self, msg):
        if self._log_errors_count >= 5:  # optimize log write operations when offline
            return
        log.error("error sending message: '{s}'".format(s=str(msg)))
        self._log_errors_count += 1
        if self._log_errors_count >= 5:
            log.warn("subsequent send errors omitted until appearing online")

    def _reset_log_errors_count(self):
        self._log_errors_count = 0
