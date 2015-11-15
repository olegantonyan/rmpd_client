# -*- coding: utf-8 -*-

from logging import getLogger, WARNING
from urllib import parse
from requests import post, get
from requests.auth import HTTPBasicAuth
from tempfile import NamedTemporaryFile
from shutil import move
from os import path
import requests.packages.urllib3

import system.systeminfo

log = getLogger(__name__)
getLogger("requests").setLevel(WARNING)
requests.packages.urllib3.disable_warnings()  # for self-signed certificate


def self_signed_certificate():
    return path.join(path.dirname(__file__), 'server.slon-ds.ru.crt')


class HttpClient(object):
    def __init__(self, server_url, login, password, onreceive_callback):
        self._api_url = parse.urljoin(server_url, '/deviceapi/status')
        self._login = login
        self._password = password
        self._onreceive = onreceive_callback

    def send(self, msg, seq):
        json, seq = self._post_request(msg, seq)
        if json is not None and len(json) > 0:
            self._onreceive(json, seq)

    def _post_request(self, jsondata, sequence_number=0):
        r = post(self._api_url,
                 json=jsondata,
                 auth=HTTPBasicAuth(self._login, self._password),
                 timeout=20,
                 headers={'X-Sequence-Number': str(sequence_number), 'User-Agent': system.systeminfo.user_agent()},
                 verify=self_signed_certificate()
                 )
        if r.status_code != 200:
            raise RuntimeError("error sending data, status code: {s}".format(s=r.status_code))
        return r.json(), r.headers['X-Sequence-Number']


def download_file(url, localpath):
    r = get(url,
            stream=True,
            timeout=60,
            headers={"User-Agent": system.systeminfo.user_agent()},
            verify=self_signed_certificate())
    temp_file = NamedTemporaryFile(delete=False)  # delete is not required since we are moving it afterward
    for chunk in r.iter_content(chunk_size=2048):
        if chunk:  # filter out keep-alive new chunks
            temp_file.write(chunk)
            temp_file.flush()
    move(temp_file.name, localpath)
