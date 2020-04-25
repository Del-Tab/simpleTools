#!/usr/bin/env python3


"""
Extract all the valid chunks (you can also filter by chunk types) to a folder.
It also extracts chunks after the IEND chunk if any

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
	print("Usage: %s infile outdir [type..]" % sys.argv[0])
	print("If types are provided, only those chunks are extracted.")
	print("If the png contains other things than PNG chunks,")
	print("\ta harmless error will display and outfile will end with");
	print("\tgarbage data.");
	exit(0)

if (len(sys.argv) < 3):
	print("wrong number of args")
	usage()

types = [x.encode("utf-8") for x in sys.argv[3:]]

print("types: {}".format(types))

infile = sys.argv[1]
outdir = sys.argv[2]
print ("\tinfile={}".format(infile))
print ("\toutDir={}".format(outdir))

if not os.path.isfile(infile):
	print("error: {} is not a file".format(infile))
	usage()

if os.path.isfile(outdir):
	print("error: {} exists and is a file".format(outdir))
	usage()
if os.path.exists(outdir):
	print("warning: {} already exists".format(outdir))
	if os.listdir(outdir):
		print("error: {} is not empty".format(outdir))
		usage()
else:
	os.makedirs(outdir)

inf = open(infile, "rb")

#writing png_signature
png_signature = inf.read(8)
with open('{}/magicHeader'.format(outdir),'wb') as f:
	f.write(png_signature)

chunk_num = 0

while (True) :
	#reading chunk size
	chunk_size = inf.read(4)
	if not chunk_size:
		break
	chunk_size_i = int.from_bytes(chunk_size, "big")
	#reading chunk type identifier
	chunk_type = inf.read(4)
	#reading the chunk data
	data = inf.read(chunk_size_i)
	#reading (and ignoring) the CRC from the file
	actual_crc=inf.read(4)
	if not types or chunk_type in types:
		print("Found a chunk whose type is {} and whose size is {}".format(chunk_type, chunk_size_i))
		with open('{}/chunk_{}_{}'.format(outdir,chunk_num, chunk_type.decode("utf-8")), 'wb') as outf:
			outf.write(data)
	chunk_num += 1
print("done")
