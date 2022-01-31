#Great Game of Britain

#Imports
from tkinter import *
from PIL import ImageTk,Image
from BoardSelector import BoardSelector
import random

#Map container class
class BoardFrame(Frame):
    def __init__(self,master):
        super(BoardFrame,self).__init__(master)
        self.pack(expand=True,fill=BOTH,side=LEFT)


#Map Class
class Board(Canvas):
    def __init__(self,frame,b,size,startnode):
        #Loads widgets in frame
        super(Board,self).__init__(frame,height=750,width=750,background='white',
                                 scrollregion=(0,0,size[0],size[1]))
        self.createScrollbar(frame)
        self.image=Image.open(b+"/map.png")
        self.boardimage=ImageTk.PhotoImage(self.image)
        self.background=self.create_image(0,0,image=self.boardimage,anchor=NW)

        #Loads necessary colors
        self.colordict={"r":"#dd0000","b":"#000000","p":"#db69b3"}
        self.color="r"

        #Binds key/button presses in frame
        self.tag_bind("node","<ButtonPress-1>",self.selectNode)
        self.tag_bind("player","<ButtonPress-1>",self.selectPlayer)
        self.bind("<ButtonPress-1>", self.scrollStart)
        self.bind("<B1-Motion>", self.scrollMove)

        #Builds network
        self.nodes=[]
        self.network=Network(b+"/network.txt")
        self.drawNetwork()

        #Adds players
        self.createPlayers(startnode)
        self.drawPlayers()
        self.playerselected=""

        #Moves scrollbars into centre
        (x,y)=self.network.lookupCoords(startnode)
        self.xview_moveto((x-375)/int(size[0]))
        self.yview_moveto((y-375)/int(size[1]))

        #Places frame canvas on frame                
        self.pack(side=LEFT,expand=True,fill=BOTH)

    def scrollStart(self, event):
        self.scan_mark(event.x, event.y)

    def scrollMove(self, event):
        self.scan_dragto(event.x, event.y, gain=1)

    def createScrollbar(self,frame):
        hbar=Scrollbar(frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.xview)
        vbar=Scrollbar(frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.yview)
        self.config(width=750,height=750)
        self.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

    def selectNode(self,event):
        #self.itemconfig(self.selected,fill=self.playerselected.getCol())
        selected=event.widget.find_closest(self.canvasx(event.x),self.canvasy(event.y))[0]
        #print(self.network.lookupCoords(self.lookupRef(selected)))
        if self.playerselected!="":
            self.playerselected.setPosition(self.lookupRef(selected))
            self.drawPlayers()
        self.playerselected=""

    def selectPlayer(self,event):
        self.selected=event.widget.find_closest(self.canvasx(event.x),self.canvasy(event.y))[0]
        for player in self.players:
            if self.selected==player.getRef():
                self.playerselected=player
                self.itemconfig(self.selected,fill=self.playerselected.getDark())
                return

    def addEdge(self,xend,yend,col,xstart=0,ystart=0):
        destination=self.find_closest(xend,yend)[0]
        start=self.find_closest(xstart,ystart)[0]
        self.create_line(self.pmean(self.coords(start)),self.pmean(self.coords(destination)),fill=self.colordict[col],width=4)
        self.tag_raise("node")
        self.tag_raise("text")

    def createNode(self,x,y,name=""):
        if name=="":
            p=self.create_oval(x-9,y-9,x+9,y+9,fill="black",tags="node")
        
        elif name[0]=="#":
            p=self.create_oval(x-9,y-9,x+9,y+9,fill="black",tags="node")
            self.create_text(x+12,y-2,text=name[1:].upper(),anchor=W,font="Ariel 8 bold",tags="text")

        elif name[0]=="*":
            p=self.create_rectangle(x-12,y-12,x+12,y+12,fill="black",tags="node")
            self.create_text(x+16,y,text=name[1:].upper(),anchor=W,font="Ariel 12 bold",tags="text")

        else:
            p=self.create_polygon(x,y-18,x-15,y+9,x+15,y+9,fill="black",
                             tags="node")
            self.create_text(x+14,y-2,text=name.upper(),anchor=W,font="Ariel 10 bold",tags="text")
            #print(name.title(),end='","')
        self.nodes.append([p,len(self.nodes)])

    def pmean(self,points):
        return (int(2*sum(points[::2])/len(points)),int(2*sum(points[1::2])/len(points)))

    def drawNetwork(self):
        for node in self.network.getNodes():
            self.createNode(int(node[0]),int(node[1]),node[2])
        for edge in self.network.getEdges():
            self.addEdge(int(edge[0]),int(edge[1]),edge[2],int(edge[3]),int(edge[4]))

    def createPlayers(self,startnode):
        (x1,y1)=self.network.lookupCoords(startnode)
        p1=self.create_oval(x1-30,y1-9,x1-12,y1+9,fill="#0000cc",tags="player")
        p2=self.create_oval(x1+30,y1-9,x1+12,y1+9,fill="#00cc00",tags="player")
        player1=Player(startnode,p1,"#0000cc",-21,"#000077",12)
        player2=Player(startnode,p2,"#00cc00",21,"#007700",12)
        self.players=[player1,player2]        
        for n in range(0,4):
            c=self.create_oval(x1-30,y1-9,x1-12,y1+9,fill="#999999",tags="counter")
            counter=Player(startnode,c,"#999999",0,"#555555",20)
            self.players.append(counter)

    def drawPlayers(self):
        for player in self.players:
            self.delete(player.getRef())
            (x,y)=self.network.lookupCoords(player.getPosition())
            r=player.getRadius()
            p=self.create_oval(x+player.getOffset()-r,y-r,x+player.getOffset()+r,y+r,fill=player.getCol(),tags="player")
            player.setRef(p)

    #Returns the canvas id given some network index
    def lookupItem(self,n):
        for node in self.nodes:
            if node[1]==n:
                return node[0]

    #Returns the network index given some canvas id
    def lookupRef(self,ref):
        for node in self.nodes:
            if node[0]==ref:
                return node[1]



