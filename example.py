from smuggler import smuggler
import os

# smuggler( file_name, num_of_bits_to_hide_in_a_byte, buffer_size_in_byte )
s = smuggler("FileZilla_3.51.0_win64-setup.exe",6,8);
#s = smuggler("text.txt",1,8);
s.setImageDir("Images")
s.writeToImages()

