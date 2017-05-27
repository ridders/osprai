import cv2
import os
import sys
import xxhash
import hashlib
import re
from time import gmtime, strftime
from os.path import splitext

def create_case(selection):	# Althought not vital now, keep this for later when saving changes to file
	for dirpath,_,filenames in os.walk(selection):
		case_dir = (os.path.join(selection, "case.osp"))
		thumbs_dir = (os.path.join(case_dir, "thumbs"))
		if os.path.isdir(thumbs_dir) == False:
			os.makedirs("{0}".format(thumbs_dir))

def create_index_and_thumbs(selection):
	total_count = 0 #Quantity of media including ducplicates. This is being used as the unqiue ID for IconView
	category = 0
	hashes = []
	extensions = ('.jpeg', '.jpg', '.png', '.gif') # Prevents CV2 crashing on non image media files
	case_dir = (os.path.join(selection, "case.osp"))
	thumbs_dir = (os.path.join(case_dir, "thumbs"))
	#index = (os.path.join(selection, "case.osp", "index.csv"))
	index_file = [] #Replacement to above

	print("commencing the population of virtual index")
	print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	for root,dirpath,filenames in os.walk(selection):
		if "case.osp" in dirpath:
			dirpath.remove('case.osp')
		for item in filenames:
			filename,extension = splitext(item)
			if extension in extensions:
				total_count+=1
				file_path = (os.path.join(os.path.abspath(root),item))
				thumb_name = ("thumbnail_{0}{1}".format(total_count,extension))
				thumbs_path = (os.path.join(thumbs_dir, thumb_name))
				xx = xxhash.xxh64(open(file_path, 'rb').read()).hexdigest() # !!! Stanity Check !!! does this work?
				if xx not in hashes:
					hashes.append(xx)

			index_file.append("{0},{1},{2},{3}".format(xx,thumbs_path,file_path,category))
			

	print("completed populating virtual index")
	print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	uniques = (len(hashes))
	return(total_count, uniques, index_file)

def thumbs_generator(file_loc, thumb_loc):
	print(file_loc)
	im = cv2.imread(file_loc)
	r = 100.0 / im.shape[1]
	dim = (100, int(im.shape[0] * r))
	resized_image = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)
	cv2.imwrite(thumb_loc, resized_image)
