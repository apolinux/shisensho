from configShisen import configShisen
from shisenException import shisenException

import random

class matrixTile:
    """
    manage resolving algorithms to validate for example
    if game could be won or if a movement is valid in rules game.
    Changed by:
    
    Manage the matrix of tiles used to fill the board
    """
    def __init__(self,dim):
        # define matrix 9x5 of tiles in "tiles-unicode.gif" image file
        self.tiles_matrix = configShisen.load('tiles-matrix')
        self.tiles_list = {}
        self.matrix_board= None
        # initialize positions
        self.initTilesPos()
        # crate random matrix 
        self.createMatrix(dim)
    
    def initTilesPos(self):
        self.tiles_list = {}
        row_count = 0
        for row in self.tiles_matrix:
            col_count=0
            for tile in row:
                self.tiles_list[tile] = (row_count,col_count)
                col_count += 1
            row_count += 1
    
    def getPosTile(self,tilename):
        """
        get position of current tilename
        """
        return self.tiles_list[tilename]
    
    def getTilePos(self,position):
        return self.tiles_matrix[position[1]][position[0]]
    
    def createMatrix(self,dim,shuffle=True):
        """
        Create the matrix of positions and tiles type
        picking random items of the matrix tile
        """
        (dimx,dimy) = dim
        # create empty matrix with input dimentions
        # this setting does not work because the referenced address of the rows are repeated, 
        # and if it's assigned a[0][3], is assigned to all a[x][3]: a[0][3], a[1][3] ...
        #matrix = [[None] * dim['posx']] * dim['posy']
        matrix = [[ None for x in range(dimx)] for x in range(dimy)]
        list_avail = []
        for posx in range(1,dimy+1):
            for posy in range(1,dimx+1):
                list_avail.append([posx - 1,posy - 1])
        
        # shuffle order in array that have matrix positions
        if shuffle:
            random.shuffle(list_avail)
        
        # get list of items to add to logic matrix
        subgroup_list = self.getSubgroup(dim) #(dim[x] * dim[y]) / 2)
        
        item=0
        for item_rand in list_avail:
            x_t=item_rand[0]
            y_t=item_rand[1]
            # get position in matrix base
            matrix[x_t][y_t] = subgroup_list[item]
            item += 1
            
        self.matrix_board = matrix
    
    def getSubgroup(self,dim):
        """
        Get a subgroup list of matrix logic of image containing tiles
        the size of list is the same as dim.x * dim.y
        but the unique tiles are a quarter of this size, it means each tile appears four times
        """
        list_size = dim[0] * dim[1]
        
        # load config
        tiles = configShisen.load('tiles')
        
        for item in tiles :
            dimitem= item['dim']
            
            if dimitem[0] * dimitem[1] == list_size :
                list_uniq = item['list']
                # multiplier = list_size / len(list_uniq
                list = list_uniq * (list_size // len(list_uniq)) 
                break
        else:
            raise ShisenException("The size '" + str(list_size) + "' of board is not configured in config file")
        
        
        
        return list
    