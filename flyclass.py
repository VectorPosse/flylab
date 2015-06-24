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
        self.x = []
        self.two = []
        self.three = []
        self.four = []
    def chooseAlleles(self):
        self.mutationinfos = []
        cfile = open("chromosome_layout.csv")
        thereader = csv.reader(cfile, delimiter=',', quotechar='|')
        for mut in self.mutations:
            self.mutpair = []
            for allele in mut:
                if (allele == "wild type"):
                    self.mutpair.append([])
                else:
                    cfile.seek(0)
                    for row in thereader:
                        if (row[1] == allele):
                            self.mutpair.append(row)
            self.mutationinfos.append(self.mutpair)
        #print("self.mutationinfos: ", self.mutationinfos)
        for i in range(0, 7):
            if(self.mutationinfos[i][0] == [] and self.mutationinfos[i][1] == []):
                self.alleles[i] = "wild type"
            elif(self.mutationinfos[i][0] == [] or self.mutationinfos[i][1] == []):
                if(self.mutationinfos[i][0] == []):
                    if(self.mutationinfos[i][1][0] == "X"):
                        self.x.append(self.mutations[i])
                    elif(self.mutationinfos[i][1][0] == "2"):
                        self.two.append(self.mutations[i])
                    elif(self.mutationinfos[i][1][0] == "3"):
                        self.three.append(self.mutations[i])
                    elif(self.mutationinfos[i][1][0] == "4"):
                        self.four.append(self.mutations[i])
                elif(self.mutationinfos[i][1] == []):
                    if(self.mutationinfos[i][0][0] == "X"):
                        self.x.append(self.mutations[i])
                    elif(self.mutationinfos[i][0][0] == "2"):
                        self.two.append(self.mutations[i])
                    elif(self.mutationinfos[i][0][0] == "3"):
                        self.three.append(self.mutations[i])
                    elif(self.mutationinfos[i][0][0] == "4"):
                        self.four.append(self.mutations[i])
            elif(self.mutationinfos[i][0][0] == self.mutationinfos[i][1][0]):
                if(self.mutationinfos[i][0][0] == "X"):
                    self.x.append(self.mutations[i])
                elif(self.mutationinfos[i][0][0] == "2"):
                    self.two.append(self.mutations[i])
                elif(self.mutationinfos[i][0][0] == "3"):
                    self.three.append(self.mutations[i])
                elif(self.mutationinfos[i][0][0] == "4"):
                    self.four.append(self.mutations[i])
        for chromosome in [self.x, self.two, self.three, self.four]:
            if(len(chromosome) == 1):
                self.alleles[self.mutations.index(chromosome[0])] = random.choice(chromosome[0])
            if(len(chromosome) == 2):
                if(chromosome[0][0] == chromosome[0][1] and chromosome[1][0] == chromosome[1][1]): #crossing over doesn't change alleles
                    self.alleles[self.mutations.index(chromosome[0])] = chromosome[0][0] #same as chromosome[0][1]
                    self.alleles[self.mutations.index(chromosome[1])] = chromosome[1][0] #same as chromosome[1][1]
                else:
                    chrom1 = [chromosome[0][0], chromosome[1][0]]
                    chrom2 = [chromosome[0][1], chromosome[1][1]]
                    allelespot0 = self.mutations.index(chromosome[0])
                    allelespot1 = self.mutations.index(chromosome[1])
                    num0 = 0
                    num1 = 0
                    for eachthingy in chromosome[0]:
                        if(num0 == 0):
                            cfile.seek(0)
                            for row in thereader:
                                if (row[1] == eachthingy):
                                    num0 = float(row[4])
                    for otherthingies in chromosome[1]:
                        if(num1 == 0):
                            cfile.seek(0)
                            for row in thereader:
                                if (row[1] == otherthingies):
                                    num1 = float(row[4])
                    m = abs(num1-num0)
                    rf = 1/2*(1-math.e**(-m/50))
                    randnumber = random.random()
                    if(randnumber > rf): #no recombination
                        thechromosome = random.choice([chrom1, chrom2])
                        self.alleles[allelespot0] = thechromosome[0]
                        self.alleles[allelespot1] = thechromosome[1]
                    else:   #recombination
                        randomchoice = random.choice([0, 1])
                        if(randomchoice == 0):
                            self.alleles[allelespot0] = chromosome[0][0]
                            self.alleles[allelespot1] = chromosome[1][1]
                        else:
                            self.alleles[allelespot0] = chromosome[0][1]
                            self.alleles[allelespot1] = chromosome[1][0]
            self.mutationinfos = []
            for mut in self.alleles:
                if (mut == "wild type"):
                    self.mutationinfos.append([])
                else:
                    cfile.seek(0)
                    for row in thereader:
                        if (row[1] == mut):
                            self.mutationinfos.append(row)
                            break

        return self.alleles, self.mutationinfos
