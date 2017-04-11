from PIL import Image
import os
import sys

# "selection" is the variable handled by the filechooserdialog. It specifies the selected file or path.

def load_images(selection):
	if os.name == 'nt':
		file_path = ("{0}\\".format(selection))
	else:
		file_path = ("{0}/".format(selection))
	
	if os.path.isdir("temp") == False:
		os.makedirs("temp")
		
		for root, dirs, files in os.walk(selection):
			count = 0
			for item in files:
				count +=1
				file_ext = item.split('.') 
				desired_width = 300
				desired_height = 300
				
				output = ("temp/thumbs{0}.{1}".format(count,file_ext[1]))
				
				media = Image.open("{0}{1}".format(file_path, item))
				media = media.resize((desired_width, desired_height), Image.ANTIALIAS)
				media.save(output)
