__author__ = 'Kira'
from tkinter import *
from flyclass import Fly
#import scipy
from scipy import stats
# import scipy.stats
import copy
import csv



def windowSettings(windowName, height, width):
    windowName.wm_title("Fly Mater")
    h = height
    w = width
    ws = windowName.winfo_screenwidth()
    hs = windowName.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    windowName.geometry('%dx%d+%d+%d' % (w, h, x, y))

def mate(female, male):
    [fAlleles, fMutations, fsexallele, fchromosomeOverload] = female.chooseAlleles()
    [mAlleles, mMutations, msexallele, mchromosomeOverload] = male.chooseAlleles()
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
    for i in range(0, len(fAlleles)): #check to see if there are any mutations that have another mutation that is epistatic to them
        if(fAlleles[i] == mAlleles[i] and fAlleles[i] != "wild type"):
            if(fMutations[i][7] != "" and fMutations[i][6] == "no"):
                epistatic = fMutations[i][7]
    for i in range(0, len(fAlleles)):
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
                print("NOPE") #This should not happen
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
                    offspring.append(["wild type", ""])
                elif(mMutations[i][3] == "no"):
                    offspring.append(["wild type", mAlleles[i]])
                else:
                    offspring.append(["wild type", mAlleles[i]])
                    offspringphenotypelist.append(mAlleles[i])
    if(len(offspringphenotypelist) == 1 and offspringphenotypelist[0] != "dead"):
        offspringphenotypelist.append("wild type") #otherwise will just print male or female
    return offspring, offspringphenotypelist, fchromosomeOverload, mchromosomeOverload