#Network class
class Network(object):
    def __init__(self,file):
        self.network = []
        self.loadNetwork(file)

    def loadNetwork(self,file):
        raw = open(file,"r")
        lines = raw.readlines()
        for line in lines:
            self.network.append(line.strip().split("|"))
        raw.close()

    def getNodes(self):
        return [n[-1].split(",") for n in self.network]

    def getEdges(self):
        edges=[]
        l=len(self.network)
        for i in range(0,l):
            for j in range(0,i):
                if self.network[i][j]!="-":
                    start=self.network[i][l].split(",")
                    end=self.network[j][l].split(",")
                    edges.append((start[0],start[1],self.network[i][j],end[0],end[1]))
        return edges

    def getDestinations(self):
        l=len(self.network)
        destinations=[]
        for i in range(0,l):
            if self.network[i][l].split(",")[2]!="" and self.network[i][l].split(",")[2][0]!="*":
                destinations.append((i,self.network[i][l].split(",")[2]))
                #print(self.network[i][l].split(",")[2])
        return destinations

    def lookupCoords(self,i):
        return [int(j) for j in self.network[int(i)][len(self.network)].split(",")[:2]]
                
        


#Player Class
class Player(object):
    def __init__(self,node,ref,col,offset,dark,radius):
        self.position=node
        self.ref=ref
        self.col=col
        self.offset=offset
        self.dark=dark
        self.radius=radius

    def getPosition(self):
        return self.position

    def getRef(self):
        return self.ref

    def setPosition(self,node):
        self.position=node

    def setRef(self,ref):
        self.ref=ref

    def getCol(self):
        return self.col

    def getOffset(self):
        return self.offset

    def getDark(self):
        return self.dark

    def getRadius(self):
        return self.radius


#Choose which map to play
root=Tk()
root.title("Select Board")
bs=BoardSelector(root)
root.mainloop()

b=bs.getboard()
meta=open(b+"/meta.txt","r")
(size,startnode)=meta.read().split(",")
meta.close()
#print(size,startnode)

root=Tk()
root.title("The Great Game of "+b.capitalize())
bf=BoardFrame(root)
board=Board(bf,b,size.split("x"),startnode)

##root.update()
##f=open("test.eps","w")
##ps = board.postscript(colormode='color')
##f.write(ps)
##f.close()
        
root.mainloop()
