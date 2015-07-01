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
                    location0 = 0 #finds location on gene for first mutation
                    location1 = 0 #finds location on gene for second mutation
                    for eachthingy in chromosome[0]:
                        if(location0 == 0):
                            cfile.seek(0)
                            for row in thereader:
                                if (row[1] == eachthingy):
                                    num0 = float(row[4])
                    for otherthingies in chromosome[1]:
                        if(location1 == 0):
                            cfile.seek(0)
                            for row in thereader:
                                if (row[1] == otherthingies):
                                    num1 = float(row[4])
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
