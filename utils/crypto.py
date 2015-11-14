# -*- coding: utf-8 -*-

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto import Random


BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s: s[:-ord(s[len(s)-1:])]


class AESCipher(object):
    def __init__(self, key):
        if len(key) not in AES.key_size:
            raise ValueError("AES key must be either 16, 24, or 32 bytes long")
        self.__key = key

    def encrypt_text(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.__key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt_text(self, enc):
        enc = b64decode(enc.encode('utf-8'))
        iv = enc[:16]
        cipher = AES.new(self.__key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('utf-8')