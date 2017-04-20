import cv2
import os
import sys
import hashlib
import re
from datetime import datetime
from os.path import splitext
	
def create_case(selection):	
	for dirpath,_,filenames in os.walk(selection):
		print("completed walking selection")
		case_dir = (os.path.join(selection, "case.osp"))
		thumbs_dir = (os.path.join(case_dir, "thumbs"))
		if os.path.isdir(thumbs_dir) == False:
			os.makedirs("{0}".format(thumbs_dir))
			print("created thumbs directory")

def create_index_and_thumbs(selection):
	total_count = 0 #Quantity of media including ducplicates. This is being used as the unqiue ID for IconView
	hashes = []
	file_paths = []
	case_dir = (os.path.join(selection, "case.osp"))
	thumbs_dir = (os.path.join(case_dir, "thumbs"))
	index = (os.path.join(selection, "case.osp", "index.csv"))
	
	print("populating file path list")
	for root,dirpath,filenames in os.walk(selection):
		if "case.osp" in dirpath:	
			dirpath.remove('case.osp')
		for file in filenames:
			file_path = (os.path.join(os.path.abspath(root),file))
			file_paths.append(file_path)
	print("file path list generated")
	
	print("commencing the population of index.csv")
	with open(index, "a") as fo:
		for item in file_paths:
			md5 = hashlib.md5(open(item, 'rb').read()).hexdigest()
			if md5 not in hashes:
				hashes.append(md5)
				# create thumbs
				size = 300, 300
				im = cv2.imread(item)
				resized_image = cv2.resize(im, size)
				filename,extension = splitext(item)
				thumb_name = ("thumbnail_{0}{1}".format(total_count,extension))
				thumbs_path = (os.path.join(thumbs_dir, thumb_name))
				cv2.imwrite(thumbs_path, resized_image)
					
			fo.write("{0},{1},{2},{3}{4}".format(total_count,md5,thumbs_path,item,"\n"))
			total_count+=1
		print("completed populating index.csv")
				
	uniques = (len(hashes))
	return(total_count, uniques)
