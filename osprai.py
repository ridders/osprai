import gi
gi.require_version('Gtk', '3.0')
import os
import sys
import os.path
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import GdkPixbuf, Gdk
from modules import folders

class image:

	def on_window1_destroy(self, object, data=None):
		gtk.main_quit()
		
	def filechooserdialog_cancel_button_clicked(self, widget, data=None):
		self.filechooserdialog.hide()	
	
	def filechooserdialog_open_button_clicked(self, widget, data=None):
		selection = self.filechooserdialog.get_current_folder()
		self.filechooserdialog.hide()
		
		self.thumb_view.set_model(self.model)
		self.thumb_view.set_pixbuf_column(0)
		self.thumb_view.set_columns(-1)
		
		thumbs = folders.load_images(selection)
		for thumbnail in thumbs:
		
			pixbuf = Pixbuf.new_from_file("temp/{0}".format(thumbnail))
			pixbuf = pixbuf.scale_simple(self.desired_width, self.desired_height, GdkPixbuf.InterpType.HYPER)
			self.model.append([pixbuf])

	def on_file_open_activate(self, menuitem, data=None):
		self.filechooserdialog.run()
		
	def on_file_new_activate(self, menuitem, data=None):
		self.filechooserdialog.run()
	
	def on_adjustment1_changed(self, widget, *argvs):
		self.model.clear()
		self.desired_width = self.adjustment.get_value()
		self.desired_height = self.adjustment.get_value()
		self.filechooserdialog_open_button_clicked(self.desired_width,self.desired_height)
	
	def iconview_button_press_event(self, iconview, event):
		if event.button == 3:
			print("item right clicked")
			self.popup.popup(None, None, None, None, event.button, event.time)
			
	def iconview_item_activated(self, widget, data=None):
		print("item double clicked")
	
	def iconview_selection_changed(self, widget, data=None):
		print("item selected")
		#self.on_item_activated(widget, widget.get_selected_items()[0])
		
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
				
		self.desired_width = self.adjustment.get_value()
		self.desired_height = self.adjustment.get_value()
		
		self.window.maximize()
		self.window.show()
		self.window.show_all()
		

if __name__ == "__main__":
	main = image()
	gtk.main()
