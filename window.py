from tkinter import Tk,Menu,Frame,Label,TclError
from tkinter import messagebox
from board import board
from tileSource import tileSource
from about import about
from clock import clock
from configShisen import configShisen
from shisenException import shisenException
from log import log
import math
class window:
    """
    create a graphic window
    """
    def __init__(self):
        self.tk = None
        self.root = None
        self.widgetList = []
        self.initial_time = 0
        self.menubar = None

    def start(self): 
        """
        create widgets in window
        """
        
        self.root = Tk()
        
        try:
            # define title
            title = configShisen.load('app-title')
            version = configShisen.load('version')
            title1 = title.replace("%version%",version)
            self.root.wm_title(title1)

            self.clock = clock()
            # initial cols x rows of board
            dimension1 = configShisen.load('initial-dim')
            dimension = dimension1[0],dimension1[1]

            filename = configShisen.load('tiles-file')
            tile_source = tileSource(filename=filename)
            tilesize = tile_source.tilesize

            menu_bar_height=20
            window_title_height = 40

            relation = math.ceil( 
                ( ( dimension[0] + 2 ) *  tilesize[0]  )/ 
                ( ( dimension[1] + 2 ) *  tilesize[1]  )
                 )

            log.save('screen dim:' + str(self.root.winfo_screenwidth()) + ',' + str(self.root.winfo_screenheight()))
            window_height = math.ceil(self.root.winfo_screenheight()*0.7)
            canvas_height = window_height - (menu_bar_height + window_title_height )
            canvas_width = math.ceil(relation * canvas_height)

            window_width = canvas_width + 2

            log.save("relation:%s,window size:%sx%s" % (relation, window_width,window_height))

            # load board
            Board = board(self,tile_source,dimension,(canvas_width,canvas_height));
            Board.load()
        except shisenException as ex:
            self.showAlert(ex.msg)
            exit(1)
        
        # readjust window width
        self.root.geometry('{}x{}'.format(Board.size[0] + 2 , window_height))
        self.root.update()
        
        self.createMenu(Board)
        
        menu_inf=Frame(self.root,height=50,bd=1)
        menu_inf.grid()
        l2 = Label(menu_inf,text='time:')
        l2.grid(row=0,column=0)
        self.label_time = Label(menu_inf,text='')
        self.label_time.grid(row=0,column=1)
        self.loop()
    
    def showAlert(self,msg):    
        messagebox.showwarning('Error',msg)
        self.root.destroy()
        
    def createMenu(self,Board):
        # create the menu
        menubar = Menu(self.root)
        
        # create a pulldown menu, and add it to the menu bar
        optionsmenu = Menu(menubar, tearoff=0)
        
        tilelist = configShisen.load('tiles')
        
        for board in tilelist:
            dim = board['dim']
            dim1 = ( dim[0], dim[1] )
            optionsmenu.add_command(label= str(dim[0]) + " x " + str(dim[1]), 
                command=lambda dim_l=dim1: Board.changeSize(dim_l))
        
        menubar.add_cascade(label="Size", menu=optionsmenu)
        
        menubar.add_command(label="New", command=Board.load)
        menubar.add_command(label="Pause", command=Board.pause)
        menubar.add_command(label="Clue", command=Board.showClue)
        menubar.add_command(label="About",command=self.about)
        menubar.add_command(label="Quit", command=self.root.destroy)
        self.menubar = menubar
        self.root.config(menu=menubar)
    
    def about(self):
        # pause clock
        self.pauseClock(True)
        window = about(self,"About")
        window.open()
        
    def pauseClock(self,status):
        self.clock.pause_clock = status
    
    def options(self):
        pass
    
    def loop(self):
        self.clock.reset()
        
        self.timerTasks()
        self.root.mainloop()
        log.save('exit')
    
    def timerTasks(self):
        time=self.clock.update()
        self.label_time.configure(text = time)
        self.root.after(1000, self.timerTasks)        
    
    def onStartGame(self):
        self.clock.reset()
        self.pauseClock(False)
        if not self.menubar is None:
            self.menubar.entryconfig('Clue',state="normal")
            self.menubar.entryconfig('Pause',state="normal")
    
    def onEndGame(self):
        self.pauseClock(True)
        self.menubar.entryconfig('Clue',state="disabled")
        self.menubar.entryconfig('Pause',state="disabled")
        try:
            self.menubar.entryconfig('Paused',state="disabled")
        except TclError:
            pass
        
    def onPauseGame(self):
        self.pauseClock(True)
        self.menubar.entryconfig('Pause',label="Paused")
        
    def onEndPause(self):
        self.pauseClock(False)
        self.menubar.entryconfig('Paused',label="Pause")