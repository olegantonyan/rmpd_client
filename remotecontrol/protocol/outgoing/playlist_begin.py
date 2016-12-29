# -*- coding: utf-8 -*-

import remotecontrol.protocol.outgoing.base_command as base_command
import utils.support as support


class PlaylistBegin(base_command.BaseCommand):
    def call(self, **kwargs):
        files = kwargs.get('files') or []
        self._message = support.join_list_excerpt(files, 20, ', ')
        return super().call()
