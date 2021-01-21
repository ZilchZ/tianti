#!/usr/bin/python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from binascii import a2b_hex, b2a_hex


class Cipher(object):
    def __init__(self, key, length=16):
        self.length = length
        self.model = AES.MODE_CBC
        self.key = self.modify_length(key)

    def modify_length(self, s):
        length = len(s)
        mod = length % self.length
        if mod == 0:
            add = 0
        else:
            add = self.length - mod
        return s + "\0" * add

    def encrypt(self, text):
        text = self.modify_length(text)
        aes = AES.new(self.key, self.model, b"0" * self.length)
        cipher_text = aes.encrypt(text)
        return b2a_hex(cipher_text)

    def decrypt(self, text):
        text = self.modify_length(text)
        aes = AES.new(self.key, self.model, b"0" * self.length)
        plain_text = aes.decrypt(a2b_hex(text))
        return plain_text.rsplit("\0")[0]


if __name__ == '__main__':
    c = Cipher("hello")
    print c.encrypt("abc")
    print c.encrypt("abc" * 7)
    print c.decrypt("0920e047c7f8285fc60988cad7f621f9")
    print c.decrypt("655ce7a2d60979dc41782adab079812dc2ff05e3f997aeb69d956bb79ed7bc8e")
