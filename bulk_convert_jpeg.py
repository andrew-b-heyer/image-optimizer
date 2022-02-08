#!/usr/bin/env python3

# This utlitiy script works by gathering all images in the local directory into a dictionary. 
# The dictionary looks like {jpeg : [taco.jpeg, sauce.jpeg, ...], png : [bacon.png, egg.png,...]} 
# The tool then iterates through each array value and begins processing the image outputting it 
# into a user defined folder.  

# Get list of all files in local directoy
import os
import sys
import subprocess
import time

from os import listdir
from os.path import isfile, join

from PIL import Image

folder_out=str(sys.argv[1])

# Create lists of all image file names
current_path = os.getcwd()

jpg_files = [f for f in listdir(current_path) if f.endswith( ('.jpg') ) or f.endswith( ('.JPG') )]
jpeg_files = [f for f in listdir(current_path) if f.endswith( ('.jpeg') )]
png_files = [f for f in listdir(current_path) if f.endswith( ('.png') )]
webp_files = [f for f in listdir(current_path) if f.endswith( ('.webp') )]

all_files = {'jpg_files' : jpg_files, ' jpeg_files' : jpeg_files, 'png_files' : png_files, 'webp_files' : webp_files}

webp_counter = 0

# Begin image processing
counter = 1
for file_type in all_files:
	for file in all_files[file_type]:
		im = Image.open(file)
		width, height = im.size

		file_out = folder_out + file

		# Only perform resize on images greater than 1600 x 1600
		if width >= 1600 or height >= 1600:
			print(str(counter) + " resizing "+str(file) + " height="+str(height)+ " width="+str(width))	

			# If the file type is webp, we need to process it differently. We must use the cwebp command, which I 
			# don't use to begin with since it must be told either a max height or a max width. I cannot simply tell
			# it to not exceed either the height or width and resize accordingly keeping the same aspect ratio. 
			# Perhaps it would be cleaner to use cwebp at a future time, ah well. P.S. apologies for the amount of
			# nested if statements.
			if file_type == 'webp_files':

				# In the case of an image that is both too wide and high then we need to know which is the greatest
				# and only run the resize against that side.
				if width >= 1600 and height >= 1600:
					if width >= height:
						subprocess.run(['cwebp','-resize','1600','0',file,'-o',file_out])
					else:
						subprocess.run(['cwebp','-resize','0','1600',file,'-o',file_out])
				
				elif height > 1600:
					subprocess.run(['cwebp','-resize','0','1600',file,'-o',file_out])

				elif width > 1600:
					print("GUUUUANNNNTESSS")
					subprocess.run(['cwebp','-resize','1600','0',file,'-o',file_out])

			else:
				subprocess.run(['sips','-Z','1600',file,'--out',file_out])


		# Move those which are under 1600 Height or Width
		else:
			print(str(counter) + " skipping resize "+str(file) + " height="+str(height)+ " width="+str(width))
			subprocess.run(['cp', file, file_out])

		# Convert the file into webp
		file_out_reformated = os.path.splitext(file_out)[0]+'.webp'
		subprocess.run(['cwebp',file_out,'-o',file_out_reformated])
		counter+=1


subprocess.run(['find',folder_out,'-type','f','!','-iname','*.webp','-delete'])


print("processing " + str(len(jpg_files)) + " jpg files")
print("processing " + str(len(jpeg_files)) + " jpeg files")
print("processing " + str(len(png_files)) + " png files")
print("processing " + str(len(webp_files)) + " webp files")

print("Total " + str(len(jpg_files)+len(jpeg_files)+len(png_files)+len(webp_files)))
print(webp_counter)