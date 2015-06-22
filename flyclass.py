__author__ = 'Kira'
import csv
import random
class Fly:
    def __init__(self, female, mutations):
        self.female = female
        self.mutations = mutations
        self.mutationinfos = []
        self.chromosomenum = []
        self.alleles = []
    def chooseAlleles(self):
        for pair in self.mutations:
            self.alleles.append(random.choice(pair))
        cfile = open("chromosome_layout.csv")
        thereader = csv.reader(cfile, delimiter=',', quotechar='|')
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
    def getLinked(self):
        for listy in self.mutationinfos:
            if (len(listy) > 0):
                self.chromosomenum.append(listy[0])
            else:
                self.chromosomenum.append("")
        return self.chromosomenum
