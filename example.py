from smuggler import smuggler
from fence import fence
import os

# smuggler( file_name, num_of_bits_to_hide_in_a_byte, buffer_size_in_byte )

s = smuggler("tkde1.pdf",6,8)
s.setImageDir("Images")
s.writeToImages()

f = fence("Images/tkde1.pdf.smg",6)
f.writeFile()