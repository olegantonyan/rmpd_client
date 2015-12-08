# -*- coding: utf-8 -*-

import logging
import os

import utils.singleton
import utils.threads

log = logging.getLogger(__name__)


class Watcher(object, metaclass=utils.singleton.Singleton):
    def __init__(self):
        pass

    def onfinished(self):
        pass
