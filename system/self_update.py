# -*- coding: utf-8 -*-

import logging
import os


import version


log = logging.getLogger(__name__)


class SelfUpdate(object):
    def __init__(self):
        self._statefile = Statefile()
        self._sequence_number_file = SequenceNumberFile()

    def downloaded(self, filepath, sequence_number):
        log.info('downloaded update file %s', filepath)
        self._statefile.write(filepath)
        self._sequence_number_file.write(sequence_number)

    def verify(self):
        import remotecontrol.protocoldispatcher as proto  # to fix AttributeError: 'module' object has no attribute
        if self._statefile.is_processing():
            log.info('update successfully finished')
            self._statefile.remove()
            seq = self._sequence_number_file.read()
            proto.ProtocolDispatcher().send('ack_ok', sequence=seq, message='software update successfully finished, current version {}'.format(version.VERSION))
            self._sequence_number_file.remove()
        elif self._statefile.is_failed():
            log.error('failed to update software, previous version was restored')
            self._statefile.remove()
            seq = self._sequence_number_file.read()
            proto.ProtocolDispatcher().send('ack_fail', sequence=seq, message='failed to update software, previous version {} was restored'.format(version.VERSION))
            self._sequence_number_file.remove()


class CustomFile(object):
    def __init__(self, path):
        self._path = path

    def read(self):
        try:
            with open(self._path, 'r') as f:
                return f.read().strip()
        except:
            return None

    def write(self, data):
        with open(self._path, 'w') as f:
            f.write(data)

    def remove(self):
        if os.path.exists(self._path):
            os.remove(self._path)


class SequenceNumberFile(CustomFile):
    def __init__(self):
        super().__init__(os.path.join(os.getcwd(), 'rmpd_update_sequence_number'))

    def read(self):
        return int(super().read())


class Statefile(CustomFile):
    def __init__(self):
        super().__init__(os.path.join(os.getcwd(), 'rmpd_update_statefile'))

    def is_processing(self):
        return self.read() == '-PROCESSING-'

    def is_failed(self):
        return self.read() == '-ROLLBACK-'






