from smuggler import smuggler
import os

# smuggler( file_name, num_of_bits_to_hide_in_a_byte, buffer_size_in_byte )
s = smuggler("smuggler/python-3.5.4-amd64.exe",6,8);
s.setImageDir("smuggler/Images")

#s.writeToImg()