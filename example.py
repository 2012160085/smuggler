from smuggler2 import smuggler
import os

# smuggler( file_name, num_of_bits_to_hide_in_a_byte, buffer_size_in_byte )
s = smuggler("Git-2.29.2-64-bit.exe",6,8);
s.setImageDir("Images")
s.writeToImages()