__author__ = 'Kira'
from tkinter import *
from flyclass import Fly
import csv
mutationsF = []
mutationsM = []
for i in range(1, 3):
    top = Tk()
    femaleL = Label(top, text="CHOOSE FEMALE MUTATIONS")
    maleL = Label(top, text="CHOOSE MALE MUTATIONS")
    if(i == 1):
        femaleL.pack()
    else:
        maleL.pack()
    var1 = StringVar(top)
    var1.set("wild type")
    var2 = StringVar(top)
    var2.set("wild type")
    var3 = StringVar(top)
    var3.set("wild type")
    var4 = StringVar(top)
    var4.set("wild type")
    var5 = StringVar(top)
    var5.set("wild type")
    var6 = StringVar(top)
    var6.set("wild type")
    var7 = StringVar(top)
    var7.set("wild type")

    eyecolors = OptionMenu(top, var1, "purple eyes", "brown eyes", "white eyes")
    eyecolorsL = Label(top, text="Eye Colors:")
    eyeshapes = OptionMenu(top, var2, "lobe eyes", "eyeless")
    eyeshapesL = Label(top, text="Eye Shapes:")
    bristles = OptionMenu(top, var3, "shaven bristles", "stubble bristles")
    bristlesL = Label(top, text="Bristles:")
    wingshapes = OptionMenu(top, var4, "apterous wings", "curly wings")
    wingshapesL = Label(top, text="Wing Shapes:")
    wingsize = OptionMenu(top, var5, "vestigial wings")
    wingsizeL = Label(top, text="Wing Sizes:")
    bodycolor = OptionMenu(top, var6, "ebony body", "black body", "tan body")
    bodycolorL = Label(top, text="Body Colors:")
    antennaeshapes = OptionMenu(top, var7, "aristapedia")
    antennaeshapesL = Label(top, text="Antennae Shapes:")
    characteristics = [eyecolors, eyeshapes, bristles, wingshapes, wingsize, bodycolor, antennaeshapes]
    labels = [eyecolorsL, eyeshapesL, bristlesL, wingshapesL, wingsizeL, bodycolorL, antennaeshapesL]
    v = [var1, var2, var3, var4, var5, var6, var7]
    for c in characteristics:
        labels[characteristics.index(c)].pack()
        c.pack()

    def backCallBack():
        global mutationsF
        global mutationsM
        for var in v:
            trait = var.get()
            if(i == 1):
                mutationsF.append(trait)
            else:
                mutationsM.append(trait)
        top.destroy()
    back = Button(top, text="CONTINUE", command=backCallBack)
    back.pack()
    top.mainloop()

#print("female mutations: ", mutationsF)
#print("male mutations: ", mutationsM)
female = Fly(True, mutationsF, 1)
male = Fly(False, mutationsM, 1)
female.getdata()
male.getdata()
female.chooseAlleles()
male.chooseAlleles()