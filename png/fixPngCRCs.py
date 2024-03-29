#!/usr/bin/env python3


"""
basic png chunk fix
will fix the CRC if you manually changed some data in the chunk. 
Don't use the same file as input and output as it has not been tested 
	and it WILL have unexpected behavior.
More documentation on http://www.libpng.org/pub/png/spec/1.2/PNG-Contents.html
	especially session 3. File Structure

Regards,
Alban Daumer (https://github.com/DelTa-B)

Note to myself: Ne pas oublier de mettre à jour ces writeUps si besoin
	- AngeCryption (Stegano) sur root-me.org 
"""

import sys
import binascii
import os.path

def usage():
	print("Usage: %s infile outfile mode" % sys.argv[0])
	print("\tmode: 0 -> display CRC errors but don't fix them, but truncate after IEND chunk")
	print("\t      1 -> Fix only critical chunks (chunk whose type starts with capital letter)")
	print("\t      2 -> Fix all chunks", end = "\n\n")
	print("The infile must exist and the outfile must NOT exist")
	print("If the png file doesn't end with a complete chunk, a harmless error")
	print("\twill display and outfile may be garbage.");
	exit(0)

if (len(sys.argv) != 4):
	print("wrong number of args")
	usage()

mode = sys.argv[3]

if (mode != '0' and mode != '1' and mode != '2'):
	print("wrong mode")
	usage()


infile = sys.argv[1]
outfile = sys.argv[2]
print ("\tinfile={}".format(infile))
print ("\toutfile={}".format(outfile))

if not os.path.exists(infile):
	print("infile must exist")
	usage()

if os.path.exists(outfile):
	print("Outfile must NOT exist")
	usage()

	

inf = open(infile, "rb")
outf = open(outfile, "wb")

png_signature = inf.read(8)
print ("signature is {}".format(png_signature))

outf.write(png_signature)

finished = False
while (not finished) :
	#reading chunk size
	chunk_size = inf.read(4)
	if not chunk_size:
		break
	chunk_size_i = int.from_bytes(chunk_size, "big")
	#reading chunk type identifier
	chunk_type = inf.read(4)
	#reading the chunk data
	data = inf.read(chunk_size_i)
	#reading the CRC from the file
	actual_crc=inf.read(4)
	actual_crc_display = ':'.join("{:02x}".format(c) for c in (actual_crc))
	#calculating what the CRC should have been, from chunk type and data
	expected_crc = binascii.crc32(chunk_type + data).to_bytes(4, byteorder='big')
	expected_crc_display = ':'.join("{:02x}".format(c) for c in (expected_crc))
	
	print("Found a chunk whose type is {} and whose size is {}".format(chunk_type, chunk_size_i))
	print("\tActual crc is   {} ...".format(actual_crc_display), end ="")
	if actual_crc != expected_crc:
		print("\n----CRC IS WRONG----")
		print("\tExpected crc is {}".format(expected_crc_display))
	else:
		print("\tCRC is OK")
	outf.write(chunk_size)
	outf.write(chunk_type)
	outf.write(data)
	if mode == '0' or actual_crc == expected_crc:
		print("\tKeeping crc")
		outf.write(actual_crc)
	elif mode == '2':
		print("\tFixing crc")
		outf.write(expected_crc)
	elif mode == '1':
		if chunk_type[0]>=65 and chunk_type[0] <= 90: # capital ASCII letter
			print("\tFixing crc")
			outf.write(expected_crc)
		else:
			print("\tKeeping (WRONG) crc")
			outf.write(actual_crc)
	if mode == '0' and chunk_type == b'IEND':
		finished = True
outf.close()
