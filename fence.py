import os

class fence:
    def __init__(self,directory):
        self.setImageDir(directory)
    def setImageDir(self,directory):
        self.basepath = directory
        self.img_name_list = list(filter(lambda x: os.path.isfile(os.path.join(self.basepath, x)) and x.endswith(".png"),os.listdir(self.basepath)))
        print(self.img_name_list)