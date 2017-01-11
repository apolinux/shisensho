from dialog import dialog
from tkinter import Message,CENTER,Frame

class about(dialog):
    def body(self,master):
        msg = Message(master, text='Implementation of the game Shisen Sho\n' +
        'By Carlos Arce\n' + 
        '@apolinux\n' +
        'apolinux@gmail.com\n' +
        '2015', justify=CENTER,width=300).grid()
        
    def onClose(self):
        self.window.pauseClock(False)
        
    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        """w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)"""

        self.bind("<Return>", self.ok)
        self.bind("<Button-1>", self.ok)
        self.bind("<Escape>", self.cancel)
        

        box.pack()
    