__author__ = 'Kira'
from tkinter import *
from flyclass import Fly
import copy

def windowSettings(windowName, height, width):
    windowName.wm_title("Fly Mater")
    h = height
    w = width
    ws = windowName.winfo_screenwidth()
    hs = windowName.winfo_screenheight()
    x = (ws/2) - (h/2)
    y = (hs/2) - (h/2)
    windowName.geometry('%dx%d+%d+%d' % (w, h, x, y))

def mate(female, male):
    [fAlleles, fMutations, fsexallele] = female.chooseAlleles()
    [mAlleles, mMutations, msexallele] = male.chooseAlleles()
    epistatic = "" #will be filled if a mutation is epistatic to another
    offspring = [] #always ordered female,male so you can do the linked genes and know parent phenotypes
    offspringphenotypelist = [] #the phenotypes that will actually be displayed; only mutations, not wild type
    if(fsexallele == msexallele == "x"): #female
        offspring.append(["female"])
        offspringphenotypelist.append("female")
    elif(fsexallele == "x" and msexallele == "y"):
        offspring.append(["male"])
        offspringphenotypelist.append("male")
    else:
        print("ERROR IN THE SEX DETERMINATION")
    for i in range(0, 8): #check to see if there are any mutations that have another mutation that is epistatic to them
        if(fAlleles[i] == mAlleles[i] and fAlleles[i] != "wild type"):
            if(fMutations[i][7] != "" and fMutations[i][6] == "no"):
                epistatic = fMutations[i][7]
    for i in range(0, 8):
        if (fAlleles[i] == "wild type" and mAlleles[i] == "wild type"):
            offspring.append(["wild type", "wild type"])
        if(fAlleles[i] != "wild type" and mAlleles[i] != "wild type"):
            if(fAlleles[i] == mAlleles[i]):
                if(fAlleles[i] == epistatic):
                    offspring.append([fAlleles[i], mAlleles[i]]) #you can't tell the phenotype so just call it wild type
                #currently saying lethal and epistatic are mutually exclusive - don't know if its true but otherwise epistatic goes to else statement too
                elif(fMutations[i][5] == "yes"): #lethal  #could be mMutations but they are the same so it doesn't matter
                    offspring = [["dead"]]
                    offspringphenotypelist = ["dead"]
                    break
                else:
                    offspring.append([fAlleles[i], mAlleles[i]])
                    offspringphenotypelist.append(fAlleles[i])
            elif(fAlleles[i] != "wild type" and mAlleles[i] == ""): #sex linked, male, will display mutation whether dominant or recessive
                offspring.append([fAlleles[i], mAlleles[i]])
                offspringphenotypelist.append(fAlleles[i])
            else:
                print("FEMALE ALLELE: ", fAlleles[i], " MALE ALLELE: ", mAlleles[i])
                print("NOPE") #This cannot happen in flylab
        elif (fAlleles[i] != "wild type" or mAlleles[i] != "wild type"):
            if(fAlleles[i] != "wild type"):
                if(fAlleles[i] == epistatic):
                    offspring.append([fAlleles[i], "wild type"]) #doesn't show up at all though because its epistatic
                elif(fMutations[i][0] == "1" and offspring[0][0] == "male"): #sex linked male - female mutation will appear no matter what
                    offspring.append([fAlleles[i], ""])
                    offspringphenotypelist.append(fAlleles[i])
                elif(fMutations[i][3] == "no"): #recessive
                    offspring.append([fAlleles[i], "wild type"])#One that comes first in offspring list is female
                else: #dominant
                    offspring.append([fAlleles[i], "wild type"])
                    offspringphenotypelist.append(fAlleles[i])
            else: #male has mutation
                if(mAlleles[i] == epistatic):
                    offspring.append(["wild type", mAlleles[i]]) #epistatic so nothing will show up
                elif(mAlleles[i] == ""): #sex linked, female is wild type and male is mutant but chose Y chromosome
                    print("line 75")
                    offspring.append(["wild type", ""])
                elif(mMutations[i][3] == "no"):
                    offspring.append(["wild type", mAlleles[i]])
                else:
                    offspring.append(["wild type", mAlleles[i]])
                    offspringphenotypelist.append(mAlleles[i])
    if(len(offspringphenotypelist) == 1 and offspringphenotypelist[0] != "dead"):
        offspringphenotypelist.append("wild type") #otherwise will just print male or female
    return offspring, offspringphenotypelist

def createFly(i): #1 = female, 2 = male
    global mutationsF
    global mutationsM
    global top
    top = Tk()
    windowSettings(top, 600, 700)
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
    var8 = StringVar(top)
    var8.set("wild type")

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
    characteristics = [eyecolors, eyeshapes, bristles, wingshapes, wingsize, bodycolor, antennaeshapes, wingveins]
    labels = [eyecolorsL, eyeshapesL, bristlesL, wingshapesL, wingsizeL, bodycolorL, antennaeshapesL, wingveinsL]
    v = [var1, var2, var3, var4, var5, var6, var7, var8]
    for c in characteristics:
        #labels[characteristics.index(c)].grid(row = characteristics.index(c), column = 0)
        labels[characteristics.index(c)].pack()
        #c.grid(row = characteristics.index(c), column = 1)
        c.pack()

    def backCallBack(): #command for continue button
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

