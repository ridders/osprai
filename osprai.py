#!python2
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
from time import gmtime, strftime
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

def initial_thumbs_load(row, selection, width, height):
    items = (row.split(","))
    thumb_loc = items[1]
    file_loc = items[2]
    dir_parser.thumbs_generator(file_loc, thumb_loc)
    pixbuf = Pixbuf.new_from_file(thumb_loc)
    pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.HYPER)
    return [pixbuf, thumb_loc]
    
def thumbs_scale(row, selection, width, height):
    items = (row.split(","))
    thumb_loc = items[1]
    file_loc = items[2]
    pixbuf = Pixbuf.new_from_file(thumb_loc)
    pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.HYPER)
    return [pixbuf, thumb_loc]


class image:
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
        self.import_prep_window = self.builder.get_object("window2")
        self.import_settings = self.builder.get_object("window2")
        self.import_settings.set_size_request(300,200)
        self.popup = self.builder.get_object("popup") #what is this?
        self.import_dir_button = self.builder.get_object('button12')
        self.import_xml_button = self.builder.get_object('button11')
        #self.total_count = self.builder.get_object("label36")
        #self.total_unique = self.builder.get_object("label35")
        self.status = self.builder.get_object("label26")
        self.not_done_count = self.builder.get_object("label34")
        self.not_done_unique = self.builder.get_object("label33")
        self.selection = ""
        self.temp_index = []

        self.window.maximize()
        self.window.show()
        self.window.show_all()

    def on_window1_destroy(self, object, data=None):
        gtk.main_quit()
        
    def filechooserdialog_cancel_button_clicked(self, widget, data=None):
        self.filechooserdialog.hide()

    def filechooserdialog_open_button_clicked(self, widget, data=None):
        #self.import_prep_window.grab_focus()
        self.import_xml_button.set_sensitive(False)
        self.status.set_text(str("Calculating"))
        #self.selection = self.filechooserdialog.get_current_folder()
        self.selection = self.filechooserdialog.get_filename() # GUI updated too, this fixes folder selection
        self.filechooserdialog.hide()
        status = dir_parser.create_case(self.selection)
        
        self.status.set_text(str("importing {0} files".format(status)))
        index_file = dir_parser.create_index_and_thumbs(self.selection)
        self.temp_index = index_file
        #self.total_count.set_text(str(total_count))
        #self.total_unique.set_text(str(uniques))
        self.filechooserdialog.hide()

        self.thumb_view.set_model(self.model)
        self.thumb_view.set_pixbuf_column(0)
        self.thumb_view.set_columns(-1)

        self.desired_width = self.adjustment.get_value()
        self.desired_height = self.adjustment.get_value()
              
        print("creating thumbs for gallery view...")
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        partial_harvester = partial(initial_thumbs_load,selection=self.selection,width=self.desired_width,height=self.desired_height)
        pool = ThreadPool(3)
        #pool = multiprocessing.Semaphore(multiprocessing.cpu_count()) 
        image_list = pool.map(partial_harvester, self.temp_index[:40])
        pool.close()
        pool.join()
        
        for item in image_list:
            #print(item)
            self.model.append(item)
        
        print("Finished creating thumbs!")
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		
        self.import_prep_window.grab_focus() # This does not appear to be drawing focus back to the import prep window
        #self.status.set_text(str("Import Complete"))
    #~ def category_checker(self):

        #~ cat_count = {
        #~ '3': []
        #~ '2': []
        #~ '3': []
        #~ '4': []
        #~ }
        #~ for row in self.temp_index:
            #~ items = (row.split(","))
            #~ xx_hash = items[0]
            #~ category = items[3]
            #~ #category.append(xx_hash)
            #~ cat_count[category].get(category, category) += 1
	
    def on_import_dir_clicked(self, widget, data=None):
        self.filechooserdialog.run()
        #self.import_xml_button.set_sensitive(False)
		
    def on_file_new_activate(self, menuitem, data=None):
        
        self.import_settings.show()    #In progress but works
    
    def on_adjustment1_changed(self, widget,*argvs):
        self.model.clear()
        self.desired_width = self.adjustment.get_value()
        self.desired_height = self.adjustment.get_value()
     
        partial_harvester = partial(thumbs_scale,selection=self.selection,width=self.desired_width,height=self.desired_height)
        pool = ThreadPool(3)
        image_list = pool.map(partial_harvester, self.temp_index[:40])
        pool.close()
        pool.join()
        
        for item in image_list:
            self.model.append(item)

                
    def iconview_button_press_event(self, iconview, event):
        if event.button == 3:
            print("item right clicked")
            self.popup.popup(None, None, None, None, event.button, event.time)

    def iconview_item_activated(self, widget, data=None):
        print("item double clicked")
    
    def iconview_selection_changed(self, widget, data=None):
        print("item selected")
        
        
    def show_result_activate(self, menuitem, data=None): # This is a temporary feature to monitor the index results
        # for each in self.thumb_view.get_selected_items():
            # path = gtk.TreePath(each)
            # treeiter = self.model.get_iter(path)
            #Get value at 2nd column
            # value = self.model.get_value(treeiter, 1)
            
            #for row in self.temp_index:
                #print(row).strip("\n")
            
        category_checker()
        
        
    def on_iconview_key_press_event(self, widget, event):
        to_remove = []
        cats = {48: 0, 49: 1, 50: 2, 51: 3, 52: 4, 53: 5, 54: 6, 55: 7, 56: 8, 57: 9} # the larger number is the keyval equvilent to the smaller number
        #What do cats use to make coffee? A purrcolator! XD 
        
        if event.keyval in cats:
            print("Key {0} has been pressed".format(cats[event.keyval]))
            
            for row in (self.temp_index):
                row_elements = row.split(",")

                for each in self.thumb_view.get_selected_items():
                    path = gtk.TreePath(each) # thumb position (numeric value) within the gallery view
                    treeiter = self.model.get_iter(path)
                    value = self.model.get_value(treeiter, 1) # thumbnail path

                    if value == row_elements[1] and row_elements[3] == "0":
                        print("match found")
                        print(row)
                        to_remove.append(row) #takes a snaptshot of the row, adds to to_remove list for iteration and removal from self.temp_index later
                        rep_str = (row)
                        rep_str = rep_str.split(",") # prepares original row for category replacement
                        new_str_seq = (rep_str[0],rep_str[1],rep_str[2],str(cats[event.keyval]))
                        rep_str = ",".join(new_str_seq)
                        print(rep_str)
                        self.temp_index.append(rep_str)
                    
            for row in self.temp_index[:]:
                row_elements = row.split(",")
                for each in to_remove:
                    if each == row:
                        self.temp_index.remove(row)
                        print("row removed")
            print("temp index updated")
            to_remove[:] = []
            self.model.clear()
            
            print("Building new thumbs!") # This takes too long, probably overwriting existing thumbs if present... sort this
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            for line in self.temp_index[:40]:
                attribute = (line.split(","))
                thumb_loc = attribute[1]
                file_loc = attribute[2]
                category = attribute[3]
                #if category == '0' and os.path.isfile(thumb_loc) == False: # !!!RESEARCH REQUIRED TO LOAD EXISTING FILE
                    #print("thumb does not exist")
                dir_parser.thumbs_generator(file_loc, thumb_loc)
                pixbuf = Pixbuf.new_from_file(thumb_loc)
                pixbuf = pixbuf.scale_simple(self.desired_width, self.desired_height, GdkPixbuf.InterpType.HYPER)
                self.model.append([pixbuf, thumb_loc])
                #else:
                    #pixbuf = pixbuf.scale_simple(self.desired_width, self.desired_height, GdkPixbuf.InterpType.HYPER)
                    #self.model.append(thumb_loc) # testing
            print("new thumbs created!")
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                
        

if __name__ == "__main__":
    main = image()
    gtk.main()

	
	        # print("creating thumbs for gallery view...")
        # print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        # partial_harvester = partial(initial_thumbs_load,selection=self.selection,width=self.desired_width,height=self.desired_height)
        # pool = ThreadPool(3)
        #pool = multiprocessing.Semaphore(multiprocessing.cpu_count()) 
        # image_list = pool.map(partial_harvester, self.temp_index[:40])
        # pool.close()
        # pool.join()
        
        # for item in image_list:
            #print(item)
            # self.model.append(item)
        
        # print("Finished creating thumbs!")
        # print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))