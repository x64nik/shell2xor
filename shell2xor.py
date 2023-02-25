# -*- coding: utf-8 -*-

import argparse
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import pyscrypt
from base64 import b64encode
from os import urandom
from string import Template
import os
import sys
import re
import textwrap
from  binascii import *
import secrets
import string





# key as a string
def xor(data, key):
	l = len(key)
	x = map(ord, key)
	keyAsInt = list(x)
	return bytes(bytearray(( (data[i] ^ keyAsInt[i % l]) for i in range(0,len(data)) )))

def file_in(shellcodeFile):
	try:
		with open(shellcodeFile, 'rb') as shellcodeFileHandle:
			global shellcodeBytes
			shellcodeBytes = bytearray(shellcodeFileHandle.read())
			shellcodeFileHandle.close()
			print("[*] Shellcode file [{}] successfully loaded".format(shellcodeFile))
	except IOError:
		print("[!] Could not open or read file [{}]".format(shellcodeFile))
		quit()


def file_out(encfileName, enc_data):
	try:
		with open(encfileName, 'wb') as enc_shellcode:
			enc_shellcode.write(enc_data)
			enc_shellcode.close()
			print("[*] Shellcode Written in the File")
	except IOError:
		print("[!] Could not open or read file [{}]".format(encfileName))
		quit()


def enc_txt(filename):
	enc_file = open(encfileName, "rb") 
	byte = bytearray(enc_file.read())
	s = byte.hex()
	sx = r"\x" + r"\x".join(s[n : n+2] for n in range(0, len(s), 2))
	enc_file.close()
	return sx


def shell_for_cpp(str_shellcode):
	every = 60
	lines = []
	for i in range(0, len(str_shellcode), every):
		lines.append( '"' +str_shellcode[i:i+every] + '"')
	multi_line = '\n'.join(lines)
	return multi_line

def rand_key():
	password = ''.join((secrets.choice(string.ascii_letters + string.digits) for i in range(24)))	
	key = str(password)
	return key



if __name__ == '__main__':


	try:
		shellcodeFile = sys.argv[1]
		encfileName = sys.argv[2]
	except IndexError:
		print("Usage: python3 shell2xor.py <input_file> <output_file> <xor_key/password>")
		sys.exit(1)


	masterKey = rand_key()


	file_in(shellcodeFile)
	encrypted_shellcode = xor(shellcodeBytes, masterKey)
	data = encrypted_shellcode
	file_out(encfileName, encrypted_shellcode)

	raw_data = enc_txt(encfileName)

	yolo = shell_for_cpp(raw_data)
	# print(yolo)

	fname = encfileName[:3] + ".txt"
	final_file = open(fname, 'w')
	final_file.write(masterKey + "\n")
	final_file.write(yolo)
	final_file.close()

	print("[*] cpp suitable shellcode is been written in {0} ".format(fname))

	print("[*] XOR key: {0}".format(masterKey))






		

	
