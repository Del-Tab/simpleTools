#!/usr/bin/env python3


"""
basic aes128cbc encode/decode tool

This is a rapidly coded generified version of this stuff from Ange Albertini  https://github.com/indrora/corkami/blob/master/src/angecryption/rmll/angecryption/crypt.py

Regards,
Alban Daumer (https://github.com/DelTa-B)

Note to myself: Ne pas oublier de mettre à jour ces writeUps si besoin
	- AngeCryption (Stegano) sur root-me.org
"""

import sys
from Crypto.Cipher import AES


def usage():
	print("Usage: %s infile outfile key iv mode" % sys.argv[0])
	print("\tkey is cleartext, length = 16, 24, 32 characters")
	print("\tiv is hexcode, length = 32 hex characters")
	print("\tmode is e -> encrypt, d->decrypt")
	print("\n\tThe key is NOT derivated")
	exit(0)

if (len(sys.argv) != 6):
	print("wrong number of args")
	usage()



infile = sys.argv[1]
outfile = sys.argv[2]
key = sys.argv[3]
iv = bytes.fromhex(sys.argv[4])
mode = sys.argv[5]

if (mode != 'e' and mode != 'd'):
	print("bad mode\n")
	usage()
key_display = "%x" % int(key)

print ("\tinfile={}".format(infile));
print ("\toutfile={}".format(outfile));
print ("\tkey={}".format(key_display))
print ("\tiv="+':'.join("{:02x}".format(c) for c in (iv)))
print ("\tmode={}".format(mode));

AES = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv)

print("opening {}".format(infile))
with open(infile, "rb") as f:
	d = f.read()

if (mode == 'e'):
	print("\tAES ciphering ...", end="", flush=True)
	d = AES.encrypt(d)
else:
	print("\tAES deciphering ...", end="", flush=True)
	d = AES.decrypt(d)
print("done")

print("writing to {}".format(outfile))
with open(outfile, "wb") as f:
	f.write(d)
