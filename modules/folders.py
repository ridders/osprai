from PIL import Image
import os
import sys

def load_images(selection):
	if os.name == 'nt':
		dir_path = ("{0}\\{1}\\".format(selection, "thumbs"))
		file_path = ("{0}\\".format(selection))
	else:
		dir_path = ("{0}/{1}/".format(selection, "thumbs"))
		file_path = ("{0}/".format(selection))
	
	if os.path.isdir(dir_path) == False:
		os.makedirs(dir_path)
		for root, dirs, files in os.walk(selection):
			count = 0
			for file in files:
				file_ext = file.split('.') 
				count +=1
				desired_width = 300
				desired_height = 300
				output = ("{0}{1}{2}.{3}".format(dir_path,"thumb",count,file_ext[1]))
				#print(output)
				media = Image.open("{0}{1}".format(file_path, file))
				media = media.resize((desired_width, desired_height), Image.ANTIALIAS)
				media.save(output)
				

		#return(files)
		#~ count = 0
		#~ for file in files:
			#~ count+=1
			#~ filename = ("{0}{1}{2}".format("thumb",count,".JPG"))
			#~ pixbuf = Pixbuf.new_from_file("{0}{1}".format(thumbs, filename))
			#~ pixbuf = pixbuf.scale_simple(desired_width, desired_height, GdkPixbuf.InterpType.HYPER)
			#~ self.model.append([pixbuf])




				#allocation = parent_widget.get_allocation()
				#desired_width = allocation.width
				#desired_height = allocation.height
		

					#self.pic.set_from_file("{0}{1}".format("Thumbs/",filename))
					
#image.test()
