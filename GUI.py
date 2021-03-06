__author__ = 'Kira'
from tkinter import *
from flyclass import Fly
import copy

chisquaretable = [["DegreesOfFreedom", .995, .990, .975, .950, .900, .100, .050, .250, .010, .0050],
                  [1, 0.000, 0.000, 0.001, 0.004, 0.016, 2.706, 3.841, 5.024, 6.635, 7.879],
                  [2, 0.010, 0.020, 0.051, 0.103, 0.211, 4.605, 5.991, 7.378, 9.210, 10.597],
                  [3, 0.072, 0.115, 0.216, 0.352, 0.584, 6.251, 7.815, 9.348, 11.345, 12.838],
                  [4, 0.207, 0.297, 0.484, 0.711, 1.064, 7.779, 9.488, 11.143, 13.277, 14.860],
                  [5, 0.412, 0.554, 0.831, 1.145, 1.610, 9.236, 11.070, 12.833, 15.086, 16.750],
                  [6, 0.676, 0.872, 1.237, 1.635, 2.204, 10.645, 12.592, 14.449, 16.812, 18.548],
                  [7, 0.989, 1.239, 1.690, 2.167, 2.833, 12.017, 14.067, 16.013, 18.475, 20.278],
                  [8, 1.344, 1.646, 2.180, 2.733, 3.490, 13.362, 15.507, 17.535, 20.090, 21.955],
                  [9, 1.735, 2.088, 2.700, 3.325, 4.168, 14.684, 16.919, 19.023, 21.666, 23.589],
                  [10, 2.156, 2.558, 3.247, 3.940, 4.865, 15.987, 18.307, 20.483, 23.209, 25.188],
                  [11, 2.603, 3.053, 3.816, 4.575, 5.578, 17.275, 19.675, 21.920, 24.725, 26.757],
                  [12, 3.074, 3.571, 4.404, 5.226, 6.304, 18.549, 21.026, 23.337, 26.217, 28.300],
                  [13, 3.565, 4.107, 5.009, 5.892, 7.042, 19.812, 22.362, 24.736, 27.688, 29.819],
                  [14, 4.075, 4.660, 5.629, 6.571, 7.790, 21.064, 23.685, 26.119, 29.141, 31.319],
                  [15, 4.601, 5.229, 6.262, 7.261, 8.547, 22.307, 24.996, 27.488, 30.578, 32.801],
                  [16, 5.142, 5.812, 6.908, 7.962, 9.312, 23.542, 26.296, 28.845, 32.000, 34.267],
                  [17, 5.697, 6.408, 7.564, 8.672, 10.085, 24.769, 27.587, 30.191, 33.409, 35.718],
                  [18, 6.265, 7.015, 8.231, 9.390, 10.865, 25.989, 28.869, 31.526, 34.805, 37.156],
                  [19, 6.844, 7.633, 8.907, 10.117, 11.651, 27.204, 30.144, 32.852, 36.191, 38.582],
                  [20, 7.434, 8.260, 9.591, 10.851, 12.443, 28.412, 31.410, 34.170, 37.566, 39.997]]

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
    global keepgoing
    if(keepgoing==True):
        keepgoing = False
        global mutationsF
        global mutationsM
        global top
        if(sex == 1):
            mutationsF = [["female"]]
        else:
            mutationsM = [["male"]]
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
            global keepgoing
            keepgoing=True
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
keepgoing = True
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
    if(keepgoing):
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

        selectedoffspringf=[]
        selectedoffspringm = []
        designedMale = False
        designedFemale = False
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
            global selectedoffspringf
            global selectedoffspringm
            global mutationsF
            global mutationsM
            if(offspringlist[index][0][0] == "female"):
                selectedoffspringf.append(index)
                mutationsF = offspring[offspringphenotypelist.index(offspringlist[index][0])]
            elif(offspringlist[index][0][0] == "male"):
                selectedoffspringm.append(index)
                mutationsM = offspring[offspringphenotypelist.index(offspringlist[index][0])]
            #if(len(mutationsM) > 1 and len(mutationsF) > 1):
                #bottom.destroy()

        def obuttoncallback(index):
            global defaultbg
            defaultbg=quit.cget('bg') #gets background color of normal buttons (quit button in this case)
            global selectedoffspringf
            global selectedoffspringm
            global offspringlist
            global buttons
            global designedFemale
            global designedMale
            global dead
            #This section turns buttons yellow when that offspring is selected
            if(dead != -1 and index > dead):
                buttons[index-1].configure(bg = "yellow")
            else:
                buttons[index].configure(bg = "yellow")
            #this section turns buttons back to normal button color if another female/male offspring button is pressed
            if(len(selectedoffspringf) > 0 and offspringlist[index][0][0] == "female"):
                if(selectedoffspringf[-1] != index): #makes it so that if you select the same offspring multiple times in a row it stays yellow
                    if(dead != -1 and selectedoffspringf[-1] > dead):
                        buttons[selectedoffspringf[-1]-1].configure(bg=defaultbg)
                    else:
                        buttons[selectedoffspringf[-1]].configure(bg=defaultbg)
            if(len(selectedoffspringm) > 0 and offspringlist[index][0][0] == "male"):
                if(selectedoffspringm[-1] != index):
                    if(dead != -1 and selectedoffspringm[-1] > dead):
                        buttons[selectedoffspringm[-1]-1].configure(bg=defaultbg)
                    else:
                        buttons[selectedoffspringm[-1]].configure(bg=defaultbg)
            #this section turns select female and select male buttons back to normal color if an offspring is then selected to mate
            if(designedFemale == True):
                designFemaleB.configure(bg=defaultbg)
                designedFemale = False
            if(designedMale == True):
                designMaleB.configure(bg=defaultbg)
                designedMale = False

            useOffspringCallback(index)

        rownum = 1
        buttons = []
        dead = -1
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
            global selectedoffspringf
            global buttons
            global dead
            global defaultbg
            global designedFemale
            global keepgoing
            keepgoing = True
            designedFemale = True
            designFemaleB.configure(bg="purple")
            if(len(selectedoffspringf) > 0):
                if(dead != -1 and selectedoffspringf[-1] > dead):
                    buttons[selectedoffspringf[-1]-1].configure(bg=defaultbg)
                else:
                    buttons[selectedoffspringf[-1]].configure(bg=defaultbg)
            createFly(1)

        def designMale():
            global selectedoffspringm
            global buttons
            global dead
            global defaultbg
            global designedMale
            global keepgoing
            keepgoing = True
            designedMale = True
            designMaleB.configure(bg="purple")
            if(len(selectedoffspringm) > 0):
                if(dead != -1 and selectedoffspringm[-1] > dead):
                    buttons[selectedoffspringm[-1]-1].configure(bg=defaultbg)
                else:
                    buttons[selectedoffspringm[-1]].configure(bg=defaultbg)
            createFly(2)

        def mateBcallback(): #mates the flies unless mutations haven't been selected for both of them in which case there is an error message
            global again
            global keepgoing
            keepgoing = True
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
            degreesofFreedom = len(expected) - 1
            pvalueabove = 0
            pvaluebelow = 0
            for i in range(1, len(chisquaretable[degreesofFreedom])):
                if(chisquarevalue <= chisquaretable[degreesofFreedom][i] and i != 1):
                    pvaluebelow = chisquaretable[0][i]
                    pvalueabove = chisquaretable[0][i-1]
                    break
                if(chisquarevalue <= chisquaretable[degreesofFreedom][i] and i == 1):
                    pvaluebelow = .995
                    pvalueabove = 1
                    break
                if(i == len(chisquaretable[degreesofFreedom])-1 and chisquarevalue >= chisquaretable[degreesofFreedom][i]):
                    pvaluebelow = 0
                    pvalueabove = .0050
                    break
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