from PIL import Image
from tkinter import messagebox
import os
from configShisen import configShisen
from log import log

class tileSource:
    """
    manage the Image containing the source of tiles
    """
    def __init__(self,filename):
        self.filename = filename
        self.size = None
        self.image = None
        # size of individual tile on image
        self.tilesize = None
        # defines cols and rows number of image
        self.dim = 9 , 5
        
        self.load()
        
        
    def load(self):
        filename1 = configShisen.getAbsPath(self.filename)
        if not os.path.isfile(filename1):
            #raise FileNotFoundError('The file "' + file_tiles +'" is not valid')
            # dialog box
            d= messagebox.showwarning(
                "Open file",
                "Cannot open this file\n(%s)" % filename1
            )
            exit(1)
        self.image = Image.open(filename1)
        
        image_width ,image_height = self.image.size
        log.save('tilesource load, img size:' +str(self.image.size))
        
        if ( image_width % self.dim[0] != 0 ) or ( image_height % self.dim[1] != 0):
            d= messagebox.showwarning(
                "Image size",
                "The image (%s) can't be splitted in integer tile size" % self.filename
            )
            exit(1)
        
        # get tile size
        self.tilesize = image_width // self.dim[0] , image_height // self.dim[1]
        
        log.save('tilesource load, tilesize:' + str(self.tilesize))
        