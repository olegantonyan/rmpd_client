# -*- coding: utf-8 -*-

import zipfile
import logging
import os

import utils.datetime as datetime
import utils.config as config

log = logging.getLogger(__name__)


class ServiceUpload(object):
    def call(self):
        log.info('starting service upload')
        filepath = self._arvive(self._logs_directory())
        if not os.path.exists(filepath):
            raise RuntimeError('error creating archive')

    def _timestamp(self):
        return datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    def _generate_destination_filepath(self):
        return '/tmp/service_upload_python_' + self._timestamp()

    def _arvive(self, directory):
        dst = self._generate_destination_filepath()
        archive = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
        self._zip_directory(directory, os.path.basename(os.path.normpath(directory)), archive)
        archive.close()
        return dst

    def _zip_directory(self, path, relname, archive):
        paths = os.listdir(path)
        for p in paths:
            p1 = os.path.join(path, p)
            p2 = os.path.join(relname, p)
            if os.path.isdir(p1):
                self._zip_directory(p1, p2, archive)
            else:
                archive.write(p1, p2)

    def _logs_directory(self):
        return os.path.dirname(config.Config().logfile())

    def _upload(self, filepath):
        pass
