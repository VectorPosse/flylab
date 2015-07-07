__author__ = 'Kira'
import csv
import random
import math
class Fly:
    def __init__(self, female, mutations):
        self.female = female
        self.mutations = mutations
        self.mutationinfos = []
        self.chromosomenum = []
        self.mutpair = []
        self.alleles = ["", "", "", "", "", "", ""]
        self.listofchromosomes = [[], [], [], []]
    def getAlleleLocation(self, chromosome, chromosomeindex): #for linked genes, finds location on chromosome
        cfile = open("chromosome_layout.csv")
        thereader = csv.reader(cfile, delimiter=',', quotechar='|')
        locationvar = 0
        for allele in chromosome[chromosomeindex]:
            if(locationvar == 0):
                cfile.seek(0)
                for row in thereader:
                    if (row[1] == allele):
                        locationvar = float(row[4])
        cfile.close()
        return locationvar

    def chooseAlleles(self):
        self.mutationinfos = []
        cfile = open("chromosome_layout.csv")
        thereader = csv.reader(cfile, delimiter=',', quotechar='|')
        for i in range(0, 7):
            self.mutpair = []
            lethal = False
            for allele in self.mutations[i]:
                if (allele == "wild type"):
                    self.mutpair.append([""])
                else:
                    cfile.seek(0)
                    for row in thereader:
                        if (row[1] == allele):
                            self.mutpair.append(row)
                            if (row[5] == "yes"): #check to see if lethal, if it is, make heterozygous
                                lethal = True
            if(lethal == True and self.mutations[i][0] == self.mutations[i][1]):
                spot = random.choice([0, 1])
                self.mutpair[spot] = [""]
                self.mutations[i][spot] = "wild type"
            self.mutationinfos.append(self.mutpair)
        for i in range(0, 7): #cycle through each pair of mutation infos and puts them in lists based on chromosomes
            if(self.mutationinfos[i][0] == [""] and self.mutationinfos[i][1] == [""]):
                self.alleles[i] = "wild type"
            elif(self.mutationinfos[i][0] == [""] or self.mutationinfos[i][1] == [""]): #one wild type and one mutation
                mutationchromosome = (self.mutationinfos[i][0][0] or self.mutationinfos[i][1][0]) #chromosome 1 is the X chromosome, this chooses the chromosome that goes with the not wild type allele
                self.listofchromosomes[int(mutationchromosome)-1].append(self.mutations[i])
            elif(self.mutationinfos[i][0][0] == self.mutationinfos[i][1][0]): #both are mutations on same chromosome
                self.listofchromosomes[int(self.mutationinfos[i][0][0])-1].append(self.mutations[i])
        for chromosome in self.listofchromosomes:
            #already took care of if length = 0 because then it is all wild type (line 41)
            if(len(chromosome) == 1): #no linked genes, randomly choose an allele
                self.alleles[self.mutations.index(chromosome[0])] = random.choice(chromosome[0])
            if(len(chromosome) == 2): #linked genes
                if(chromosome[0][0] == chromosome[0][1] and chromosome[1][0] == chromosome[1][1]): #crossing over doesn't change alleles
                    self.alleles[self.mutations.index(chromosome[0])] = chromosome[0][0] #same as chromosome[0][1]
                    self.alleles[self.mutations.index(chromosome[1])] = chromosome[1][0] #same as chromosome[1][1]
                else: #linked genes, must do crossing over
                    femalechrom = [chromosome[0][0], chromosome[1][0]] #make female and male instead
                    malechrom = [chromosome[0][1], chromosome[1][1]]
                    allelespot0 = self.mutations.index(chromosome[0])
                    allelespot1 = self.mutations.index(chromosome[1])
                    location0 = self.getAlleleLocation(chromosome, 0) #finds location on gene for first mutation
                    location1 = self.getAlleleLocation(chromosome, 1) #finds location on gene for second mutation
                    m = abs(location1-location0)
                    rf = 1/2*(1-math.e**(-m/50)) #mapping function
                    randnumber = random.random()
                    if(randnumber > rf): #no recombination
                        chromosomechoice = random.choice([femalechrom, malechrom])
                        self.alleles[allelespot0] =chromosomechoice[0]
                        self.alleles[allelespot1] = chromosomechoice[1]
                    else:   #recombination
                        randomchoice = random.choice([0, 1])
                        if(randomchoice == 0):
                            self.alleles[allelespot0] = chromosome[0][0]
                            self.alleles[allelespot1] = chromosome[1][1]
                        else:
                            self.alleles[allelespot0] = chromosome[0][1]
                            self.alleles[allelespot1] = chromosome[1][0]
            if(len(chromosome) == 3): #three linked genes
                femalechromosome = [chromosome[0][0], chromosome[1][0], chromosome[2][0]]
                malechromosome = [chromosome[0][1], chromosome[1][1], chromosome[2][1]]
                if(femalechromosome == malechromosome): #no recombination
                    self.alleles[self.mutations.index(chromosome[0])] = chromosome[0][0] #same as chromosome[0][1]
                    self.alleles[self.mutations.index(chromosome[1])] = chromosome[1][0] #same as chromosome[1][1]
                    self.alleles[self.mutations.index(chromosome[2])] = chromosome[2][0] #same as chromosome[2][1]
                else: #must do crossing over
                    threelocation0 = self.getAlleleLocation(chromosome, 0)
                    threelocation1 = self.getAlleleLocation(chromosome, 1)
                    threelocation2 = self.getAlleleLocation(chromosome, 2)
                    morgans01 = abs(threelocation0-threelocation1)
                    morgans12 = abs(threelocation1-threelocation2)
                    morgans20 = abs(threelocation2-threelocation0)
                    unsortedmorgans = [morgans01, morgans12, morgans20]
                    sortedmorgans = sorted([morgans01, morgans12, morgans20])
                    indexmax = unsortedmorgans.index(sortedmorgans[2])
                    indexmin = unsortedmorgans.index(sortedmorgans[0])
                    #ORDERING CHROMOSOME, 0-1-2 where 0-1 is smallest distance
                    if(indexmax == 0 and indexmin == 1):
                        order = [1, 2, 0]
                    elif(indexmax == 0 and indexmin == 2):
                        order = [0, 2, 1]
                    elif(indexmax == 1 and indexmin == 0):
                        order = [1, 0, 2]
                    elif(indexmax == 1 and indexmin == 2):
                        order = [2, 0, 1]
                    elif(indexmax == 2 and indexmin == 0):
                        order = [0, 1, 2]
                    elif(indexmax == 2 and indexmin == 1):
                        order = [2, 1, 0]
                    femalechromosome = [chromosome[order[0]][0], chromosome[order[1]][0], chromosome[order[2]][0]]
                    malechromosome = [chromosome[order[0]][1], chromosome[order[1]][1], chromosome[order[2]][1]]
                    threeAllelespot0 = self.mutations.index(chromosome[order[0]])
                    threeAllelespot1 = self.mutations.index(chromosome[order[1]])
                    threeAllelespot2 = self.mutations.index(chromosome[order[2]])
                    rfmin = 1/2*(1-math.e**(-sortedmorgans[0]/50))
                    rfmiddle = 1/2*(1-math.e**(-sortedmorgans[1]/50))
                    rfdoublerecombination = rfmin*rfmiddle
                    randomnumber = random.random()
                    if(randomnumber <= rfdoublerecombination): #double recombination
                        randallelechoice = random.choice([0, 1])
                        if(randallelechoice == 0):
                            self.alleles[threeAllelespot0] = femalechromosome[0]
                            self.alleles[threeAllelespot1] = malechromosome[1]
                            self.alleles[threeAllelespot2] = femalechromosome[2]
                        else:
                            self.alleles[threeAllelespot0] = malechromosome[0]
                            self.alleles[threeAllelespot1] = femalechromosome[1]
                            self.alleles[threeAllelespot2] = malechromosome[2]
                    if(randomnumber <= rfmin and randomnumber > rfdoublerecombination): #crossing over between closest genes
                        randomchoice = random.choice([0, 1])
                        if(randomchoice == 0):
                            self.alleles[threeAllelespot0] = femalechromosome[0]
                            self.alleles[threeAllelespot1] = malechromosome[1]
                            self.alleles[threeAllelespot2] = malechromosome[2]
                        else:
                            self.alleles[threeAllelespot0] = malechromosome[0]
                            self.alleles[threeAllelespot1] = femalechromosome[1]
                            self.alleles[threeAllelespot2] = femalechromosome[2]
                    if(randomnumber <= rfmiddle+rfmin-rfdoublerecombination and randomnumber > rfmin): #crossing over between other two genes (middle length)
                        randomchoice = random.choice([0, 1])
                        if(randomchoice == 0):
                            self.alleles[threeAllelespot0] = femalechromosome[0]
                            self.alleles[threeAllelespot1] = femalechromosome[1]
                            self.alleles[threeAllelespot2] = malechromosome[2]
                        else:
                            self.alleles[threeAllelespot0] = malechromosome[0]
                            self.alleles[threeAllelespot1] = malechromosome[1]
                            self.alleles[threeAllelespot2] = femalechromosome[2]
                    if(randomnumber > rfmiddle+rfmin-rfdoublerecombination): #no recombination, just choose one of the chromosomes to pass on
                        chromosomechoice = random.choice([femalechromosome, malechromosome])
                        self.alleles[threeAllelespot0] = chromosomechoice[0]
                        self.alleles[threeAllelespot1] = chromosomechoice[1]
                        self.alleles[threeAllelespot2] = chromosomechoice[2]
        self.mutationinfos = [] #going to refill self.mutationinfos with info just for the alleles so mating is easier
        for mut in self.alleles:
            if (mut == "wild type"):
                self.mutationinfos.append([""])
            else:
                cfile.seek(0)
                for row in thereader:
                    if (row[1] == mut):
                        self.mutationinfos.append(row)
                        break

        return self.alleles, self.mutationinfos
