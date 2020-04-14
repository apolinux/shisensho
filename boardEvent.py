import math
import time
import threading
from tileboard import tileboard 
from matchTiles import matchTiles
from configShisen import configShisen
from log import log

class boardEvent:
    """
    manage the user events inside board like clicks
    """
    
    def __init__(self,gameboard):
        self.tile_selec_1st = None
        self.board = gameboard
        #self.active = True
    
    def clickOnCanvas(self,event):
        if self.board.status== 'paused':
            log.save('click disabled')
            return
        x=event.x
        y=event.y
        (x_offset,y_offset) = self.board.offset_size
        
        #print('board limits:',self.board.limits)
        (lim_width,lim_height) = self.board.limits[1]
        
        if ((x >= x_offset) and (x <= lim_width ) )\
          and ( (y >= y_offset) and (y <= lim_height ) ):
            (wtile,htile) = self.board.tile_size
            # minus 1 because of offset , must be configurable
            curr_col = math.ceil( x / wtile - 1 ) - 1
            curr_row = math.ceil( y / htile - 1 ) - 1
            position = (curr_col,curr_row)
            log.save("clicked at " + str(position) + ", ts:" + str(self.board.tile_size) + ',offset:' \
                + str(self.board.offset_size))
            tile_board = tileboard.factoryFromPosition(board=self.board,position = position)
            #tile_board.highlight()
            self.checkTile(tile_board)
    
    def checkTile(self,tileboard):
        if tileboard.status == 'free' :
            return 
        
        if self.tile_selec_1st is None :
            # no clicks made
            self.tile_selec_1st = tileboard
            tileboard.highlight(True)
            return
        else:
            if tileboard.position == self.tile_selec_1st.position :
                self.tile_selec_1st = None
                tileboard.highlight(False)
                return 
            tileboard.highlight(True)
            tile1 = self.tile_selec_1st
            tile2 = tileboard
            log.save('tiles:' + tile1.name + ',' + tile2.name)
            match_tiles = matchTiles()
            if ( tile1.name == tile2.name ) and match_tiles.positionMatch(tile1,tile2,self.board):
                # delete Tile
                self.deleteTile(tile1)
                self.deleteTile(tile2)
                
                # print path
                objects=self.printPath(match_tiles.valid_path)
                
                objects.extend([tile1.canvasref,tile2.canvasref])
                # delete path and tiles
                self.deleteObjectsTimer(objects)
                
                # check if win
                if self.board.checkWin():
                    return
                
                # validate if board is solvable
                self.board.checkSolvable()
            else:
                #unhightlight tiles
                threading.Timer(0.5, self.highlightTiles,[tile1,tile2]).start()
            self.tile_selec_1st = None    
    
    def highlightTiles(self,tile1,tile2):
        tile1.highlight(False)
        tile2.highlight(False)
            
    def deleteTile(self,tile):
        self.board.setStatusTile(tile,'free')    
        
    def printPath(self,path_list):
        """
        print the route having 3 points
        """
        points = [None]*4
        # get the pixel points
        (points[0],points[1]) = path_list[0]
        (points[1],points[2]) = path_list[1]
        (points[2],points[3]) = path_list[2]
        
        pointpix = []
        for point in points:
            tile1 = self.board.getTileFromPos(point)
            log.save("print path, tile:%s box:%s" % (tile1.name,tile1.box))
            (x1,y1,x2,y2) = tile1.box
            pointpixt = (math.ceil( (x1+x2) / 2 ) , math.ceil( (y1 + y2) / 2) )
            pointpix.append(pointpixt)
        
        # draw a line between points
        canvas = self.board.canvas
        pointpix1=pointpix[0]
        pointpix2=pointpix[1]
        pointpix3=pointpix[2]
        pointpix4=pointpix[3]
        l1 = canvas.create_line(pointpix1[0], pointpix1[1], pointpix2[0], pointpix2[1],width=5)
        l2 = canvas.create_line(pointpix2[0], pointpix2[1], pointpix3[0], pointpix3[1],width=5)
        l3 = canvas.create_line(pointpix3[0], pointpix3[1], pointpix4[0], pointpix4[1],width=5)
        
        return [l1,l2,l3]
    
    def deleteObjectsTimer(self,objects):
        delay = configShisen.load('delay-deleting')
        threading.Timer(delay, self.deleteObjects,[objects]).start()
        
    def deleteObjects(self,objects):
        log.save("en deletepath " + str(objects))
        for object in objects:
            self.board.canvas.delete(object)
        