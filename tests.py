__author__ = 'Kira'
clayout = open("readFile.txt", "r")

def locateGene(gene):
    for line in clayout:
        if gene in line:
            chromosome = line
    cnum = chromosome[0]
    wordlocale = chromosome.index(gene)
    num = chromosome[wordlocale+len(gene)+2:wordlocale+len(gene)+7]
    end = wordlocale+len(gene)+11
    if (chromosome[wordlocale+len(gene)+10] == ')'): #works even if only one letter
        end = wordlocale+len(gene)+10
    abbr = chromosome[wordlocale+len(gene)+9:end]
    dominant = False
    if(abbr[0].isupper()):
        dominant = True
    print(cnum, num, abbr, dominant)
#locateGene("stubble bristles")
clayout.close()

me = []
me.append(["no","what","hey"])
me.append("WOOO")
print(me)