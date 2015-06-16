__author__ = 'Kira'
import csv
cfile = open("chromosome_layout.csv")
thereader = csv.reader(cfile, delimiter=',', quotechar='|')
rows = []
mutationinfo = []
def getdata(mutation):
    for row in thereader:
        if (row[1] == mutation):
            print(row)
getdata("white eyes")
cfile.close()