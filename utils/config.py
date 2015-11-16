# -*- coding: utf-8 -*-

import configparser
import codecs

import utils.singleton
import utils.crypto

KP1 = ('mplayer_executable' * 2)[0:-4]
KP2 = ('mediafiles_path'*3)[0:-13]


class Config(object, metaclass=utils.singleton.Singleton):
    def __init__(self, filename):
        self._filename = filename
        self._parser = configparser.ConfigParser()
        with codecs.open(self._filename, 'r', encoding='utf-8') as f:
            self._parser.read_file(f)
        
        self._enc1 = utils.crypto.AESCipher(KP1)
        self._enc2 = utils.crypto.AESCipher(KP2)
        
        section = 'remote_control'
        self._server_url = self._parser.get(section, 'server_url')
        self._login = self._parser.get(section, 'login')
        try:
            self._password = self._enc1.decrypt_text(self._parser.get(section, 'password'))
        except:
            self._password = ""
            
        section = 'logging'
        self._logfile = self._parser.get(section, 'logfile')
        self._verbose = self._parser.get(section, 'verbose')
        
        section = 'player'
        self._mediafiles_path = self._parser.get(section, 'mediafiles_path')
        self._mplayer_executable = self._parser.get(section, 'mplayer_executable')
        self._omplayer_executable = self._parser.get(section, 'omxplayer_executable')
        self._omplayer_arguments = self._parser.get(section, 'omxplayer_arguments')
        
        section = 'webui'
        try:
            self._webui_password = self._enc2.decrypt_text(self._parser.get(section, 'password'))
        except:
            self._webui_password = ""
            
    def _save_value(self, section, option, value):
        self._parser.set(section, option, str(value))
        with codecs.open(self._filename, 'w', encoding='utf-8') as f:
            self._parser.write(f)
           
    def server_url(self):
        return self._server_url
       
    def login(self):
        return self._login
      
    def password(self):
        return self._password
    
    def set_password(self, value): 
        self._save_value('remote_control', 'password', self._enc1.encrypt_text(value))
        self._password = value
        
    def logfile(self):
        return self._logfile
    
    def mediafiles_path(self):
        return self._mediafiles_path
    
    def mplayer_executable(self):
        return self._mplayer_executable
    
    def omplayer_executable(self):
        return self._omplayer_executable
    
    def omplayer_arguments(self):
        return self._omplayer_arguments
    
    def verbose_logging(self):
        return self._verbose == "yes" or self._verbose == "y" or self._verbose == "true"
    
    def webui_password(self):
        return self._webui_password
    
    def set_webui_password(self, value):
        self._save_value('webui', 'password', self._enc2.encrypt_text(value))
        self._webui_password = value
