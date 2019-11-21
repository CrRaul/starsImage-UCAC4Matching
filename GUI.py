
from readExcel import *
from fitsImageProcessing import *
from Ucac4Processing import *
from Operations import *
from Matching import *

import time

from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import ntpath
import cv2
import numpy as np
import math

import matplotlib
import matplotlib.pyplot as plt
import skimage.io as io
from skimage.filters import threshold_otsu
from skimage import img_as_ubyte
#"load image data"

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)   

        self.readExcel = readExcel()
        self.fitsImage = fitsImageProcessing()
        self.ucacReg = Ucac4Processing()
        self.matching = Matching()

        self.fullImageL = None
        self.fullImageR = None
     
        #reference to the master widget, which is the tk window                 
        self.master = master
        self.panelA = None
        self.panelB = None
        self.panelZ = None

        self.textL = None
        self.textR = None
        self.rezultatLabel = None
        self.rezultatLabel1 = None

        self.listBox = None

        self.sliderA = None
        self.sliderB = None

        self.init_window()

######################################################
        


######################################################    v	 
    def readExcelFile(self):
        event = 1
        filename = filedialog.askopenfilename(title='open')

        self.readExcel.readData(filename,0,31,47)

        for i in range(self.readExcel.getLenData()): 
            self.listBox.insert(END, self.readExcel.getData(i)[0]) 

    def clearListBOx(self):
        self.listBox.select_clear(0, END) # unselect allowing
                   


    def openImage(self):
        selected = self.listBox.curselection()
        if selected: # only do stuff if user made a selection
            print(self.listBox.get(selected)) # how you get the value of the selection from a listbox
            self.fitsImage.openImages("Red_20160730_Feleac/Galileo/", self.listBox.get(selected))

            im =  self.fitsImage.getImage()
            img_cv = cv2.resize(im,(im.shape[1],im.shape[0]))

            plt.ion()
            plt.imshow(img_cv)
            plt.savefig('trash/foos.png')
            plt.close()
          #  plt.close()
            im = cv2.imread("trash/foos.png",0)
            im = im[45:455, 20:590]

            self.fullImageL = im

            self.textL.configure(text = "Original image")
            self.updatePanelL()

    def starsDetection(self):
        selected = self.listBox.curselection()
        if selected: # only do stuff if user made a selection
            print(self.listBox.get(selected)) # how you get the value of the selection from a listbox
            self.fitsImage.openImages("Red_20160730_Feleac/Galileo/", self.listBox.get(selected))

            im =  self.fitsImage.getImage()
            img_cv = cv2.resize(im,(im.shape[1],im.shape[0]))

            self.fitsImage.detection()

            a = self.sliderA.get()
            self.fitsImage.sortFilterFirstNmag(a)
           # self.fitsImage.showDetection()
            sources = self.fitsImage.getSourcesDetection()
            print(sources)
            for i in range(len(sources)):
                cv2.circle(img_cv,(int(sources[i][0]),int(img_cv.shape[0]-sources[i][1])), 5, (255,255,255),-1)

            plt.ion()
            plt.imshow(img_cv)
            plt.savefig('trash/foos.png')
            plt.close()
            im = cv2.imread("trash/foos.png",0)
            im = im[45:455, 20:590]

            self.fullImageL = im

            self.textL.configure(text =   " stars:  " + str(a))
            self.updatePanelL()


    def getUcacCat(self):
        selected = self.listBox.curselection()
        if selected: # only do stuff if user made a selection
            ra = self.readExcel.getData(selected[0])[3]
            dec = self.readExcel.getData(selected[0])[4]
            
            raa = str(int(ra[0]))+"h"+str(int(ra[1]))+"m"+str(int(ra[2]))+"s"
            decc = str(int(dec[0]))+"d"+str(int(dec[1]))+"m"+str(int(dec[2]))+"s"

            self.ucacReg.readUCACregion(raa,decc,'0d23m39.7s','0d16m46.5s')

            a = self.sliderB.get()
            self.ucacReg.sortFilterFirstNmag(a)

            self.ucacReg.showCatRegRaw()

            #time.sleep(.01)
            im = cv2.imread("trash/foo.png",0)
            im = im[35:465, 20:590]
           # im = cv2.flip(im, 0)
           # im = cv2.flip(im, 1)

            self.fullImageR = im
            self.textR.configure(text = "UcacRegion-  " + "ra:  "+ raa + ";   dec:" + decc + ";  stars: " + str(a))
            self.textR.place(y=30,x=930)


            self.updatePanelR()
            print("\n\nUCAC4 - Reg\n\n")
            print(self.ucacReg.getUcacReg())


    def precessUcac(self):
        selected = self.listBox.curselection()
        if selected: # only do stuff if user made a selection
            self.ucacReg.precess(self.readExcel.getData(selected[0])[1][0])
            self.ucacReg.showCatRegRaw()

            im = cv2.imread("trash/foo.png",0)
            im = im[35:465, 20:590]

           # im = cv2.flip(im, 0)
           # im = cv2.flip(im, 1)

            self.fullImageR = im

            ra = self.readExcel.getData(selected[0])[3]
            dec = self.readExcel.getData(selected[0])[4]
            raa = str(int(ra[0]))+"h"+str(int(ra[1]))+"m"+str(int(ra[2]))+"s"
            decc = str(int(dec[0]))+"d"+str(int(dec[1]))+"m"+str(int(dec[2]))+"s"
            self.textR.configure(text = "UcacRegion-  " + "ra:  "+ raa + " dec:" + decc + "   +precession")
            self.textR.place(y=30,x=900)

            self.updatePanelR()
            print("\n\nUCAC4 - Precession\n\n")
            print(self.ucacReg.getUcacReg())

    def properMotion(self):
        selected = self.listBox.curselection()
        if selected: # only do stuff if user made a selection
            self.ucacReg.properMotion(self.readExcel.getData(selected[0])[1][0])
            self.ucacReg.showCatRegRaw()

            im = cv2.imread("trash/foo.png",0)
            im = im[35:465, 20:590]

           # im = cv2.flip(im, 0)
           # im = cv2.flip(im, 1)

            self.fullImageR = im

            ra = self.readExcel.getData(selected[0])[3]
            dec = self.readExcel.getData(selected[0])[4]
            raa = str(int(ra[0]))+"h"+str(int(ra[1]))+"m"+str(int(ra[2]))+"s"
            decc = str(int(dec[0]))+"d"+str(int(dec[1]))+"m"+str(int(dec[2]))+"s"
            self.textR.configure(text = "UcacRegion-  " + "ra:  "+ raa + " dec:" + decc + "   +precession +properMotion")
            self.textR.place(y=30,x=850)


            self.updatePanelR()
            print("\n\nUCAC4 - properMotion\n\n")
            print(self.ucacReg.getUcacReg())


