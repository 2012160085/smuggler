import numpy as np
import hashlib
import os
from PIL import Image
class smuggler:    

    def __init__(self,_filename,_modulation=3,_byte_buff_size=4):
        self.modulation = _modulation
        self.byte_buff_size = _byte_buff_size
        self.bit_buffer = np.array([],dtype=np.uint8)
        self.setFile(_filename)
        self.calHash = self.getCalHash()
        
    def setFile(self,_filename):
        self.file_name = _filename
        self.file_stream = open(_filename,'rb')  
        self.file_name_bytes = _filename.encode() + (64 - len(_filename.encode()))*bytes([32])
        self.file_size_bytes = os.path.getsize(_filename).to_bytes(8, byteorder="little")
        self.file_hash_bytes = self.getHash(_filename)     
        
    def getHash(self,file_name, blocksize=65536):
        afile = open(file_name, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.digest()      
        
    def setImage(self,_imgArr):
        self.img_array = _imgArr
        
    def addBytes(self):
        if not self.file_stream.closed:
            _bytes = bytearray(self.file_stream.read(self.byte_buff_size))
            if not _bytes:
                self.file_stream.close()
            bits = np.unpackbits(_bytes)
            self.bit_buffer = np.append(self.bit_buffer,bits)
        return self.file_stream.closed
        
        
    def calculateByte(self,origin,value,bpp):
        value_int = np.packbits(value)[0]
        r = origin%bpp #15
        if abs(r-value_int) < bpp/2:
            origin = origin+value_int-r
        else: 
            origin = origin + (lambda bpp,r,value_int: bpp-r+value_int if value_int<r else -bpp-r+value_int)(bpp,r,value_int)
        if origin < 0:
            origin = origin + bpp
        if origin > 255:
            origin = origin - bpp
        return origin
    def getCalHash(self):
        print("===  Calculating byte hash...")
        _hash = {}
        for b in range(1,8):
            for i in range(0,256):
                for j in range(0,2**b):
                    bits = np.unpackbits(np.array([j],dtype=np.uint8))
                    key = tuple([i]+bits.tolist()[-b:])
                    _hash[key] = self.calculateByte(i,bits,2**b)
        print("===  Completed")
        return _hash   
        
    def pickBits(self):
        if self.bit_buffer.size < self.modulation:
            self.addBytes()
        if self.bit_buffer.size == 0 :
            return []
        value = self.bit_buffer[:self.modulation]
        self.bit_buffer = self.bit_buffer[self.modulation:]
        return value
        
    def writeByte(self):
        for i,row in enumerate(self.img_array):
            for j,pixel in enumerate(row):
                for k,c in enumerate(pixel):
                    value = self.pickBits()
                    if len(value) is 0:
                        return False 
                    self.img_array[i][j][k] = self.calHash[tuple([c]+value.tolist())]
                    
    def writeToImg(self):
        self.writeByte()
        return self.img_array

class fence():
    def readFromImg(self,_image):
        
        return 
        