def createFly(sex): #1 = female, 2 = male
    global mutationsF
    global mutationsM
    global top
    top = Tk()
    windowSettings(top, 600, 700)
    femaleL = Label(top, text="CHOOSE FEMALE MUTATIONS")
    maleL = Label(top, text="CHOOSE MALE MUTATIONS")
    if(sex == 1):
        femaleL.pack()
    else:
        maleL.pack()

    varss = [] #creates list of unnamed variables for option menus below
    for i in range(0, 8):
        varss.append(StringVar(top))
        varss[i].set("wild type")

    ####
    # To add a new mutations, just add it to the correct tuple from those below
    # and add it to the chromosome_layout.csv file, along with the information
    # about its location on the chromosome
    ####
    eyecolors = ("wild type", "purple eyes", "brown eyes", "white eyes")
    eyeshapes = ("wild type", "lobe eyes", "eyeless")
    bristles = ("wild type", "shaven bristles", "stubble bristles")
    wingshapes = ("wild type", "apterous wings", "curly wings")
    wingsize = ("wild type", "vestigial wings")
    bodycolor = ("wild type", "ebony body", "black body", "tan body")
    antennaeshapes = ("wild type", "aristapedia")
    wingveins = ("wild type", "incomplete wing vein")

    eyecolorsL = Label(top, text="Eye Colors:")
    eyeshapesL = Label(top, text="Eye Shapes:")
    bristlesL = Label(top, text="Bristles:")
    wingshapesL = Label(top, text="Wing Shapes:")
    wingsizeL = Label(top, text="Wing Sizes:")
    bodycolorL = Label(top, text="Body Colors:")
    antennaeshapesL = Label(top, text="Antennae Shapes:")
    wingveinsL = Label(top, text="Wing Veins: ")
    characteristics = [eyecolors, eyeshapes, bristles, wingshapes, wingsize, bodycolor, antennaeshapes, wingveins]
    labels = [eyecolorsL, eyeshapesL, bristlesL, wingshapesL, wingsizeL, bodycolorL, antennaeshapesL, wingveinsL]

    optionMenus = []
    for i in range(0, 8):
        labels[i].pack()
        optionMenus.append(OptionMenu(top, varss[i], *characteristics[i])) # *characteristics[i] uses all the mutations from the tuple selected from characteristics
        optionMenus[i].pack()

    def backCallBack(): #command for continue button
        global mutationsF
        global mutationsM
        for i in range(0, 8):
            trait = varss[i].get()
            traitspotinOptionMenu = characteristics[i].index(trait)
            if(sex == 1):
                if(trait != "wild type"):
                    for k in range(1, traitspotinOptionMenu):
                        mutationsF.append(["wild type", "wild type"]) #appends both alleles
                    mutationsF.append([trait, trait])
                    for j in range(traitspotinOptionMenu+1, len(characteristics[i])):\
                        mutationsF.append(["wild type", "wild type"])
                else:
                    for k in range(1, len(characteristics[i])):
                        mutationsF.append([trait, trait])
            else:
                if(trait != "wild type"):
                    for k in range(1, traitspotinOptionMenu):
                        mutationsM.append(["wild type", "wild type"]) #appends both alleles
                    mutationsM.append([trait, trait])
                    for j in range(traitspotinOptionMenu+1, len(characteristics[i])):
                        mutationsM.append(["wild type", "wild type"])
                else:
                    for k in range(1, len(characteristics[i])):
                        mutationsM.append(["wild type", "wild type"])
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
    again = False
    if(firstTime):
        mutationsF = [["female"]]
        mutationsM = [["male"]]
        for i in range(1, 3):
            createFly(i)
    offspring = []
    offspringphenotypelist = []
    chromosomeOverload = []
    for i in range(0, 1000): #does mating 1000 times
        female = Fly(True, copy.deepcopy(mutationsF))
        male = Fly(False, copy.deepcopy(mutationsM))
        [offspringpart,  offspringphenotypelistpart, moverload, foverload] = mate(female, male)
        chromosomeOverload.append(moverload)
        chromosomeOverload.append(foverload)
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
    #bottom.configure(bg="LightBlue1")
    windowSettings(bottom, 600, 1200)
    for i in range(0,4):
        bottom.columnconfigure(i, minsize=300)
    #bottom.columnconfigure(2, weight = 3)
    def newCrossCommand():
        global again
        global firstTime
        again = True
        firstTime = True
        bottom.destroy()
    def quitCallBack():
        global again
        again = False
        bottom.destroy()


    newfly = Label(bottom, text = "Offspring")
    newCross = Button(bottom, text = "Perform a new cross", command = newCrossCommand)
    quit = Button(bottom, text = "QUIT", command = quitCallBack)
    newfly.grid(row = 0, column = 1, columnspan = 2)

    #FOLLOWING CODE DEALS WITH DISPLAYING OFFSPRING WITH BUTTONS TO SELECT THEM
    def useOffspringCallback(index):
        global mutationsF
        global mutationsM
        if(offspringlist[index][0][0] == "female"):
            mutationsF = offspring[offspringphenotypelist.index(offspringlist[index][0])]
        elif(offspringlist[index][0][0] == "male"):
            mutationsM = offspring[offspringphenotypelist.index(offspringlist[index][0])]
        #if(len(mutationsM) > 1 and len(mutationsF) > 1):
            #bottom.destroy()

    def obuttoncallback(index):
        global buttons
        global dead
        if(dead != 0 and index > dead):
            buttons[index-1].configure(bg = "yellow")
        else:
            buttons[index].configure(bg = "yellow")
        useOffspringCallback(index)

    rownum = 1
    buttons = []
    dead = 0
    for i in range(0, len(offspringlist)): #just makes generic label and button, but the button command knows which button it is
        texts = ", ".join(offspringlist[i][0]) + ": " + str(offspringlist[i][1])
        Label(bottom, text=texts).grid(row = rownum, column = 1, sticky=E)
        if(offspringlist[i][0][0] != "dead"): #makes it so you cannot select dead fly to mate
            buttons.append(Button(bottom, text="Use to mate", command=lambda x=i: obuttoncallback(x)))
            buttons[-1].grid(row = rownum, column = 2, sticky=W)
        else:
            dead = i
        rownum += 1

    def designFemale():
        designFemaleB.configure(bg="purple")
        createFly(1)

    def designMale():
        designMaleB.configure(bg="purple")
        createFly(2)

    def mateBcallback(): #mates the flies unless mutations haven't been selected for both of them in which case there is an error message
        global again
        again = True
        if(len(mutationsF) > 1 and len(mutationsM) > 1):
            bottom.destroy()
        elif(len(mutationsF) == 1 and len(mutationsM) == 1):
            errorboth.grid()
        elif(len(mutationsF) == 1):
            errorF.grid()
        elif(len(mutationsM) == 1):
            errorM.grid()
        else:
            print("something happened")

    def ignoreSexCallBack(): #creates a new window where offspring are displayed without regard to sex
        middle = Tk()
        windowSettings(middle, 400, 400)
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

    def chisquareDo(): #actually performs chi-square test
        global entries
        expected = []
        observed = []
        for i in range(0, len(offspringlist)):
            if(entries[i].get() == ""):
                Label(bottom, text="Please finish filling in expected values", fg="red").grid()
                break
            else:
                expected.append(int(entries[i].get()))
                observed.append(offspringlist[i][1])
        chisquarevalue = 0
        for i in range(0, len(expected)):
            chisquarevalue += ((observed[i] - expected[i])**2)/expected[i]
        print(chisquarevalue)
        chifile = open("chisquaretable.csv")
        thereader = csv.reader(chifile, delimiter=' ', quotechar='|')
        degreesofFreedom = len(expected) - 1
        pvalueabove = 0
        pvaluebelow = 0
        chifile.seek(0)
        for row in thereader:
            if(str(degreesofFreedom) == row[0]):
                chifile.seek(0)
                for lines in thereader:
                    if(lines[0] == 'DegreesOfFreedom'):
                        for numbers in range(1, len(row)):
                            if(chisquarevalue <= float(row[numbers]) and numbers != 1):
                                pvaluebelow = float(lines[numbers])
                                pvalueabove = float(lines[numbers-1])
                                break
                            elif(chisquarevalue <= float(row[numbers]) and numbers == 1):
                                pvaluebelow = float(lines[numbers])
                                pvalueabove = 1
                                break
                            elif(numbers == len(row)-1 and chisquarevalue >= float(row[numbers])):
                                pvaluebelow = 0
                                pvalueabove = float(lines[10])
                                break
        chifile.close()
        print("The p-value is between ", pvaluebelow, " and ", pvalueabove)
        chisquareresults = Label(bottom, text="chi square = " + str(chisquarevalue))
        chisquareresults2 = Label(bottom, text="the p-value is between " + str(pvaluebelow) + " and " + str(pvalueabove))
        chisquareresults.grid(column = 3)
        chisquareresults2.grid(column = 3)

    def chisquareShowInput(): #displays entry boxes for expected values
        global rownum
        global entries
        entries = []
        Label(bottom, text="Enter Expected Values:").grid(row = 0, column = 3)
        for i in range(0, len(offspringlist)):
            entries.append(Entry(bottom))
            entries[i].grid(row=i+1, column=3)
        chisquare.configure(text="Calculate", command=chisquareDo)
        chisquare.grid(row=rownum, column=3, sticky=NSEW)


    errorboth = Label(bottom, text="Please choose two flies to mate", fg="red")
    errorF = Label(bottom, text="Please design female fly", fg="red")
    errorM = Label(bottom, text="Please design male fly", fg="red")
    designFemaleB = Button(bottom, text="Design Female", command=designFemale)
    designMaleB = Button(bottom, text="Design Male", command=designMale)
    mateB = Button(bottom, text="MATE", command=mateBcallback)
    ignoreSex = Button(bottom, text="Ignore Sex", command=ignoreSexCallBack)
    chisquare = Button(bottom, text="Perform Chi-Square Test", command=chisquareShowInput)
    designFemaleB.grid(row = rownum+1, column = 0, pady = (5,0))
    rownum += 1
    designMaleB.grid(row = rownum+1, column = 0, pady=(0,5))
    rownum += 2

    bottom.columnconfigure(rownum, weight = 2)
    ignoreSex.grid(row = 0, column = 0, sticky=NW)
    newCross.grid(row = rownum, column = 0, sticky=NSEW)
    mateB.grid(row = rownum, column = 1, sticky=NSEW)
    quit.grid(row = rownum, column = 2, sticky=NSEW)
    chisquare.grid(row = rownum, column = 3, sticky=NSEW)

    if(True in chromosomeOverload):
        Label(bottom, text="Error: Please only choose at most three mutations per chromosome", fg="red").grid(columnspan=4, pady=15)


    bottom.mainloop()