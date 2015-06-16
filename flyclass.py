__author__ = 'Kira'
import csv
class Fly:
    def __init__(self, female, mutations):
        self.female = female
        self.mutations = mutations
    def getdata(self):
        cfile = open("chromosome_layout.csv")
        thereader = csv.reader(cfile, delimiter=',', quotechar='|')
        mutationinfos = []
        for mut in self.mutations:
            if (mut == "wild type"):
                mutationinfos.append([])
            else:
                cfile.seek(0)
                for row in thereader:
                    if (row[1] == mut):
                        mutationinfos.append(row)
                        break
        print(mutationinfos)
    def chooseAlleles(self):
        print(self.mutations)