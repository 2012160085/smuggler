import numpy as np
import hashlib
import os
from PIL import Image
import datetime
import sys
class smuggler:    

    def __init__(self,_filename,_modulation=3,_byte_buff_size=4):
        self.modulation = _modulation
        self.byte_buff_size = _byte_buff_size
        self.setFile(_filename)
        self.bit_buffer = np.unpackbits(np.array(list(self.file_head_bytes),dtype=np.uint8))
        self.calHash = self.getCalHash()
        self.time_started = datetime.datetime.now()
        self.time_latest = datetime.datetime.now()
        
    def setFile(self,_filename):
        self.file_name = _filename
        self.file_stream = open(_filename,'rb')  
        self.file_name_bytes = _filename.encode() + (64 - len(_filename.encode()))*bytes([32])
        self.file_size = os.path.getsize(_filename)
        self.file_size_bytes = self.file_size.to_bytes(8, byteorder="little")
        self.file_hash_bytes = self.getHash(_filename)
        self.file_head_bytes = self.file_name_bytes + self.file_size_bytes + self.file_hash_bytes
        self.bytes_written = 0

    def getHash(self,file_name, blocksize=65536):
        afile = open(file_name, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.digest()      

    def setImageDir(self,directory):
        self.basepath = directory
        self.img_name_list = list(filter(lambda x: os.path.isfile(os.path.join(self.basepath, x)) and x.endswith(".png"),os.listdir(self.basepath)))

    def setImage(self,imageFile):
        img = Image.open(os.path.join(self.basepath, imageFile))
        arr = np.array(img)
        self.img_name = imageFile;
        self.img_array = arr
        
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
        r = origin%bpp 
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
        print("Hashing calculation table", end="", flush=True)
        _hash = {}
        for b in range(1,8):
            print(".", end="", flush=True)
            for i in range(0,256):
                for j in range(0,2**b):
                    bits = np.unpackbits(np.array([j],dtype=np.uint8))
                    key = tuple([i]+bits.tolist()[-b:])
                    _hash[key] = self.calculateByte(i,bits,2**b)
        print("completed")
        return _hash   
    def seconds2hhmmss(self,seconds): 
        seconds = seconds % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)     
    def pickBits(self):
        if self.bit_buffer.size < self.modulation:
            self.addBytes()
        if self.bit_buffer.size == 0 :
            return []
        value = self.bit_buffer[:self.modulation]
        self.bit_buffer = self.bit_buffer[self.modulation:]
        self.bytes_written = self.bytes_written + self.modulation/8
        return value
    def statusMsg(self,img_name,written,time):
        speed = round(0.001*written/time,2)
        remain = str(round((self.file_size - written)/1000))
        est_time = str(self.seconds2hhmmss(round((self.file_size - written)/(speed*1000))))
        return '[{img_name}] {speed}kB/s : {est_time}                     '.format(img_name=img_name, speed=speed, est_time=est_time)
    def progressBar(self,count, total, status = ''):
        bar_len = 40
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '>' * filled_len + '_' * (bar_len - filled_len)
        sys.stdout.write('%s kB [%s] %s%s %s\r' % (str(round((self.file_size-self.bytes_written)/1000)),bar, percents, '%', status))
    def writeByte(self):
        for i,row in enumerate(self.img_array):
            now_time_passed = (datetime.datetime.now()-self.time_started).total_seconds()
            if (datetime.datetime.now()-self.time_latest).total_seconds() >= 1:
                self.time_latest = datetime.datetime.now()
                msg =  self.statusMsg(self.img_name,self.bytes_written,now_time_passed)
                self.progressBar( self.bytes_written, self.file_size,msg )
            for j,pixel in enumerate(row):
                for k,c in enumerate(pixel):
                    value = self.pickBits()
                    if len(value) is 0:
                        return False 
                    self.img_array[i][j][k] = self.calHash[tuple([c]+value.tolist())]
        return True
    def saveImageAsName(self,imgName):
        im = Image.fromarray(self.img_array)
        im.save(imgName)               
    def writeToImages(self):
        self.time_started = datetime.datetime.now()
        img_idx = 0
        while True:
            self.setImage(self.img_name_list[img_idx % len(self.img_name_list)])
            need_next_img = self.writeByte()
            self.saveImageAsName(os.path.join(self.basepath , "smugglers", str(img_idx)+".png"))
            if not need_next_img:
                return True;
            img_idx = img_idx + 1