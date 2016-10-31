# -*- coding: utf-8 -*-

import tarfile
import logging
import os

import utils.datetime as datetime
import utils.config as config
import remotecontrol.httpclient as httpclient
import utils.files as files
import system.rw_fs as rw_fs

log = logging.getLogger(__name__)


class ServiceUpload(object):
    def __init__(self, reason):
        self._reason = reason

    def call(self):
        log.info('starting service upload')
        filepath = self._arvive(self._logs_directory())
        if not os.path.exists(filepath):
            raise RuntimeError('error creating archive')
        try:
            if not self._upload(filepath):
                raise RuntimeError('error uploading archive')
        finally:
            os.remove(filepath)

    def _timestamp(self):
        return datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    def _generate_destination_filepath(self):
        return '/tmp/service_upload_python_' + self._timestamp()

    def _arvive(self, directory):
        with rw_fs.Storage():
            dst = self._generate_destination_filepath() + '.tar.gz'
            with tarfile.open(dst, mode='w:gz') as archive:
                archive.add(directory)
            return dst

    def _upload(self, filepath):
        data = {'reason': self._reason}
        fils = {'file': open(filepath, 'rb')}
        login = config.Config().login()
        password = config.Config().password()
        return httpclient.submit_multipart_form(files.full_url_by_relative('/deviceapi/service_upload'), data, fils, login, password)

    def _logs_directory(self):
        return os.path.dirname(config.Config().logfile())

