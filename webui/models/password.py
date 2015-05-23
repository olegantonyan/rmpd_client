#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import match
from logging import getLogger

log = getLogger(__name__)

import utils.config

class Password(object):
    def __init__(self, current, new=""):
        self.__current_password = current
        self.__new_password = new
        self.__errors = ""
        
    def save(self):
        if Password.password() != self.__current_password:
            self.__errors = "Wrong current password"
            return False
        if len(self.__new_password) < 4:
            self.__errors = "Password must be at least 4 characters long"
            return False
        if match('^[\w]+$', self.__new_password) is None:
            self.__errors = "Password may only contain latin characters and digits"
            return False
        try:
            utils.config.Config().set_webui_password(self.__new_password)
            log.warning("new admin password saved")
            return True
        except:
            log.exception("error saving password")
            self.__errors = "Error saving new password, please try another one"
            return False
    
    def errors(self):
        return self.__errors
    
    @staticmethod
    def authenticate(username, password):
        return username == "admin" and password == Password.password()
    
    @staticmethod
    def password():
        return utils.config.Config().webui_password()
    
    
        