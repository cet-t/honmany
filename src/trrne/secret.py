﻿from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding
from hashlib import pbkdf2_hmac


class MyAES:
    def __init__(self, password, *, size: int = 16, hash: str = 'sha256') -> None:
        self.__size = size
        self.__salt = get_random_bytes(self.__size)
        self.__pw = password
        self.__iv = get_random_bytes(self.__size)
        self.__hash = hash

    def en(self, src):
        key = pbkdf2_hmac(self.__hash, bytes(
            self.__pw, encoding='utf-8'), self.__salt, 50000, self.__size)
        return AES.new(key, AES.MODE_CBC, self.__iv).encrypt(Padding.pad(str(src).encode('utf-8'), AES.block_size, 'pkcs7'))

    def de(self, src):
        key = pbkdf2_hmac(self.__hash, bytes(
            self.__pw, encoding='utf-8'), self.__salt, 50000, self.__size)
        return AES.new(key, AES.MODE_CBC, self.__iv).decrypt(src)
