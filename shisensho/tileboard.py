from PIL import ImageEnhance
import threading

class tileboard:
    
    def __init__(self,name,position,size=None,board =None,box=None):
        self.size = size
        self.position = position
        self.board =board
        # name on board: "bamboo-1" ...
        self.name = name
        
        # dimensions x1,y1,x2,y2
        self.box=box
        
        # status: free or busy
        self.status='busy'
        
        # reference on canvas
        #self.imagebox = None
        self.canvasref = None
        
        # TkImage object
        self.imageboxtk=None
        
        # image object
        self.imagebox = None
        
        if not board is None:
            self.name = self.board.tiles[position[1]][position[0]]
        
        # define if highlight is on
        self.__ishl = False
            
    def factoryFromPosition(position,board):
        #tile_board = tileboard("",position,board=board)
        
        tile_board= board.tiles[position[1]][position[0]]
        return tile_board
    
    def highlight(self,status):
        if not self.imageboxtk is None:
            enh = ImageEnhance.Brightness(self.imagebox)
            
            if status:
                self.imageboxtk.paste(enh.enhance(1.5))
                self.__ishl = True
            else :
                self.imageboxtk.paste(enh.enhance(1.0))
                self.__ishl = False

    def twinkle(self,times,on=None):
        """
        blink tile
        """
        if self.imageboxtk is None:
            return
        
        if times < 1 :
            return
        
        times -= 1
        
        enh = ImageEnhance.Brightness(self.imagebox)
        #print('twinkle times', times,' on:',on)
        if on :
            self.imageboxtk.paste(enh.enhance(1.5))
        else :
            self.imageboxtk.paste(enh.enhance(1))
            
        threading.Timer(0.2,self.twinkle,[times,not(on)]).start()
        #    self.__ishl = False
        