##########################################################
    
    def matchingF(self):
        print("matching......")
        op = Operations()

        imStars = self.fitsImage.getSourcesDetection()
        imCat = self.ucacReg.getUcacReg()

        setA, setB = [],[]

        minRaUcac = 99999
        minDecUcac = 99999

        starC = self.ucacReg.getUcacReg()
        for i in range(0,len(starC)):
            if starC[i][0] < minRaUcac:
                minRaUcac = starC[i][0]
            if starC[i][1] < minDecUcac:
                minDecUcac = starC[i][1]


        for i in range(0,len(imStars)):
            setA.append([imStars[i][0], imStars[i][1]])
        for i in range(0,len(imCat)):
            setB.append([imCat[i][0], imCat[i][1]])

        self.matching.setData(setA,setB)
        tr1, tr2 = self.matching.getMatch()


        im =  self.fitsImage.getImage()
        img_cv = cv2.resize(im,(im.shape[1],im.shape[0]))

        #img_cv = cv2.flip(img_cv, 0)


        starsD = self.fitsImage.getSourcesDetection()
        x,y = [],[]
        for i in range(0,len(starsD)):
            x.append(starsD[i][0])
            y.append(510-starsD[i][1])

        plt.ion()
        plt.imshow(img_cv)
        plt.scatter(x, y, facecolors='none', edgecolors='w')
        plt.plot([tr1[0][0],tr1[1][0]], [510-tr1[0][1],510-tr1[1][1]], linewidth=3)
        plt.plot([tr1[0][0],tr1[1][0],tr1[2][0],tr1[0][0]], [510-tr1[0][1],510-tr1[1][1],510-tr1[2][1],510-tr1[0][1]])
        plt.savefig('trash/foos.png')
        plt.close()
          #  plt.close()
        im = cv2.imread("trash/foos.png",0)
        im = im[45:455, 20:590]

        self.fullImageL = im

        self.textL.configure(text = "Original image")
        self.updatePanelL()

        self.rezultatLabel.configure(text = str(tr1))
        self.rezultatLabel1.configure(text = str(tr2))


        #inter = op.intersectionPoint([tr1[0][0], tr1[0][1]], [tr1[1][0], tr1[1][1]], [tr2[0][0], tr2[0][1]], [tr2[1][0], tr2[1][1]])
       # ang = op.angle3pt([tr1[0][0], tr1[0][1]], inter, [tr2[1][0], tr2[1][1]])

        #print(ang)


        #self.textR.place(y=30,x=930)

        # show triangle R
        self.ucacReg.showCatRegRaw(tr2,minRaUcac,minDecUcac)
        im = cv2.imread("trash/foo.png",0)
        im = im[35:465, 20:590]
        self.fullImageR = im
        self.updatePanelR()

        print(tr1,tr2)

    

