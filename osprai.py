import gi
gi.require_version('Gtk', '3.0')
import os
import sys
import os.path
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import GdkPixbuf, Gdk
from modules import dir_parser

class image:
	
	def on_window1_destroy(self, object, data=None):
		gtk.main_quit()
		
	def filechooserdialog_cancel_button_clicked(self, widget, data=None):
		self.filechooserdialog.hide()	
	
	def filechooserdialog_open_button_clicked(self, widget, data=None):
		self.selection = self.filechooserdialog.get_current_folder()
		dir_parser.create_case(self.selection)
		
		total_count, uniques = dir_parser.create_index_and_thumbs(self.selection)
		self.total_count.set_text(str(total_count))
		self.total_unique.set_text(str(uniques))
		self.filechooserdialog.hide()
		
		self.thumb_view.set_model(self.model)
		self.thumb_view.set_pixbuf_column(0)
		self.thumb_view.set_columns(-1)
		
		self.desired_width = self.adjustment.get_value()
		self.desired_height = self.adjustment.get_value()
		
		self.load_thumbs(self.selection,self.desired_width,self.desired_height)
		
	def load_thumbs(self, selection, width, height):
		index = (os.path.join(selection, "case.osp", "index.csv"))
		thumbs_locations = []
		with open(index, "r") as fo:
			for line in fo:
				attribute = (line.split(","))
				thumbs_path = attribute[2]
				if thumbs_path not in thumbs_locations:
					thumbs_locations.append(attribute[2])
				
			for each in thumbs_locations:
				pixbuf = Pixbuf.new_from_file(each)
				pixbuf = pixbuf.scale_simple(self.desired_width, self.desired_height, GdkPixbuf.InterpType.HYPER)
				self.model.append([pixbuf])
		
	def on_file_open_activate(self, menuitem, data=None):
		self.filechooserdialog.run()
		
	def on_file_new_activate(self, menuitem, data=None):
		self.filechooserdialog.run()
	
	def on_adjustment1_changed(self, widget,*argvs):
		self.model.clear()
		self.desired_width = self.adjustment.get_value()
		self.desired_height = self.adjustment.get_value()
		self.load_thumbs(self.selection,self.desired_width,self.desired_height)

				
	def iconview_button_press_event(self, iconview, event):
		if event.button == 3:
			print("item right clicked")
			self.popup.popup(None, None, None, None, event.button, event.time)

	def iconview_item_activated(self, widget, data=None):
		print("item double clicked")
	
	def iconview_selection_changed(self, widget, data=None):
		print("item selected")
		
		
	def show_result_activate(self, menuitem, data=None):
		#print (self.thumb_view.get_selected_items()[0])
		selected_path = (self.thumb_view.get_selected_items())
		#for f in selected_path:
			#print(f)
		# (pathlist) = self.thumb_view.get_selected_items()
		# for path in pathlist :
			# tree_iter = self.model.get_iter(path)
			# value = self.model.get_value(tree_iter,0)
			# print value

		self.model, treeiter = 0 
			

	def __init__(self):
		self.gladefile = "gui.glade"
		self.builder = gtk.Builder()
		self.builder.add_from_file(self.gladefile)
		self.builder.connect_signals(self)
		self.window = self.builder.get_object("window1")
		self.thumb_view = self.builder.get_object('iconview2')
		self.model = self.builder.get_object('liststore1')
		self.scale = self.builder.get_object('scale1')
		self.adjustment = self.builder.get_object('adjustment1')
		self.filechooserdialog = self.builder.get_object("filechooserdialog1")
		self.popup = self.builder.get_object("popup")
		self.total_count = self.builder.get_object("label36")
		self.total_unique = self.builder.get_object("label35")
		self.selection = ""	
		self.window.maximize()
		self.window.show()
		self.window.show_all()
		

if __name__ == "__main__":
	main = image()
	gtk.main()
