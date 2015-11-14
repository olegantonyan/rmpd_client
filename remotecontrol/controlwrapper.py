#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger
from traceback import format_exc
from json import loads, dumps  # @UnresolvedImport
from os import path, getcwd

log = getLogger(__name__)

import remotecontrol.httpclient
import remotecontrol.messagequeue
import utils.threads
import system.status


class ControlWrapper(object):
    '''
    Implements wrapper for remote control
    '''

    def __init__(self, server_url, login, password, receive_protocol_callback):
        self.__proto = remotecontrol.httpclient.HttpClient(server_url, login, password, self.onreceive)
        self.__receive_protocol_callback = receive_protocol_callback
        self.__queue = remotecontrol.messagequeue.MessageQueue(path.join(getcwd(), "message_queue.db3"))
        self.__check_queue()

    def send(self, msg, queued=False, seq=0):
        log.debug("sending message ({q}): '{s}'".format(s=str(msg), q=("queued" if queued else "immed")))
        if queued:
            data = {"msg": msg,
                    "seq": seq}
            self.__queue.enqueue(dumps(data))
            return True
        else:
            try:
                self.__proto.send(msg, seq)
                self.__set_online_status(True)
                return True
            except:
                log.error("error sending message: '{s}'".format(s=str(msg)))
                log.debug(format_exc())
                self.__set_online_status(False)
                return False

    def onreceive(self, msg, seq):
        log.debug("received message: '%s'", str(msg))
        utils.threads.run_in_thread(target=self.__receive_protocol_callback, args=(msg, seq), daemon=True)

    def __check_queue(self):
        messageid, data = self.__queue.dequeue()
        if data is not None and messageid is not None and len(data) > 0:
            parsed_data = loads(data)
            if self.send(parsed_data["msg"], False, parsed_data["seq"]):
                self.__queue.remove(messageid)

        utils.threads.run_after_timeout(0.2, self.__check_queue)

    def __set_online_status(self, status):
        system.status.Status().online = status
