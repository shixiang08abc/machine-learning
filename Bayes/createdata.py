#!/usr/bin/python
import sys
import random

data = []
for line in sys.stdin:
    line = line.strip()
    ts = line.split(',')
    if len(ts)!=9:
        continue
    feature = ''
    try:
        classity = int(ts[8])
        feature = str(classity) + ':'
        for i in range(0,len(ts)-1,1):
            score = float(ts[i])
            feature = feature + str(score) + ' '
    except:
        continue
    data.append(feature.strip())

random.shuffle(data)
fout1 = open('data.trn','w')
fout2= open('data.test','w')

for i in range(0,len(data),1):
    if i%4==1:
        fout2.write(data[i].strip()+'\n')
    else:
        fout1.write(data[i].strip()+'\n')
    
fout1.close()
fout2.close()
            

