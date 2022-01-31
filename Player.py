#GGOB Player Window

#Imports
from tkinter import *
from PIL import ImageTk,Image
from tkinter import simpledialog
from BoardSelector import BoardandSeedSelector
import random

#Widgets container class
class WidgetFrame(Frame):
    def __init__(self,master,destinations,hazards):
        super(WidgetFrame,self).__init__(master)
        self.root=root
        self.hazards=hazards
        self.pack(side=RIGHT,fill=Y,padx=20,pady=20)
        self.createWidgets(destinations,master)

    #Creates all the widgets on the GUI
    def createWidgets(self,destinations,master):

        #Text regarding destinations
        destinationsframe=Frame(self)
        destinationsframe.pack(side=LEFT)
        Label(destinationsframe,font="Ariel 16 bold",text="DESTINATIONS").grid(row=0,column=0,columnspan=2)
        self.destinationlist=[]
        self.unticked=ImageTk.PhotoImage(Image.open("assets/unticked.png"))
        self.ticked=ImageTk.PhotoImage(Image.open("assets/ticked.png"))

        #Destinations and adjacent tickboxes
        for n in range(0,6):
            l=Label(destinationsframe,font="Ariel 16 bold",text=destinations[n],fg="#0000ff",anchor=W)
            l.grid(row=1+n,column=0)
            Checkbutton(destinationsframe,indicatoron=False,image=self.unticked,selectimage=self.ticked).grid(row=1+n,column=1)
            self.destinationlist.append([destinations[n],l])

        #Window management stuff
        sideframe=Frame(self)
        sideframe.pack(side=LEFT,padx=(20,10),pady=10)
        dieframe=Frame(sideframe)
        dieframe.pack(side=TOP,pady=(0,10))

        #Creates die
        Label(dieframe,font="Ariel 16 bold",text="ROLL").pack(side=LEFT)
        self.die=Die(dieframe,self.roll)
        self.die.pack(side=RIGHT,padx=(10,0))
        self.die.set(5)

        #Creates hazard box and button
        self.displayedHazard=StringVar()
        self.hazardimage=ImageTk.PhotoImage(Image.open("assets/hazardbutton.png").resize((128,41)))
        Label(sideframe,textvariable=self.displayedHazard,wraplength=150,
              font="Ariel 12 bold").pack(side=BOTTOM)
        Button(sideframe,command=self.hazard,text="Hazard",
               image=self.hazardimage).pack(side=BOTTOM,pady=10)


    #Generates random roll sequence when die is clicked
    def roll(self):
        for n in range(24,3,-1):
            self.root.after(int(1000/n))
            self.die.set(random.randint(1,6))
            self.root.update()

    #Generates random hazard when hazard is clicked
    def hazard(self):
        self.displayedHazard.set("*LOADING*")
        self.root.update()
        self.root.after(500)
        self.displayedHazard.set(random.choice(self.hazards))

#Die Class
class Die(Button):
    def __init__(self,master,c):
        super(Die,self).__init__(master)

        #Loads images - here c is the .roll command of the WidgetFrame object
        self.images=[]
        self.config(command=c)
        for n in range(0,6):
            self.i=ImageTk.PhotoImage(Image.open("assets/die"+str(n+1)+".png"))
            self.images.append(self.i)

    #Sets die to specified value
    def set(self,n):
        self.config(image=self.images[n-1])


#Looks up seed and returns 6 destinations (/37-1234 is arbitraty encoding)
def lookupSeed(seed,destinations):
    l=[]
    for r in seed.split("-"):
        l.append((destinations[0]+destinations[1])[int(int(r)/37-1234)])
    return l

#Creates two seeds with 6 distinct random destinations (3 hard, 3 easy) (+1234*37 is arbitraty encoding)
def createSeed(destinations):
    l1=""
    l2=""
    l=[str((n+1234)*37)+"-" for n in random.sample(range(0,len(destinations[0])),6)]+[str((n+len(destinations[0])+1234)*37)+"-" for n in random.sample(range(0,len(destinations[1])),6)]

    #Gross fudge but efficient
    for n in range(0,3):
        l1+=l[n]+l[n+6]
        l2+=l[n+3]+l[n+9]
    return l1[:-1],l2[:-1]
       


#Creates window where board and seed are entered
root=Tk()
root.title("Enter Details")
bss = BoardandSeedSelector(root)
root.mainloop()

#Gets board and seed once selection window is closed
board=bss.getboard()
seed=bss.getseed()

#Loads destinations from text file
f1=open(board+"/destinations.txt")
destinations=[i.strip().split(",") for i in f1.readlines()]
f1.close()

#Loads hazard cards from text file
f2=open(board+"/hazards.txt")
hazards=[i.strip() for i in f2.readlines()]
f2.close()

#Generates seed if the seed box is left blank
if seed == "":
    (s1,s2)=createSeed(destinations)

    #Copies seed to clipboard - cheeky method of doing so
    temproot = Tk()
    temproot.withdraw()
    temproot.clipboard_clear()
    temproot.clipboard_append(s2)
    temproot.update()
    temproot.destroy()
    print(s2)
else:
    s1=seed

#Creates in game window    
root=Tk()

#Adjusts title accordingly
if board == "europe":
    root.title("The Great Game of Britain")
else:
    root.title("The Great Game of Europe")

#Creates widgets
wf=WidgetFrame(root,lookupSeed(s1,destinations),hazards)
root.mainloop()
