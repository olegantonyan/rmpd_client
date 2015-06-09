#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv, exit

import utils.config
import utils.crypto

def main():
    if len(argv) < 3:
        exit("you have to specify type and password")
    
    if argv[1] == 'webui':
        key = utils.config.KP2
    elif argv[1] == 'remote_control':
        key = utils.config.KP1
    else:
        exit("unknown password type, available: 'remote_control', 'webui'")
        
    c = utils.crypto.AESCipher(key)
    
    if len(argv) == 4 and argv[2] == 'decrypt':
        print(c.decrypt_text(argv[3]))
    else:
        print(c.encrypt_text(argv[2]))
    exit(0)

if __name__ == '__main__':
    main()