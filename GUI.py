__author__ = 'Kira'
from tkinter import *
from flyclass import Fly
import copy

def windowSettings(windowName):
    top.minsize(500, 500)
    top.wm_title("Fly Mating")
    h = 500
    w = 700
    ws = top.winfo_screenwidth()
    hs = top.winfo_screenheight()
    x = (ws/2) - (h/2)
    y = (hs/2) - (h/2)
    windowName.geometry('%dx%d+%d+%d' % (w, h, x, y))

def mate(female, male):
    [fAlleles, fMutations, fsexallele] = female.chooseAlleles()
    [mAlleles, mMutations, msexallele] = male.chooseAlleles()
    epistatic = "" #will be filled if a mutation is epistatic to another !!(currently only works if other mutation comes first)!!
    phenotype = [0] #keeps track of which is phenotype, starts out with one zero for sex
    offspring = [] #always ordered female,male so you can do the linked genes and know parent phenotypes
    deleteme = -1
    if(fsexallele == msexallele == "x"): #female
        offspring.append(["female"])
    elif(fsexallele == "x" and msexallele == "y"):
        offspring.append(["male"])
    else:
        print("ERROR IN THE SEX DETERMINATION")
    for i in range(0, 8):
        if (fAlleles[i] == "wild type" and mAlleles[i] == "wild type"):
            offspring.append(["wild type", "wild type"])
            phenotype.append(0)
        if(fAlleles[i] != "wild type" and mAlleles[i] != "wild type"):
            if(fAlleles[i] == mAlleles[i]):
                if(fMutations[i][7] != ""):
                    if(fMutations[i][6] == "no"):
                        epistatic = fMutations[i][7]
                if(fAlleles[i] == epistatic):
                    offspring.append([fAlleles[i], mAlleles[i], "wild type"]) #you can't tell the phenotype so just call it wild type - will delete later
                    phenotype.append(2)
                    deleteme = len(offspring)-1 #gives first index for the list with 3 elements instead of two (need to delete it after printing phenotypes)
                if(fMutations[i][5] == "yes"): #lethal  #could be mMutations but they are the same so it doesn't matter
                    offspring = [["dead"]]
                    phenotype = [0]
                    break
                else:
                    offspring.append([fAlleles[i], mAlleles[i]])
                    phenotype.append(0)
            elif(fAlleles[i] != "wild type" and mAlleles[i] == ""): #sex linked, male, will display mutation whether dominant or recessive
                offspring.append([fAlleles[i], mAlleles[i]])
                phenotype.append(0)
            else:
                print("FEMALE ALLELE: ", fAlleles[i], " MALE ALLELE: ", mAlleles[i])
                print("NOPE") #This cannot happen in flylab
        elif (fAlleles[i] != "wild type" or mAlleles[i] != "wild type"):
            if(fAlleles[i] != "wild type"):
                if(fAlleles[i] == epistatic):
                    offspring.append([fAlleles[i], "wild type"])
                    phenotype.append(1) #not TECHNICALLY this if it is dominant but it doesn't show up b/c it is epistatic to something
                if(fMutations[i][0] == "1" and offspring[0][0] == "male"): #sex linked male - female mutation will appear no matter what
                    offspring.append([fAlleles[i], ""])
                    phenotype.append(0)
                elif(fMutations[i][3] == "no"): #recessive
                    offspring.append([fAlleles[i], "wild type"])#One that comes first in offspring list is female
                    phenotype.append(1)
                else: #dominant
                    offspring.append([fAlleles[i], "wild type"])
                    phenotype.append(0)
            else: #male has mutation
                if(mAlleles[i] == epistatic):
                    offspring.append(["wild type", mAlleles[i]])
                    phenotype.append(0) #epistatic to another gene so nothing will show up
                if(mAlleles[i] == ""): #sex linked, female is wild type and male is mutant but chose Y chromosome
                    offspring.append(["wild type", ""])
                    phenotype.append(0)
                elif(mMutations[i][3] == "no"):
                    offspring.append(["wild type", mAlleles[i]])
                    phenotype.append(0)
                else:
                    offspring.append(["wild type", mAlleles[i]])
                    phenotype.append(1)
    offspringphenotypelist = [] #the phenotypes that will actually be displayed
    if(len(offspring) > 1):
        for i in range(0, 9): #skips over sex
            offspringphenotypelist.append(offspring[i][phenotype[i]])
    else:
        offspringphenotypelist = ["dead"]
    if(deleteme != -1):
        del (offspring[deleteme][2])
    return offspring, phenotype, offspringphenotypelist

again = True
offspringCanUse = False
generation = 1
while (again):
    mutationsF = [["female"]]
    mutationsM = [["male"]]
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
        var8 = StringVar(top)
        var8.set("wild type")

        def useOffspringCallback():
            #gotta make sure offspring aren't dead
            global mutationsF
            global mutationsM
            global generation
            if (i == 1):
                for j in range(0, 1000): #Must find a female
                    if(offspring[j][0] == ["female"]):
                        mutationsF = offspring[j]
                        generation += 1
                        break
                    else:
                        continue
            else:
                for j in range(0, 1000): #Must find a male
                    if(offspring[j][0] == ["male"]):
                        mutationsM = offspring[j]
                        generation += 1
                        break
                    else:
                        continue
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
        wingveins = OptionMenu(top, var8, "wild type", "incomplete wing vein")
        wingveinsL = Label(top, text="Wing Veins: ")
        offspringButton = Button(top, text="USE OFFSPRING", command=useOffspringCallback)
        characteristics = [eyecolors, eyeshapes, bristles, wingshapes, wingsize, bodycolor, antennaeshapes, wingveins]
        labels = [eyecolorsL, eyeshapesL, bristlesL, wingshapesL, wingsizeL, bodycolorL, antennaeshapesL, wingveinsL]
        v = [var1, var2, var3, var4, var5, var6, var7, var8]
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
        female = Fly(True, copy.deepcopy(mutationsF), generation)
        male = Fly(False, copy.deepcopy(mutationsM), generation)
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