__author__ = 'Kira'
import csv
class Fly:
    def __init__(self, female, mutations, generation):
        self.female = female
        self.mutations = mutations
        self.generation = generation
        self.mutationinfos = []
    def getdata(self):
        cfile = open("chromosome_layout.csv")
        thereader = csv.reader(cfile, delimiter=',', quotechar='|')
        for mut in self.mutations:
            if (mut == "wild type"):
                self.mutationinfos.append([])
            else:
                cfile.seek(0)
                for row in thereader:
                    if (row[1] == mut):
                        self.mutationinfos.append(row)
                        break
        return self.mutationinfos
    def chooseAlleles(self):
        if(self.generation == 1):
            return self.mutations