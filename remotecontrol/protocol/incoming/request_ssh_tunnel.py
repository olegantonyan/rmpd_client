# -*- coding: utf-8 -*-

import logging

import remotecontrol.protocol.incoming.base_command as base_command
import utils.shell as shell

log = logging.getLogger(__name__)


class RequestSshTunnel(base_command.BaseCommand):
    def call(self):
        cli = "ssh -R {ext_port}:localhost:{int_port} {user}@{server} -p {server_port} -f sleep {dur}"\
            .format(ext_port=self._data['external_port'],
                    int_port=self._data['internal_port'],
                    user=self._data['username'],
                    server=self._data['server'],
                    server_port=self._data['server_port'],
                    dur=self._data['duration'])
        m = "opening ssh tunnel: '{cli}'".format(cli=cli)
        log.info(m)
        self._sender('ack_ok').call(sequence=self._sequence, message=m)
        r, o, e = shell.execute(cli)
        # self._sender('ack').call(ok=(r == 0), sequence=self._sequence, message=(m + ";" + str(o) + ";" + str(e)))
        log.info("ssh tunnel result: {r}, stdout: {o}, stderr: {e}".format(r=r, o=o, e=e))

