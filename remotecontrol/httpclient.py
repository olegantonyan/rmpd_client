# -*- coding: utf-8 -*-

import logging
import urllib
import requests
import requests.auth
import requests.packages.urllib3
import tempfile
import shutil

import system.systeminfo as systeminfo

log = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)


class HttpClient(object):
    def __init__(self, server_url, login, password, onreceive_callback):
        self._api_url = urllib.parse.urljoin(server_url, '/deviceapi/status')
        self._login = login
        self._password = password
        self._onreceive = onreceive_callback

    def send(self, msg, seq):
        json, seq = self._post_request(msg, seq)
        if json is not None and len(json) > 0:
            self._onreceive(json, seq)

    def _post_request(self, jsondata, sequence_number=0):
        r = requests.post(self._api_url,
                          json=jsondata,
                          auth=requests.auth.HTTPBasicAuth(self._login, self._password),
                          timeout=20,
                          headers={'X-Sequence-Number': str(sequence_number), 'User-Agent': systeminfo.user_agent()})
        if r.status_code != 200:
            raise RuntimeError("error sending data, status code: {s}".format(s=r.status_code))
        return r.json(), r.headers['X-Sequence-Number']


def download_file(url, localpath):
    r = requests.get(url,
                     stream=True,
                     timeout=60,
                     headers={"User-Agent": systeminfo.user_agent()})
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # delete is not required since we are moving it afterward
    for chunk in r.iter_content(chunk_size=2048):
        if chunk:  # filter out keep-alive new chunks
            temp_file.write(chunk)
            temp_file.flush()
    shutil.move(temp_file.name, localpath)
