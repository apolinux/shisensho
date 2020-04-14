from log import log

class matchTiles:
    """
    Find if position of pair tiles are valid
    """
    def __init__(self):
        self.valid_path = None
        self.current_board = None
    
    def positionMatch(self,tile1,tile2,current_board):
        """
        algorithm to validate if two positions in board
        are valid according to Shisen-Sho Rules
        
        Two positions in board are valid if:
        The tiles are the same and
        There is a path between both with 3 segments at most 
        the segments must be horizontally or vertically
        
        The validation process can be like that:
        
        given position1: x1,y1 and position2: x2,y2
        board limits: upper left(1,1) and lower right(cols,rows)
        first, sweep vertically:
         
         (0,0)
                (1,1)
                         D (y2,xm) ---- pos2 (x2,y2)
                                   |         |
                                   |         |
               A (x1,ym)--------------------- B (x2,ym)           
                       |           |
                       |           |   
               pos1 (x1,y1)--------- C (y1,xm)
                   
                                              (cols-1,rows-1)
                                                            (cols,rows )
                                    
        using a segment between x1 and x2 and moving over y axis between
         0 and rows , the path should be:
         
         1. pos1-A 
         2. A-B
         3. B-pos2
         
         second, sweep horizontally
         Using a segment between y1 and y2 and moving over x axis between 0
         and cols , the path should be:
         
         1. pos1-C
         2. C-D
         3. D-pos2
         
         When there is a free path, it means without tiles in between, the match
         is valid
        
        Special cases:
        - The tiles are next each other. It means either x1=x2 and y2=y1 +/- 1 or y1=y2 and x2= x1 +/- 1
        In this case its valid the match
        
        - The tiles are aligned over y or x axis. It means x1=x2 or y1=y2. In this case the path is only one
        and only is necessary to validate the free path
        
        """
        
        # first group, sweep vertically
        """(x1,y1) = position1
        (x2,y2) = position2
        for ym in range(0,rows +1):
            posA = (x1,ym)
            posB = (x2,ym)
            path_list = []
            path_list[0] = (position1,posA)
            path_list[1] = (posA,posB)
            path_list[2] = (posB,position2)
            
            for path in path_list :
                valid = self.validateFreePath(path,current_board)
                if valid:
                    return True
        
        for xm in range(0,cols +1):
            posC = (y1,xm)
            posD = (y2,xm)
            path_list = []
            path_list[0] = (position1,posC)
            path_list[1] = (posC,posD)
            path_list[2] = (posD,position2)
            
            for path in path_list :
                valid = self.validateFreePath(path,current_board)
                if valid:
                    return True        
           """
        self.current_board = current_board
        (cols,rows) = current_board.dimension   
        #print("cols:",cols,'rows:',rows)
        return (
            self.sweepOnDirection(tile1,tile2,'v',-1,rows)   
            or
            self.sweepOnDirection(tile1,tile2,'h',-1,cols)   
        )
        
                
            
    def sweepOnDirection(self,tile1,tile2,sweep,lim_inf,lim_sup):
        """
        sweep : order of sweep. "v" : vertically, "h" : horizontally
        """
        
        (x1,y1) = position1 = tile1.position
        (x2,y2) = position2 = tile2.position
        
        for coordm in range(lim_inf,lim_sup + 1):
            if sweep == 'v':
               posR = (x1,coordm)
               posQ = (x2,coordm) 
            else:
                posR = (coordm,y1)
                posQ = (coordm,y2)
            path_list = [None]*3
            path_list[0] = (position1,posR)
            path_list[1] = (posR,posQ)
            path_list[2] = (posQ,position2)
            
            valid = True 
            for path in path_list :
                #print("sweepondirection position1: %s, position2:%s pathlist: %s, path: %s,sweep:%s coordm: %s posR:%s \
                #posQ:%s, range: %s"  
                # %(position1,position2,path_list,path,sweep,coordm,posR,posQ,(lim_inf,lim_sup)))
                valid = (valid and self.validateFreePath(path,position1,position2,))
            if  valid:
                log.save('ruta valida: %s' % (path_list) )
                self.valid_path = path_list
                return True
                
        return False
    
    def validateFreePath(self,path,exclude_pos1,exclude_pos2):
        """
        validates if path is free of tiles
        """
        (position1,position2) = path
        
        (x1,y1) = position1
        (x2,y2) = position2
        
        if (x1 == x2) and (y1 != y2) :
            fixed_coord=x1
            varcoord1=y1
            varcoord2=y2
            fixed_coord_name='x1'
        elif (y1 == y2) and (x1 != x2):
            fixed_coord=y1
            varcoord1=x1
            varcoord2=x2
            fixed_coord_name='x2'
        elif (x1 == x2) and (y1 == y2):
            return True
        else:
            raise Exception('The path is neither x axis or y axis')
        
        # determine if is forward or backward
        factor = (1 if (varcoord1 < varcoord2) else -1)
        # sweep on coordinates
        for varcoordm in range(varcoord1,varcoord2 + 1*factor, factor ):
            
            try:
                if fixed_coord_name == 'x1':
                    # sweep rows
                    cur_pos = (fixed_coord,varcoordm)
                else:
                    # fixec_coord = y1
                    # sweep cols
                    cur_pos = (varcoordm,fixed_coord)
                #print ("pos1: %s, pos2:%s,cur pos:%s range:%s fixed coord: %s"
                #% (position1,position2,cur_pos,(varcoord1,varcoord2), 'x1' if (fixed_coord == x1) else 'y1'))    
                (board_cols,board_rows) = self.current_board.dimension
                if (varcoordm == -1)  or (fixed_coord == -1) \
                   or (cur_pos[0] ==  board_cols) or (cur_pos[1] == board_rows):
                    # positions outside usable tile board
                    raise TilePositionException(cur_pos) 
                    
                # exclude start and end points
                if ( cur_pos == exclude_pos1) or ( cur_pos == exclude_pos2) :
                    #print ("excluded:",)
                    raise TilePositionException(cur_pos) 
                    
                current_tile=self.current_board.tiles[ cur_pos[1] ][ cur_pos[0] ]

                #print('validatefreepath:pos: %s, current tile: %s, status:%s' 
                #    % (current_tile.position, current_tile.name,current_tile.status))

                if current_tile.status != 'free':
                    return False
            except TilePositionException as e:
                #print("tile excluded:%s" % (e))
                continue
        return True
    
class TilePositionException(BaseException):
    
    def __init__(self,msg = None):
        self.msg = msg