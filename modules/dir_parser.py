import cv2
import os
import sys
import hashlib
import re
#from multiprocessing import Pool
from datetime import datetime
	
def create_case(selection):	
	for dirpath,_,filenames in os.walk(selection):
		case_dir = (os.path.join(selection, "case.osp"))
		thumbs_dir = (os.path.join(case_dir, "thumbs"))
		if os.path.isdir(thumbs_dir) == False:
			os.makedirs("{0}".format(thumbs_dir))

def create_index_and_thumbs(selection):
	total_count = 0 #Quantity of media including ducplicates. This is being used as the unqiue ID for IconView
	hashes = []
	case_dir = (os.path.join(selection, "case.osp"))
	thumbs_dir = (os.path.join(case_dir, "thumbs"))
	index = (os.path.join(selection, "case.osp", "index.csv"))	
	with open(index, "a") as fo:
		for root,dirpath,filenames in os.walk(selection):
			dirpath.remove('case.osp') # Excludes the case folder from os.walk traversal

		for f in filenames:
			file_path = (os.path.join(selection, f))
			md5 = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
			if md5 not in hashes:
				hashes.append(md5)
				
				size = 300, 300
				im = cv2.imread(file_path)
				resized_image = cv2.resize(im, size)
				thumb_name = ("thumbnail_{0}.jpg".format(total_count))
				thumbs_path = (os.path.join(thumbs_dir, thumb_name))
				cv2.imwrite(thumbs_path, resized_image)
					
			fo.write("{0},{1},{2},{3}{4}".format(total_count,md5,thumbs_path,file_path,"\n"))
			total_count+=1
				
	uniques = (len(hashes))
	return(total_count, uniques)
