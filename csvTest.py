__author__ = 'Kira'
import csv
cfile = open("chromosome_layout.csv")
thereader = csv.reader(cfile, delimiter=',', quotechar='|')
rows = []
for row in thereader:
    rows.append(row[1])
print(rows)
def getdata(mutation):
    place = rows.index(mutation)
    thereader.readline(place)
cfile.close()
getdata('white eyes')