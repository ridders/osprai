import cv2
import os
import sys
from multiprocessing import Pool
from datetime import datetime

# "selection" is the variable handled by the filechooserdialog. It specifies the selected file or path.

def load_images(selection):
	files = []
	count = 0
	
	if os.path.isdir("temp") == False:
		os.makedirs("temp")
	else:
		for dirpath,_,filenames in os.walk("temp"):
			thumbs = files
			return(thumbs)
			
	for dirpath,_,filenames in os.walk(selection):
		for f in filenames:
			files.append (os.path.abspath(os.path.join(dirpath, f)))

	for image in files:
		count+=1
		size = 300, 300
		im = cv2.imread(image)
		resized_image = cv2.resize(im, size)
		cv2.imwrite("temp/thumbnail_%s.jpg" % count, resized_image) 
		
	for dirpath,_,filenames in os.walk("temp"):
		thumbs = filenames
		return(thumbs)
	
	
		
		
