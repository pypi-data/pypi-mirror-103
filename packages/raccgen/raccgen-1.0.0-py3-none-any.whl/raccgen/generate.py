import csv
import random
import time

def build(infile):
    accdata = []

    with open(infile) as f:
        reader = csv.reader(f)
        for row in reader:
            accdata.append(row)

    return accdata

def racc(data):
    maxn = len(data)
    random.seed(time.time())
    
    first = random.randint(0,maxn)
    last = random.randint(0,maxn)
    password = random.randint(0,maxn)

    first = data[first][0]
    last = data[last][1]
    password = data[password][2]

    return [first, last, first.lower() + last.lower() + str(random.randint(0,99)), password]
