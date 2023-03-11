#!/usr/bin/env python3

def str_xor(data, key):
    for i in range(len(data)):
        data[i] ^= key[i % len(key)]
    return data

def generateKey(n):
    return [0] * n



def fillKeyInfoData(offset, data):
    for k in keys:
        for i in range(0, len(data)):
            k[(offset + i) % (len(k))] = data[i]
    return

def printKeys():
    for k in keys:
        print(*k)
    return



#key  = bytearray(open('xorkey.bin', 'rb').read())
keys=[]
for i in range(5, 13):
    keys.append(generateKey(i))


# first 2 bytes are ont of those in ASCII:
cmt="""
BM
    Windows 3.1x, 95, NT, ... etc.
BA
    OS/2 struct bitmap array
CI
    OS/2 struct color icon
CP
    OS/2 const color pointer
IC
    OS/2 struct icon
PT
    OS/2 pointer
"""
#then length of the BMP is at offset 2 on 4 bytes
#in ch3.bmp, len ='0x78ff6' =hex(495606) 495606 trouvé via ls -l
#à ces offsets dans le fichier on a : 9a e3 62 6e
#au lieu de                         : 00 07 8F F6
key=[]
key.append(0x9a^0x00) # 0x9a
key.append(0xe3^0x07) # 0xe4
key.append(0x62^0x8f) # 0xed
key.append(0x6e^0xF6) # 0x98

fillKeyInfoData(2, key)
printKeys()
#data = bytearray(open('ch3.bmp',  'rb').read())
#decoded = str_xor(data, key)
#open("out.bmp", "wb").write(decoded)