again = True
firstTime = True #if it is the first time, you select male/female mutations, otherwise you can use offspring or design a new male or female
offspringlist = [] #used to display offspring phenotypes with count
mutationsF = [["female"]]
mutationsM = [["male"]]
while (again):
    if(firstTime):
        mutationsF = [["female"]]
        mutationsM = [["male"]]
        for i in range(1, 3):
            createFly(i)
    offspring = []
    offspringphenotypelist = []
    for i in range(0, 1000): #does mating 1000 times
        female = Fly(True, copy.deepcopy(mutationsF))
        male = Fly(False, copy.deepcopy(mutationsM))
        [offspringpart,  offspringphenotypelistpart] = mate(female, male)
        offspring.append(offspringpart)
        offspringphenotypelist.append(offspringphenotypelistpart)
    firstTime = False
    mutationsF = [["female"]]
    mutationsM = [["male"]]

    from collections import Counter  #this counts how many times each PHENOTYPE appears
    data = offspringphenotypelist
    yes = Counter(", ".join(e) for e in data)
    offspringlist = []
    for k,v in yes.items():
        offspringlist.append([k.split(", "), v]) #takes string/dictionary from Counter and turns it back into list


    bottom = Tk()
    windowSettings(bottom, 600, 700)
    def newCrossCommand():
        global firstTime
        firstTime = True
        bottom.destroy()
    def quitCallBack():
        global again
        again = False
        bottom.destroy()

    newfly = Label(bottom, text = "Offspring")
    newCross = Button(bottom, text = "Perform a new cross", command = newCrossCommand)
    quit = Button(bottom, text = "QUIT", command = quitCallBack)
    newfly.pack()

    #FOLLOWING CODE DEALS WITH DISPLAYING OFFSPRING WITH BUTTONS TO SELECT THEM
    def useOffspringCallback(index):
        global mutationsF
        global mutationsM
        if(offspringlist[index][0][0] == "female"):
            mutationsF = offspring[offspringphenotypelist.index(offspringlist[index][0])]
        elif(offspringlist[index][0][0] == "male"):
            mutationsM = offspring[offspringphenotypelist.index(offspringlist[index][0])]
        if(len(mutationsM) > 1 and len(mutationsF) > 1):
            bottom.destroy()

    def obuttoncallback(index):
        useOffspringCallback(index)

    for i in range(0, len(offspringlist)): #just makes generic label and button, but the button command knows which button it is
        texts = ", ".join(offspringlist[i][0]) + ": " + str(offspringlist[i][1])
        Label(bottom, text=texts).pack()
        if(offspringlist[i][0][0] != "dead"): #makes it so you cannot select dead fly to mate
            Button(bottom, text="Use to mate", command=lambda x=i: obuttoncallback(x)).pack()

    def designFemale():
        createFly(1)

    def designMale():
        createFly(2)

    def mateBcallback(): #mates the flies unless mutations haven't been selected for both of them in which case there is an error message
        if(len(mutationsF) > 1 and len(mutationsM) > 1):
            bottom.destroy()
        elif(len(mutationsF) == 1 and len(mutationsM) == 1):
            errorboth.pack()
        elif(len(mutationsF) == 1):
            errorF.pack()
        elif(len(mutationsM) == 1):
            errorM.pack()
        else:
            print("something happened")

    def ignoreSexCallBack(): #creates a new window where offspring are displayed without regard to sex
        middle = Tk()
        windowSettings(middle, 300, 300)
        data = []
        for i in range(0, len(offspringphenotypelist)):
            if(offspringphenotypelist[i][0] != "dead"):
                data.append(offspringphenotypelist[i][1:]) #deletes the sex from all the offspring
            else: #if the offspring are dead then you don't need to delete the sex - just show dead
                data.append(offspringphenotypelist[i])
        yes = Counter(", ".join(e) for e in data)
        offspringlist = []
        for k,v in yes.items():
            offspringlist.append([k.split(", "), v])
        offspringprint = ("\n".join("{}: {}".format(k, v) for k, v in yes.items()))

        def closeCommand():
            middle.destroy()

        displayOffspringL = Label(middle, text=offspringprint)
        close = Button(middle, text="CLOSE", command=closeCommand, height=3)
        displayOffspringL.pack()
        close.pack()
        middle.mainloop()

    errorboth = Label(bottom, text="Please choose two flies to mate", fg="red")
    errorF = Label(bottom, text="Please design female fly", fg="red")
    errorM = Label(bottom, text="Please design male fly", fg="red")
    designFemaleB = Button(bottom, text="Design Female", command=designFemale)
    designMaleB = Button(bottom, text="Design Male", command=designMale)
    mateB = Button(bottom, text="MATE", command=mateBcallback)
    ignoreSex = Button(bottom, text="Ignore Sex", command=ignoreSexCallBack)
    designFemaleB.pack()
    designMaleB.pack()

    ignoreSex.pack()
    newCross.pack(side=LEFT)
    mateB.pack(side=RIGHT)
    quit.pack(side=BOTTOM)
    bottom.mainloop()