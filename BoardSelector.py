#Board Selecting Window

#Imports
from tkinter import *
from PIL import ImageTk,Image

class BoardSelector(object):
    def __init__(self,root):
        self.root=root
        self.root.title("Select Board")

        self.addlabels()
        self.addbuttons()

    def addlabels(self):
        Label(self.root,font="Ariel 16 bold",text="Please Choose a Board").grid(row=0,column=0,columnspan=2)
        self.britainimage = ImageTk.PhotoImage(Image.open("britain/thumbnail.png").resize((128,128)))
        Label(self.root,font="Ariel 16",text="Britain").grid(row=2,column=0)
        self.europeimage = ImageTk.PhotoImage(Image.open("europe/thumbnail.png").resize((128,128)))
        Label(self.root,font="Ariel 16",text="Europe").grid(row=2,column=1)

    def addbuttons(self):
        britainbutton = Button(self.root,image=self.britainimage,command=lambda:self.submit("britain"))
        britainbutton.grid(row=1,column=0,padx=8,pady=(8,0))
        europebutton = Button(self.root,image=self.europeimage,command=lambda:self.submit("europe"))
        europebutton.grid(row=1,column=1,padx=8,pady=(8,0))    
        
    def submit(self,board):
        self.board=board
        self.root.destroy()

    def getboard(self):
        return self.board


class BoardandSeedSelector(BoardSelector):
    def __init__(self,root):
        super().__init__(root)
        self.root.bind("<Return>",self.submit)

    def addbuttons(self):
        self.britaindarkimage = ImageTk.PhotoImage(Image.open("britain/thumbnaildark.png").resize((128,128)))
        self.europedarkimage = ImageTk.PhotoImage(Image.open("europe/thumbnaildark.png").resize((128,128)))
        self.board=StringVar()
        self.board.set("britain")
        self.britainbutton = Checkbutton(self.root,image=self.britainimage,selectimage=self.britainimage,
                                         variable=self.board,onvalue="britain",offvalue="europe",indicatoron=False)
        self.britainbutton.grid(row=1,column=0,padx=8,pady=(8,0))
        self.europebutton = Checkbutton(self.root,image=self.europeimage,selectimage=self.europeimage,
                                        variable=self.board,onvalue="europe",offvalue="britain",indicatoron=False)
        self.europebutton.grid(row=1,column=1,padx=8,pady=(8,0))

        f = Frame(self.root)
        f.grid(row=3,column=0,columnspan=2)
        self.seed=StringVar()
        self.seed.set("")
        seed = Entry(f,textvar=self.seed,width=29)
        seed.grid(row=0,column=1)
        seed.focus_set()
        Label(f,font="Ariel 14 bold",text="Enter seed:").grid(row=0,column=0)
        b=Button(self.root,command=self.submit,text="SUBMIT")
        b.grid(row=4,column=0,columnspan=2,pady=8)

    def submit(self,*args):
        self.root.destroy()

    def getboard(self):
        return self.board.get()

    def getseed(self):
        return self.seed.get()
