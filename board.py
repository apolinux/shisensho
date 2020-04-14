from tkinter import Frame,Canvas,NW,N,S,SUNKEN,ALL,Message,CENTER
from tkinter import messagebox
from PIL import Image,ImageTk
import math
import time
import random
import os.path
from os import listdir
from os.path import isfile, join
from matrixTile import matrixTile
from configShisen import configShisen
from tileboard import tileboard
from boardEvent import boardEvent
from matchTiles import matchTiles
from log import log

class board:
    """
    manipulates tiles on board game
    """
    
    def __init__(self,window,tile_source,dimension,size):
        self.window = window
        # size of canvas width,height in pixels
        self.size = size
        # size of base canvas, can't be modified
        self.basesize = size
        # dimension in row x cols
        self.dimension = dimension
        #self.tiles_image = None
        self.tile_source = tile_source
        self.canvas = None
        self.offset_size = None
        self.limits = None
        self.tiles = None
        self.msg_frame = None
        
        # two tiles that match
        self.clue = None
        self.background_file = configShisen.load('background-file')
        #self.background_file = 'wallpaper1.jpg'
        self.status = 'run'
        
    def changeSize(self,dim):     
        log.save('in changesize, new dim:' + str(dim))
        self.dimension = dim
        self.load()
        
    def load(self):
        """
        load board on window
        """
        # initialize timer
        self.window.onStartGame()
        
        log.save("loading board")
        # create matrixtile object
        matrix_tile = matrixTile(self.dimension)
        self.matrix_tile = matrix_tile
        
        log.save('canvas size' + str(self.size))
        
        new_tile_size= board.getTileSize(self.basesize,self.tile_source.tilesize, self.dimension)
        log.save('new tile size' + str(new_tile_size))
        self.tile_size = new_tile_size
        #define offset size
        self.offset_size = new_tile_size
        
        # create matrix of gameboard
        (dimx,dimy) = self.dimension
        matrix_board = [[ None for x in range(dimx)] for x in range(dimy)]
        
        # adjust size to tile_width * (cols + 2)
        self.size = (self.tile_size[0] *(self.dimension[0] + 2), self.size[1] )
        log.save('new board size' + str(self.size))
        # write image to canvas
        self.loadBoardToImage()
        self.canvas.delete(self.msg_frame)
        # load tiles in new image
        row_count=0
        for tile_row in matrix_tile.matrix_board:
            col_count=0
            for tilename in tile_row:
                position = (col_count,row_count)
                tile_board = self.drawTile(matrix_tile, new_tile_size,position,tilename)
                matrix_board[row_count][col_count] = tile_board
                col_count +=1
            row_count +=1    
        self.tiles = matrix_board    
        # save last box position    
        self.last_box = tile_board.box
        
        #define board limits of clickable area 
        self.limits = ((self.offset_size),(tile_board.box[2],tile_board.box[3]))
        
        # validate if board is solvable
        self.checkSolvable()
        
        log.save("loading board done")
    
    #def getTileSize(matrix_tile):
    def getTileSize(board_size,tile_size, dimension):
        """
        calculates the new size based on formula:
        given:
          bw = board width
          bh = board height
          tw = tile width
          th = tile height
          
          Tr = tile relative size = tw / th
          ntw = number of tiles horizontally
          nth = number of tiles vertically
          
          twb = tile width depending of board = bw /( ntw + 2)
          thb = tile height depending of board = bh /( nth + 2)
          
          thrb = tile height relative to tile width = twb / Tr
          fth = final tile height = minor(thrb , thb)
          ftw = final tile width = Tr * fth
        """
        
        #tiles=matrix_tile.matrix_board
        #rows = len(tiles)
        #cols = len(tiles[0])
        
        (bw,bh) = board_size
        (tw,th) = tile_size
        (ntw, nth) = dimension
        
        tr = tw /th
        
        twb = bw / (ntw + 2)
        thb = bh / (nth + 2)
        
        thrb = twb / tr
        fth = math.ceil(board.minor(thrb, thb))
        ftw = math.ceil(tr * fth)
        
        return (ftw,fth) 
    
    #def drawTile(self,tile_board,matrix_tile,new_size,offset_size):
    def drawTile(self, matrix_tile, new_size,position, tilename):
        """
        Draw a Tile of certain type in certain position
        get the token piece from some graphic tile group
        and put on certain position in graphic board
        """
        
        (wt,ht) = self.tile_source.tilesize
        
        (row_tile_base,col_tile_base) = matrix_tile.getPosTile(tilename)
        x1 = col_tile_base * wt
        y1 = row_tile_base * ht
        # cut piece of tiles image
        box_tiles = (x1 , y1 , x1 + wt , y1 + ht)
        region = self.tile_source.image.crop(box_tiles)
        
        # resize 
        new_region = region.resize(size=new_size, resample=Image.BICUBIC)
        
        # paste tile on image board
        box_board = self.getBoxPosition(position,new_size,self.offset_size)
       
        new_region_tk = ImageTk.PhotoImage(new_region)
        canvasref = self.canvas.create_image(box_board[0],box_board[1],image=new_region_tk,anchor=NW)
        
        tile_board = tileboard(position=position,name=tilename)
        tile_board.box  = box_board
        tile_board.canvasref = canvasref #imagebox
        tile_board.imageboxtk = new_region_tk
        tile_board.imagebox = new_region
                
        return tile_board
    
    
    def getBoxPosition(self,position,size,offset):
        (new_width,new_height) = size
        (col_count,row_count) = position
        (width_offset,height_offset) = offset
        box_board = (col_count * new_width + width_offset, row_count * new_height + height_offset,
            col_count * new_width + new_width + width_offset, row_count * new_height + new_height + height_offset)
        
        return box_board
    
    def minor(a,b):
        if(a < b):
            return a
        else :
            return b
        
    def loadBoardToImage(self):
        """
        create an Image Tk object, save Image into it and 
        save ImageTk object into label as image, this is the final frame
        """
        # create a blank image object
        #self.board_image = Image.new("RGB",size=self.size,color=(255,255,255))
        #self.board_image = Image.open(self.background_file)
        self.board_image = Image.open(self.getBackgroundFile())
        imagetk=ImageTk.PhotoImage(image=self.board_image)
        self.imagetk=imagetk
        if self.canvas is None:
            log.save('label image is none')
            self.canvas = Canvas(self.window.root,width=self.size[0],height=self.size[1])
            
            #self.canvas = Canvas(self.window.root,width=canvas_width,height=canvas_height)
            self.canvas.create_image((0,0), image=self.imagetk,anchor=NW)
            
        else:
            self.canvas.delete(ALL)
        # bind click events to board Event
        board_event = boardEvent(self)    
        self.canvas.bind("<Button-1>",board_event.clickOnCanvas)
        # this let save image reference    
        self.image_on_canvas = self.canvas.create_image((0,0), image=self.imagetk,anchor=NW)
        self.canvas.itemconfig(self.image_on_canvas, image = self.imagetk)
        
        # grid once
        self.canvas.grid(sticky=N+S) 
        
    def getBackgroundFile(self):
        """
        obtain a background image
        """
        # image dir
        mypath= configShisen.getAbsPath("wallpapers")

        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        
        file =random.choice(onlyfiles)
        
        return configShisen.getAbsPath("wallpapers/" + file)
        
    def setStatusTile(self,tile,status):
        position = tile.position
        self.tiles[position[1]][position[0]].status = status
        
    def getTileFromPos(self,position):
        """
        get current tile from position in game board
        """
        (col,row) = position
        (board_cols,board_rows) = self.dimension
        
        if ( col == -1 ) or ( col >= board_cols ) \
            or ( row == -1 ) or ( row >= board_rows ) :
                tile= self.getTileFromPosWithExceptions(position)
        else :
            tile = self.tiles[row][col]
        
        return tile
        
    def getTileFromPosWithExceptions(self,position):
        
        """
        get current tile from position in game board
        and manage exceptions
        a position outside board tiles exists if
        colpos < 0 or rowpos < 0 or colpos >= board_cols or rowpos >= board_rows
        
        given: (x1,y1) upper left position and (x2,y2) right bottom position of box
        given: (xl,yl) lower right corner of lower right tile in board
        if colpos = -1 => x1 = 0 and x2 = x1 + tile_width
        if rowpos = -1 => y1 = 0 and y2 = y1 + tile_height
        if colpos >= board_cols => x1 = xl , x2 = x1 + tile_width
        if rowpos >= board_rows => y1 = yl , y2 = y1 + tile_height
        """
        # manage exceptions
        (col,row) = position
        (board_cols,board_rows) = self.dimension
        (tile_width,tile_height) = self.tile_size
        # get last tile
        last_tile = self.tiles[board_rows - 1][board_cols - 1]
        (xnp,ynp,xl,yl) = last_tile.box
        
        x1=y1=None
        
        if col == -1 :
            x1 = 0 
        elif col >= board_cols:
            x1 = xl    
        
        if row == -1 :
            y1 = 0
        elif row >= board_rows:
            y1 = yl
        
        if x1 is None:
            x1 = (col + 1) * tile_width
        
        if y1 is None:
            y1 = (row + 1) * tile_height
        
        x2 = x1 + tile_width
        y2 = y1 + tile_height
        
        box = (x1,y1,x2,y2)
        
        tile = tileboard(name='',position=position)
        tile.box = box
        
        return tile
    
    def checkWin(self):
        """
        check if all tiles are in status "free"
        """
        for rows in self.tiles:
            for tile in rows:
                if tile.status != "free":
                    return False
        # no tiles free, you won!        
        self.endGame('You Won!!!')
        return True
    
    def checkSolvable(self):
        """
        if game is not solvable, then block
        sweep board of tiles and order in array indexing by tilename
        then sweep that array and look for two similar tiles that match
        """
        tilelist={}
        for rows in self.tiles:
            for tile in rows:
                if tile.status == 'busy':
                    if not tile.name in tilelist:
                        tilelist[tile.name] = []
                    tilelist[tile.name].append(tile)
        
        match_tiles = matchTiles()
        
        for tilename, tilelistsame in tilelist.items():
            for tile1 in tilelistsame:
                for tile2 in tilelistsame:
                    if tile1 != tile2:
                        if match_tiles.positionMatch(tile1,tile2,self):
                            #self.valid_path = match_tiles.valid_path
                            self.clue = tile1,tile2
                            return True
                        
        # there is not pair of tiles matching a valid position, then block game
        self.endGame('Game Blocked')
        
    def endGame(self,message):    
        self.__showMessage(message,self.reload)
        
        # disable clue
        self.window.onEndGame()
        
    def __showMessage(self,message,action=None):                    
        frame=Frame(height=200, width=200, bd=1, relief=SUNKEN)
        frame.grid()
        w = Message(frame, text=message)
        w.config(bg='lightgreen', font=('times',24,'bold'))
        w.bind('<Button-1>',action)
        w.grid()

        centerxc = math.ceil(self.size[0] / 2)
        centeryc = math.ceil(self.size[1] / 2)
        self.msg_frame = self.canvas.create_window(centerxc,centeryc,window=frame,anchor=CENTER)
        
    def showMessageTest(self):
        self.endGame('hola a todos esto es un test!!!')
    
    def reload(self,event):
        #self.canvas.unbind('<Button-1>')
        log.save('loading board again')
        
        self.load()
        
    def showClue(self):
        """
        show the last valid path found with checksolvable
        use the path and show it
        """
        self.checkSolvable()
        # get last path
        tile1,tile2 = self.clue
        
        # hightlight tiles
        tile1.twinkle(5,False)
        tile2.twinkle(5,False)
        
    def pause(self):
        if self.status == 'run' :
            self.status = 'paused'
            #self.window.pauseClock(True)
            self.window.onPauseGame()
            self.__showMessage('paused',self.onEndPause)
        else:
            self.onEndPause()
            
    def onEndPause(self,event=None):
        #self.window.pauseClock(False)
        self.window.onEndPause()
        self.canvas.delete(self.msg_frame)
        self.status = 'run'
