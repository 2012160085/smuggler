import numpy as np
import hashlib
import os
from PIL import Image
import datetime
import sys
import random
import string
from functools import reduce

class fence:
    def __init__(self,directory,modulation):
        self.modulation = modulation
        self.image_dict = {}
        self.setImageDir(directory)
        self.bits_buffer = []
        self.bytes_buffer = np.array([],dtype=np.uint8)
    def setImageDir(self,directory):
        self.basepath = directory
        self.img_name_list = list(filter(lambda x: os.path.isfile(os.path.join(self.basepath, x)) 
                                                   and x.endswith(".png")
                                        ,os.listdir(self.basepath)
                                        )
                                )
        for img_name in self.img_name_list:
            img = Image.open(os.path.join(self.basepath, img_name))
            arr = np.array(img)
            order = list(map(lambda x: x%(2**self.modulation),arr.flatten()[:1+32//self.modulation]))
            bits = np.unpackbits(np.array(order,dtype=np.uint8))[:256]
            valid_bits = []
            for i in range(0,len(bits)):
                if i % 8 >= 8-self.modulation:
                    valid_bits.append(bits[i])
            valid_bits = valid_bits[:32]
            order_bytes = np.array(np.packbits(valid_bits),dtype = np.int64)
            self.image_dict[reduce((lambda x,y : x*256 + y), reversed(order_bytes+[0]))] = img_name
        if max(self.image_dict.keys())+1 != len(self.image_dict.keys()):
            print('err')

    def readImage(self,order):
        img_arr = np.array(Image.open(os.path.join(self.basepath, self.image_dict[order]))
                           ,dtype= np.uint8)
        flat_img = img_arr.flatten()
        decoded = list(map(lambda x: x%(2**self.modulation),flat_img))
        data_bits =  np.unpackbits( np.array(decoded,dtype=np.uint8))
        buff = []
        for i,x in enumerate(data_bits):
            if i%8 >= 8-self.modulation:
                buff.append(x)
        file_order_bits = buff[:4*8]
        buff= buff[4*8:] 
        file_order_bytes = np.packbits(file_order_bits)
        if order == 0:
            file_name_bits = buff[:64*8]
            buff = buff[64*8:]
            file_size_bits = buff[:8*8]
            buff = buff[8*8:]
            file_hash_bits = buff[:16*8]
            buff = buff[16*8:]
            file_name_bytes = np.packbits(file_name_bits)
            file_size_bytes = np.packbits(file_size_bits)
            file_hash_bytes = np.packbits(file_hash_bits)
            self.file_name = bytearray(file_name_bytes).decode()
            self.file_size = int.from_bytes(file_size_bytes, byteorder='little', signed=False)
            print('file name : ',self.file_name)
            print( 'file size : ',self.file_size,'B')
            print('file hash : ',''.join('{:02x}'.format(x) for x in file_hash_bytes))
        self.bits_buffer = self.bits_buffer + buff
        print('img order : ', int.from_bytes(file_order_bytes, byteorder='little', signed=False))
    def _packBitsBuffer(self,buffer_size):
        self.bytes_buffer = np.append(self.bytes_buffer , np.packbits(self.bits_buffer[:buffer_size]))
        self.bits_buffer = self.bits_buffer[buffer_size:]

    def writeFile(self,buffer_size = 65536):
        idx = 0
        while idx < len(self.image_dict):
            if len(self.bits_buffer) < buffer_size:
                self.readImage(idx)
            self._packBitsBuffer(buffer_size)
            oFile = open(os.path.join(self.basepath,'result',self.file_name), "wb")
            oFile.write(bytearray(self.bytes_buffer))
            self.packBitsBuffer = np.array([],dtype=np.uint8)
            idx = idx + 1
