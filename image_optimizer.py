#!/usr/bin/env python3


import os
import sys
import subprocess
import time
import argparse
import pathlib

from os import listdir
from os.path import isfile, join
from PIL import Image


parser = argparse.ArgumentParser(
	description='''Image Optimizer makes bulk image optimization easy. It converts images of .jpg, 
	.jpeg, .png and webp types into .webp. Any image within the given directory that has a length or
	heigh greater than 1600px will be reduced to 1600px while maintaining aspect ratios. Any image 
	below 1600px will be ignored and only have their file types converted.

	1600 is choosen since this is Wordpress's recommended image size. Perhaps future updates will be
	made to allow for a specified dimension.''')

parser.add_argument('input_directory', type=pathlib.Path, help='Directory of images to be optimized')
parser.add_argument('-o', '--output', type=pathlib.Path, help='Directory to place optimized images')
args = parser.parse_args()


# Identify our folder_in (un-optimized images) and where our folder_out (optimized images) point to.
folder_in=args.input_directory
folder_out = ""
if args.output:
	folder_out = args.output
else:
	folder_out = pathlib.Path(str(pathlib.Path(folder_in.parent/folder_in.name))+"_optimizado")
print(folder_out)
print(folder_in.name)
subprocess.run(['mkdir','-p',f'{folder_out}{os.sep}'])
	
# Identify all file names withing the given file in directory
jpg_files = [f for f in listdir(folder_in) if f.endswith( ('.jpg') ) or f.endswith( ('.JPG') )]
jpeg_files = [f for f in listdir(folder_in) if f.endswith( ('.jpeg') )]
png_files = [f for f in listdir(folder_in) if f.endswith( ('.png') )]
webp_files = [f for f in listdir(folder_in) if f.endswith( ('.webp') )]
all_files = {'jpg_files' : jpg_files, ' jpeg_files' : jpeg_files, 'png_files' : png_files, 'webp_files' : webp_files}

# Begin image processing
webp_counter = 0
counter = 1
for file_type in all_files:
	for file in all_files[file_type]:
		
		file_in = str(pathlib.Path(folder_in/file))
		file_out = str(pathlib.Path(folder_out/file))
		print("\nAttemptting to optimize file_in: " + file_in)
		print("Attempting to write to file_out: " + str(file_out))

		im = Image.open(file_in)
		width, height = im.size
		# Only perform resize on images greater than 1600 x 1600
		if width >= 1600 or height >= 1600:
			print(str(counter) + " resizing "+str(file_in) + " height="+str(height)+ " width="+str(width))	

			# If the file_in type is webp, we need to process it differently. We must use the cwebp command, which I 
			# don't use to begin with since it must be told either a max height or a max width. I cannot simply tell
			# it to not exceed either the height or width and resize accordingly keeping the same aspect ratio. 
			# Perhaps it would be cleaner to use cwebp at a future time, ah well. P.S. apologies for the amount of
			# nested if statements.
			if file_type == 'webp_files':

				# In the case of an image that is both too wide and high then we need to know which is the greatest
				# and only run the resize against that side.
				if width >= 1600 and height >= 1600:
					if width >= height:
						subprocess.run(['cwebp','-resize','1600','0',file_in,'-o',file_out])
					else:
						subprocess.run(['cwebp','-resize','0','1600',file_in,'-o',file_out])
				
				elif height > 1600:
					subprocess.run(['cwebp','-resize','0','1600',file_in,'-o',file_out])

				elif width > 1600:
					print("GUUUUANNNNTESSS")
					subprocess.run(['cwebp','-resize','1600','0',file_in,'-o',file_out])

			else:
				subprocess.run(['sips','-Z','1600',file_in,'--out',file_out])


		# Move those which are under 1600 Height or Width
		else:
			print(str(counter) + " skipping resize "+str(file_in) + " height="+str(height)+ " width="+str(width))
			subprocess.run(['cp', file_in, file_out])

		# Convert the file_in into webp
		file_out_reformated = os.path.splitext(file_out)[0]+'.webp'
		subprocess.run(['cwebp',file_in,'-o',file_out_reformated])
		counter+=1

subprocess.run(['find',folder_out,'-type','f','!','-iname','*.webp','-delete'])

print("processing " + str(len(jpg_files)) + " jpg files")
print("processing " + str(len(jpeg_files)) + " jpeg files")
print("processing " + str(len(png_files)) + " png files")
print("processing " + str(len(webp_files)) + " webp files")
print("Total " + str(len(jpg_files)+len(jpeg_files)+len(png_files)+len(webp_files)))
print(webp_counter)