##########################################################

    # update the left panel with self.imageRL
    # transform cv2 image to tkinter image and show
    def updatePanelL(self):
        img = cv2.resize(self.fullImageL,(500,400))

        im = Image.fromarray(img)      
        imgtk = ImageTk.PhotoImage(image = im)
        
        self.panelA = Label(self.master, image=imgtk)
        self.panelA.image = imgtk
        self.panelA.place(x=200, y=50)

        # bind mouse events to window
        self.panelA.bind( "<Button-1>", self.clickZoom)

    # update the right panel with self.imageR 
    # transform cv2 image to tkinter image and show
    def updatePanelR(self):
        img = cv2.resize(self.fullImageR,(500,400))

        im = Image.fromarray(img)      
        imgtk = ImageTk.PhotoImage(image = im)
        
        self.panelB = Label(self.master, image=imgtk)
        self.panelB.image = imgtk
        self.panelB.place(x=820, y=50)


    def updatePanelZ(self):
        img = cv2.resize(self.fullImageL,(500,400))
        img =img[self.valClickY-25:self.valClickY+25, self.valClickX-25:self.valClickX+25]
        img = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

        im = Image.fromarray(img)      
        imgtk = ImageTk.PhotoImage(image = im)
        
        self.panelZ = Label(self.master, image=imgtk)
        self.panelZ.image = imgtk
        self.panelZ.place(x=702, y=50)


     # get postion of mouse click in imageL 
    def clickZoom( self, event ):
        self.valClickX = event.x
        self.valClickY = event.y
        print(self.valClickX, self.valClickY)
        self.updatePanelZ()


    #Creation of init_window
    def init_window(self):
        import tkinter as tk

        # background
        image1 = ImageTk.PhotoImage(Image.open("Untitled_Panorama1.jpg"))  # PIL solution       
        panel1 = tk.Label(self.master, image=image1)
        panel1.pack(side='top', fill='both', expand='yes')
        panel1.image = image1

        # changing the title of our master widget      
        self.master.title("ObservatorP")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)



        # menubar
        menubar = Menu(self.master)
        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="ReadExcel", command=self.readExcelFile)
        filemenu.add_command(label="SaveL", command=self.readExcelFile)
        filemenu.add_command(label="SaveR", command=self.readExcelFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command= self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        # display the menu
        self.master.config(menu=menubar)


        # ListBox
        self.listBox = Listbox(self.master, selectmode=SINGLE) # create Listbox
        self.listBox.place(x=20, y=50) # put listbox on window

        # Buttpn
        but = Button(self.master, text='OpenImage', command=self.openImage)
        but.place(x=20, y=208)
        but.config(width = 16 )
        but = Button(self.master, text='StarsDetection', command=self.starsDetection)
        but.place(x=20, y=240)
        but.config(width = 16 )
        but = Button(self.master, text='GetUCAC', command=self.getUcacCat)
        but.place(x=20, y=315)
        but.config(width = 16 )
        but = Button(self.master, text='Precession', command=self.precessUcac)
        but.place(x=20, y=390)
        but.config(width = 16 )
        but = Button(self.master, text='ProperMotion', command=self.properMotion)
        but.place(x=20, y=420)
        but.config(width = 16 )
        but = Button(self.master, text='Matching', command=self.matchingF)
        but.place(x=20, y=450)
        but.config(width = 16 )

        # Label
        self.textL = Label(self.master, text="")
        self.textL.place(y=30,x=420)
        self.textR = Label(self.master, text="")
        self.textR.place(y=30,x=1040)

        self.rezultatLabel = Label(self.master, text="")
        self.rezultatLabel.place(y=500,x=300)

        self.rezultatLabel1 = Label(self.master, text="")
        self.rezultatLabel1.place(y=550,x=300)

        # Slider
        self.sliderA = Scale(self.master, from_=5, to=100, orient=HORIZONTAL)
        self.sliderA.set(16)
        self.sliderA.config(width = 16)
        self.sliderA.place(x=20,y=270)

        self.sliderB = Scale(self.master, from_=5, to=100, orient=HORIZONTAL)
        self.sliderB.set(16)
        self.sliderB.config(width = 16)
        self.sliderB.place(x=20,y=345)
######################################################     ^
    

root = Tk()

root.geometry("1350x590")

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  