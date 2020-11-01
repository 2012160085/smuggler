# Tool for hiding data in PNG images

After splitting the binary file, hide it in the most insignificant bits of the image pixels.

* Usage

  ```python
  from smuggler import smuggler
  
  # smuggler( file_name, num_of_bits_to_hide_in_a_byte, buffer_size_in_byte )
  s = smuggler('fileToHide.zip',4,8)
  s.setImage('original_image.png')
  s.writeToImg('output_image.png')
  ```

  


| ![original.png](https://github.com/2012160085/smuggler/blob/main/Images/12bit_per_pixel.png?raw=true) | ![24bit_per_pixel.png](https://github.com/2012160085/smuggler/blob/main/Images/24bit_per_pixel.png?raw=true) | ![28bit_per_pixel.png](https://github.com/2012160085/smuggler/blob/main/Images/28bit_per_pixel.png?raw=true) |
| :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|                          *Original*                          |                     *24 Bits per pixel*                      |                     *28 Bits per pixel*                      |

