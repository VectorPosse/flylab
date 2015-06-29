__author__ = 'Kira'
from tkinter import *
from flyclass import Fly

def windowSettings(windowName):
    top.minsize(500, 500)
    top.wm_title("Fly Mating")
    h = 500
    w = 500
    ws = top.winfo_screenwidth()
    hs = top.winfo_screenheight()
    x = (ws/2) - (h/2)
    y = (hs/2) - (h/2)
    windowName.geometry('%dx%d+%d+%d' % (w, h, x, y))

def mate(female, male):
    [fAlleles, fMutations] = female.chooseAlleles()
    [mAlleles, mMutations] = male.chooseAlleles()
    phenotype = [] #keeps track of which is phenotype
    offspring = [] #always ordered female,male so you can do the linked genes and know parent phenotypes
    for i in range(0, 7):
        if (fAlleles[i] == "wild type" and mAlleles[i] == "wild type"):
            offspring.append(["wild type", "wild type"])
            phenotype.append(0)
        if(fAlleles[i] != "wild type" and mAlleles[i] != "wild type"):
            if(fAlleles[i] == mAlleles[i]):
                offspring.append([fAlleles[i], mAlleles[i]])
                phenotype.append(0)
            else:
                print("NOPE") #This cannot happen in flylab
        elif (fAlleles[i] != "wild type" or mAlleles[i] != "wild type"):
            if(fAlleles[i] != "wild type"):
                if(fMutations[i][3] == "no"):
                    offspring.append([fAlleles[i], "wild type"])#One that comes first in offspring list is female
                    phenotype.append(1)
                else:
                    offspring.append([fAlleles[i], "wild type"])
                    phenotype.append(0)
            else:
                if(mMutations[i][3] == "no"):
                    offspring.append(["wild type", mAlleles[i]])
                    phenotype.append(0)
                else:
                    offspring.append(["wild type", mAlleles[i]])
                    phenotype.append(0)
    offspringphenotypelist = [] #the phenotypes that will actually be displayed
    for i in range(0, 7):
        offspringphenotypelist.append(offspring[i][phenotype[i]])
    return offspring, phenotype, offspringphenotypelist

again = True
offspringCanUse = False
while (again):
    mutationsF = []
    mutationsM = []
    for i in range(1, 3):
        top = Tk()
        windowSettings(top)
        femaleL = Label(top, text="CHOOSE FEMALE MUTATIONS")
        femaleOffspringL = Label(top, text="CHOOSE FEMALE MUTATIONS OR USE OFFSPRING")
        maleL = Label(top, text="CHOOSE MALE MUTATIONS")
        maleOffspringL = Label(top, text="CHOOSE MALE MUTATIONS OR USE OFFSPRING")
        if(i == 1):
            if(offspringCanUse):
                femaleOffspringL.pack()
            else:
                femaleL.pack()
        else:
            if(offspringCanUse):
                maleOffspringL.pack()
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

        def useOffspringCallback():
            global mutationsF
            global mutationsM
            if (i == 1):
                mutationsF = offspring[0]
            else:
                mutationsM = offspring[0]
            top.destroy()

        eyecolors = OptionMenu(top, var1, "wild type", "purple eyes", "brown eyes", "white eyes")
        eyecolorsL = Label(top, text="Eye Colors:")
        eyeshapes = OptionMenu(top, var2, "wild type", "lobe eyes", "eyeless")
        eyeshapesL = Label(top, text="Eye Shapes:")
        bristles = OptionMenu(top, var3, "wild type", "shaven bristles", "stubble bristles")
        bristlesL = Label(top, text="Bristles:")
        wingshapes = OptionMenu(top, var4, "wild type", "apterous wings", "curly wings")
        wingshapesL = Label(top, text="Wing Shapes:")
        wingsize = OptionMenu(top, var5, "wild type", "vestigial wings")
        wingsizeL = Label(top, text="Wing Sizes:")
        bodycolor = OptionMenu(top, var6, "wild type", "ebony body", "black body", "tan body")
        bodycolorL = Label(top, text="Body Colors:")
        antennaeshapes = OptionMenu(top, var7, "wild type", "aristapedia")
        antennaeshapesL = Label(top, text="Antennae Shapes:")
        offspringButton = Button(top, text="USE OFFSPRING", command=useOffspringCallback)
        characteristics = [eyecolors, eyeshapes, bristles, wingshapes, wingsize, bodycolor, antennaeshapes]
        labels = [eyecolorsL, eyeshapesL, bristlesL, wingshapesL, wingsizeL, bodycolorL, antennaeshapesL]
        v = [var1, var2, var3, var4, var5, var6, var7]
        for c in characteristics:
            labels[characteristics.index(c)].pack()
            c.pack()

        if(offspringCanUse):
            offspringButton.pack()

        def backCallBack():
            global mutationsF
            global mutationsM
            for var in v:
                trait = var.get()
                if(i == 1):
                    mutationsF.append([trait, trait]) #appends both alleles
                else:
                    mutationsM.append([trait, trait]) #appends both alleles
            top.destroy()
        back = Button(top, text="CONTINUE", command=backCallBack)
        back.pack()
        top.mainloop()

    offspring = []
    phenotype = []
    offspringphenotypelist = []
    for i in range(0, 1000): #does mating 1000 times
        female = Fly(True, mutationsF)
        male = Fly(False, mutationsM)
        [offspringpart, phenotypepart, offspringphenotypelistpart] = mate(female, male)
        offspring.append(offspringpart)
        phenotype.append(phenotypepart)
        offspringphenotypelist.append(offspringphenotypelistpart)

    from collections import Counter  #this counts how many times each PHENOTYPE appears
    data = offspringphenotypelist
    yes = Counter(str(e) for e in data)
    offspringphenotypelistUse = ("\n".join("{}: {}".format(k, v) for k, v in yes.items())) #makes dictionary output look pretty


    top = Tk()
    windowSettings(top)
    def anotherCrossCommand():
        global offspringCanUse
        offspringCanUse = True
        top.destroy()
    def newCrossCommand():
        global offspringCanUse
        offspringCanUse = False
        top.destroy()
    def quitCallBack():
        global again
        again = False
        top.destroy()

    newfly = Label(top, text = "Offspring")
    offspringgenotypelabel = Label(top, text = offspringphenotypelistUse)
    mutationtypesL = Label(top, text = "Eye Color  Eye Shape  Bristles  Wing Shape  Wing Size  Body Color  Antennae Shape")
    anotherCross = Button(top, text = "Perform another cross", command = anotherCrossCommand) #can use offspring
    newCross = Button(top, text = "Perform a new cross", command = newCrossCommand)
    quit = Button(top, text = "QUIT", command = quitCallBack)
    newfly.pack()
    mutationtypesL.pack()
    offspringgenotypelabel.pack()
    anotherCross.pack(side=LEFT)
    newCross.pack(side=RIGHT)
    quit.pack(side=BOTTOM)
    top.mainloop()