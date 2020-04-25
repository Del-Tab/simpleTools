#!/usr/bin/env python3


"""
will create a png from separated chunk data.
You must provide a folder that contains the chunks and a target file name.
Chunks (and signature) are ordered with respect to the names of files in the folder:
- first the signature/magic raw data must be stored in a file named magicHeader
- then the chunks file names must match this format
	chunk_<chunk_order>_<chunk type name>
	with :
		- chunk_order: an integer corresponding to the ascending order you want the chunks to be stored in the png
		- chunk type name: the 4 digit type of the chunk (ex IHDR)

all other file names will be ignored.
The content of the file will be the content of the data part of the chunk.

You can create such a folder from a PNG file using the extractPngChunks program in the same git repository

More documentation about PNG chunks on http://www.libpng.org/pub/png/spec/1.2/PNG-Contents.html
	especially session 3. File Structure

Regards,
Alban Daumer (https://github.com/DelTa-B)
 
"""

import sys
import binascii
import os.path
import glob


def usage():
	print("Usage: %s indir outfile" % sys.argv[0])
	exit(-1)

if (len(sys.argv) != 3):
	print("wrong number of args")
	usage()


indir = sys.argv[1]
outfile = sys.argv[2]
print ("\tindir={}".format(indir))
print ("\toutfile={}".format(outfile))

if os.path.isfile(indir):
	print("{} exists but is a file".format(outdir))
	usage()
	
if os.path.exists(outfile):
	print("error: outfile already exists")
	usage()

magicFileName = indir+'/magicHeader'
if not os.path.exists(magicFileName):
	print('error: missing magicHeader file in {}'.format(indir))
	usage()

files=[]
for f in glob.glob(indir+'/chunk_*_*'):
	if not os.path.isfile(f):
		print("error: {} is not a regular file".format(f))
		exit(-1)
	print("found a chunk in " + f)
	(_, order, type_name) = f.rsplit("_",2)
	if len(type_name) != 4:
		print("warning: ignoring this chunk because type must be 4 characters long, got: "+ type_name)
	else:
		files.append([order, type_name])

def takeFirstAsInt(elems):
	return int(elems[0])
files.sort(key=takeFirstAsInt)

print(files)

with open(outfile, 'wb') as outf:
	with open(magicFileName, 'rb') as inf:
		outf.write(inf.read())
	for (chunk_num, type_name) in files:
		print('reading chunk num {} whose type is {}'.format(chunk_num, type_name))
		with open("{}/chunk_{}_{}".format(indir, chunk_num, type_name), 'rb') as inf:
			data = inf.read()
			length = len(data).to_bytes(4, "big")
			type_name_bytes = type_name.encode("utf-8")
			crc = binascii.crc32(type_name_bytes + data).to_bytes(4, byteorder='big')
			outf.write(length)
			outf.write(type_name_bytes)
			outf.write(data)
			outf.write(crc)
print("done")
