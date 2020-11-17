from smuggler import smuggler
from fence import fence

# hide file in png images
s = smuggler("FileZilla_3.49.1_win64-setup.exe",6,8) #file to hide
s.setImageDir("demo") #directory where png images are
s.writeToImages()

# get file from png images
f = fence("demo\\FileZilla_3.49.1_win64-setup.exe.smg",6) #d
f.writeFile()
