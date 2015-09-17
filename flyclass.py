__author__ = 'Kira'
import random
import math
class Fly:
    def __init__(self, female, mutations):
        self.female = female #either true or false
        self.mutations = mutations #list of mutations, first index is mutation (0 through 6), second index is allele (0 is female, 1 is male)
        self.mutationinfos = [] #fisrt index is mutation (0 through 6), second index is allele (0 or 1), third index is specific data (0 through 5)
        self.mutpair = [] #each pair that is appended to self.mutationinfos
        self.alleles = [""]*(len(self.mutations)-1) #alleles that will be returned from chooseAlleles(), subtract one because you delete sex
        self.listofchromosomes = [[], [], [], []] #chromosome 1 is the X chromosome
        self.sex = [] #[x,x] if female, [x,y] if male
        self.sexallele = "" #either x or y; randomly chosen from self.sex
        self.chromosomeOverload = False #will become true if there are 4 or more mutations on a chromosome
        self.chromosomelayout = [["1","white eyes","w","no","1.5","no","no","" ],["1","tan body","t","no","27.5","no","no","" ],
                                 ["2","curly wings","Cy","yes","6.1","yes","no",""],["2","black body","b","no","48.5","no","no","" ],
                                 ["2","purple eyes","pr","no","54.5","no","no","" ], ["2","vestigial wings","vg","no","67","no","no","incomplete wing vein"],
                                 ["2","lobe eyes","L","yes","72","no","no",""], ["2","brown eyes","bw","no","104.5","no","no","" ],
                                 ["3","stubble bristles","Sb","yes","58.2","yes","no","" ],["3","ebony body","e","no","70.7","no","no",""],
                                 ["4","eyeless","ey","no","2","no","no","" ],["4","shaven bristles","sv","no","3","no","no",""],
                                 ["2","apterous wings","ap","no","55.4","no","no",""], ["3","aristapedia","ssa","no","58.5","yes","no","" ],
                                 ["3","incomplete wing vein","","no","47","no","yes","vestigial wings"]]
                                ###Chromosome, mutation, abbreviation, dominant, number (location), lethal, epistatic, epistatic with

    def getAlleleLocation(self, chromosome, chromosomeindex): #for linked genes, finds location on chromosome
        locationvar = 0
        for allele in chromosome[chromosomeindex]:
            if(locationvar == 0):
                for row in self.chromosomelayout:
                    if (row[1] == allele):
                        locationvar = float(row[4])
        return locationvar

    def chooseAlleles(self):
        del(self.mutations[0]) #remove sex because it isn't a mutation
        self.mutationinfos = []
        if(self.female):
            self.sex = ["x", "x"]
        else:
            self.sex = ["x", "y"]
        for i in range(0, len(self.mutations)):
            self.mutpair = []
            lethal = False
            sexlinked = False
            for allele in self.mutations[i]:
                if (allele == "wild type" or allele == ""):
                    self.mutpair.append([""])
                else:
                    for row in self.chromosomelayout:
                        if (row[1] == allele):
                            self.mutpair.append(row)
                            if (row[5] == "yes"): #check to see if lethal, if it is, make heterozygous
                                lethal = True
                            if (row[0] == "1" and self.female == False): #check to see if it is on x chromosome
                                sexlinked = True
            if(sexlinked == True and self.mutations[i][0] == self.mutations[i][1]):
                self.mutpair[1] = [""]
                self.mutations[i][1] = ""
            if(lethal == True and self.mutations[i][0] == self.mutations[i][1]):
                spot = random.choice([0, 1])
                self.mutpair[spot] = [""]
                self.mutations[i][spot] = "wild type"
            self.mutationinfos.append(self.mutpair)
        #DETERMINE WHICH SEX ALLELE WILL BE PASSED ON
        self.sexallele = random.choice(self.sex)
        for i in range(0, len(self.mutations)): #cycle through each pair of mutation infos and puts them in lists based on chromosomes
            if(self.mutationinfos[i][0] == [""] and self.mutationinfos[i][1] == [""]):
                self.alleles[i] = "wild type"
            elif(self.mutationinfos[i][0] == [""] or self.mutationinfos[i][1] == [""]): #one wild type and one mutation
                mutationchromosome = (self.mutationinfos[i][0][0] or self.mutationinfos[i][1][0]) #this chooses the chromosome that goes with the not wild type allele
                self.listofchromosomes[int(mutationchromosome)-1].append(self.mutations[i])
            elif(self.mutationinfos[i][0][0] == self.mutationinfos[i][1][0]): #both are mutations on same chromosome
                self.listofchromosomes[int(self.mutationinfos[i][0][0])-1].append(self.mutations[i])
        for chromosome in self.listofchromosomes:
            #already took care of if length = 0 because then it is all wild type (line 43)
            if(len(chromosome) == 1): #no linked genes, randomly choose an allele
                if(self.female == False and self.listofchromosomes.index(chromosome) == 0): #male and gene is on X chromosome
                        if(self.sexallele == "x"):
                            self.alleles[self.mutations.index(chromosome[0])] = chromosome[0][0]
                        else:
                            self.alleles[self.mutations.index(chromosome[0])] = chromosome[0][1]
                else:
                    self.alleles[self.mutations.index(chromosome[0])] = random.choice(chromosome[0])
            if(len(chromosome) == 2): #linked genes
                if(self.female == False and self.listofchromosomes.index(chromosome) == 0): #male and X chromosome, no crossing over because only one chromosome
                    if(self.sexallele == "x"):
                        self.alleles[self.mutations.index(chromosome[0])] = chromosome[0][0]
                        self.alleles[self.mutations.index(chromosome[1])] = chromosome[1][0]
                    else: #passing on Y chromosome, which lacks these mutations
                        self.alleles[self.mutations.index(chromosome[0])] = ""
                        self.alleles[self.mutations.index(chromosome[1])] = ""
                elif(chromosome[0][0] == chromosome[0][1] and chromosome[1][0] == chromosome[1][1]): #crossing over doesn't change alleles
                    self.alleles[self.mutations.index(chromosome[0])] = chromosome[0][0] #same as chromosome[0][1]
                    self.alleles[self.mutations.index(chromosome[1])] = chromosome[1][0] #same as chromosome[1][1]
                else: #linked genes, must do crossing over
                    femalechrom = [chromosome[0][0], chromosome[1][0]]
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
                #No sex stuff here yet because we only have 2 genes on X chromosome thus far
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
                    #CHROMOSOME IS NOW ORDERED
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
            if(len(chromosome) > 3): #no crossing over for four linked genes (or more) - complicated and not necessary
                self.chromosomeOverload = True
        self.mutationinfos = [] #going to refill self.mutationinfos with info just for the alleles so mating is easier
        for mut in self.alleles:
            if (mut == "wild type" or mut == ""):
                self.mutationinfos.append([""])
            else:
                for row in self.chromosomelayout:
                    if (row[1] == mut):
                        self.mutationinfos.append(row)
                        break
        return self.alleles, self.mutationinfos, self.sexallele, self.chromosomeOverload
