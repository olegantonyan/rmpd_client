#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from codecs import open

import utils.singleton
import utils.crypto

KP1 = ('mplayer_executable' * 2)[0:-4]
KP2 = ('mediafiles_path'*3)[0:-13]


class Config(object, metaclass=utils.singleton.Singleton):
    '''
    Handles configuration data
    '''

    def __init__(self, filename):
        self.__filename = filename
        self.__parser = ConfigParser()
        with open(self.__filename, 'r', encoding='utf-8') as f:
            self.__parser.read_file(f)
        
        self.__enc1 = utils.crypto.AESCipher(KP1)
        self.__enc2 = utils.crypto.AESCipher(KP2)
        
        section = 'remote_control'
        self.__server_url = self.__parser.get(section, 'server_url')
        self.__login = self.__parser.get(section, 'login')
        try:
            self.__password = self.__enc1.decrypt_text(self.__parser.get(section, 'password'))
        except:
            self.__password = ""
            
        section = 'logging'
        self.__logfile = self.__parser.get(section, 'logfile')
        self.__verbose = self.__parser.get(section, 'verbose')
        
        section = 'player'
        self.__mediafiles_path = self.__parser.get(section, 'mediafiles_path')
        self.__mplayer_executable = self.__parser.get(section, 'mplayer_executable')
        self.__omplayer_executable = self.__parser.get(section, 'omxplayer_executable')
        self.__omplayer_arguments = self.__parser.get(section, 'omxplayer_arguments')
        
        section = 'webui'
        try:
            self.__webui_password = self.__enc2.decrypt_text(self.__parser.get(section, 'password'))
        except:
            self.__webui_password = ""
            
    def __save_value(self, section, option, value):
        self.__parser.set(section, option, str(value))
        with open(self.__filename, 'w', encoding='utf-8') as f:
            self.__parser.write(f)
           
    def server_url(self):
        return self.__server_url
       
    def login(self):
        return self.__login
      
    def password(self):
        return self.__password
    
    def set_password(self, value): 
        self.__save_value('remote_control', 'password', self.__enc1.encrypt_text(value))
        self.__password = value
        
    def logfile(self):
        return self.__logfile
    
    def mediafiles_path(self):
        return self.__mediafiles_path
    
    def mplayer_executable(self):
        return self.__mplayer_executable
    
    def omplayer_executable(self):
        return self.__omplayer_executable
    
    def omplayer_arguments(self):
        return self.__omplayer_arguments
    
    def verbose_logging(self):
        return self.__verbose == "yes" or self.__verbose == "y" or self.__verbose == "true"
    
    def webui_password(self):
        return self.__webui_password
    
    def set_webui_password(self, value):
        self.__save_value('webui', 'password', self.__enc2.encrypt_text(value))
        self.__webui_password = value
