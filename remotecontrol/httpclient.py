#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger, WARNING
from urllib import parse
from requests import post, get
from requests.auth import HTTPBasicAuth
from tempfile import NamedTemporaryFile
from shutil import move
from os import path

log = getLogger(__name__)
getLogger("requests").setLevel(WARNING)
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings() # for self-signed certificate

import system.systeminfo

class HttpClient(object):
    '''
    Implement HTTP(S) protocol
    '''

    def __init__(self, server_url, login, password, onreceive_callback):
        self.__api_url = parse.urljoin(server_url, "/deviceapi/status")
        self.__login = login
        self.__password = password
        self.__onreceive = onreceive_callback
        
    def send(self, msg, seq):
        json, seq = self.__post_request(msg, seq)
        if json is not None and len(json) > 0:
            self.__onreceive(json, seq)
    
    def __post_request(self, jsondata, sequence_number=0):
        r = post(self.__api_url, 
                 json=jsondata, 
                 auth=HTTPBasicAuth(self.__login, self.__password), 
                 timeout=20, 
                 headers={"X-Sequence-Number": str(sequence_number), "User-Agent": system.systeminfo.user_agent()}
                 )
        if r.status_code != 200:
            raise RuntimeError("error sending data, status code: {s}".format(s=r.status_code))
        return r.json(), r.headers["X-Sequence-Number"]
    
def download_file(url, localpath):
    r = get(url, stream=True, timeout=60, headers={"User-Agent": system.systeminfo.user_agent()})
    temp_file = NamedTemporaryFile()
    for chunk in r.iter_content(chunk_size=2048): 
        if chunk: # filter out keep-alive new chunks
            temp_file.write(chunk)
            temp_file.flush()
    move(temp_file.name, localpath)


        