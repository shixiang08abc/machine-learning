#!/usr/bin/python
import sys
import copy
import math
import random
import getopt

def usage():
    print '''Help Information:
    -h, --help: show help information;
    -r, --train: train file;
    -k, --kind: kind number;
    -i, --iter: iter number;
    '''

def getparamenter():
    try:
      opts, args = getopt.getopt(sys.argv[1:], "hr:k:i:", ["help", "train=","kind=","iter="])
    except getopt.GetoptError, err:
      print str(err)
      usage()
      sys.exit(1)

    sys.stderr.write("\ntrain.py : a python script for perception training.\n")
    sys.stderr.write("Copyright 2016 sxron, search, Sogou. \n")
    sys.stderr.write("Email: shixiang08abc@gmail.com \n\n")

    train = ''
    kind = 10
    iter = 100
    for i, f in opts:
      if i in ("-h", "--help"):
        usage()
        sys.exit(1)
      elif i in ("-r", "--train"):
        train = f
      elif i in ("-k", "--kind"):
        kind = int(f)
      elif i in ("-i", "--iter"):
        iter = int(f)
      else:
        assert False, "unknown option"
  
    print "start trian parameter \ttrain:%s\tkind:%d\titer:%d" % (train,kind,iter)

    return train,kind,iter

def loadData(file):
    trnData = []
    fin = open(file,'r')
    while 1:
        line = fin.readline()
        if not line:
            break
        ts = line.strip().split(' ')
        vec = []
        for term in ts:
            term = term.strip()
            vec.append(term)
        trnData.append(vec)
    fin.close()
    return trnData

def getDist(feature,mean):
    dist = 0.0
    for i in range(0,len(feature),1):
        dist += (float(feature[i])-float(mean[i]))*(float(feature[i])-float(mean[i]))
    return dist

def getLabel(feature,means):
    label = 0
    mindist = getDist(feature,means[0])
    for i in range(1,len(means),1):
        dist = getDist(feature,means[i])
        if dist<mindist:
            label = i
            mindist = dist
    return label

def getVar(clusters,means):
    var = 0.0
    for i in range(0,len(means),1):
        feaVec = clusters[i]
        for fea in feaVec:
            var += getDist(fea,means[i])
    return var

def updataMeans(cluster):
    mean = []
    length = len(cluster)
    for j in range(0,len(cluster[0]),1):
        sum = 0.0
        for fea in cluster:
            sum += float(fea[j])
        mean.append(sum/length)
    return mean

def trainKmeans(trnData,kind,iter):
    means = []
    # random init means
    his_value = []
    for i in range(0,kind,1):
        index = random.randint(0,len(trnData)-1)
        value = ""
        for tmp in trnData[index]:
            value = value + " " + tmp.strip()
        value = value.strip()
        while (value in set(his_value)):
            index = random.randint(0,len(trnData)-1)
            value = ""
            for tmp in trnData[index]:
                value = value + " " + tmp.strip()
            value = value.strip()
        his_value.append(value)
        means.append(trnData[index])
    #init classify
    clusters = {}
    for feature in trnData:
        label = getLabel(feature,means)
        vec = []
        if clusters.has_key(label):
            vec = clusters[label]
        vec.append(feature)
        clusters[label] = vec
    
    #iter
    oldVar = -1
    newVar = getVar(clusters,means)
    for i in range(0,iter,1):
        if newVar==oldVar:
            print 'classify end by var equal!!'
            break
        for k in range(0,kind,1):
            means[k] = updataMeans(clusters[k])
        oldVar = newVar
        newVar = getVar(clusters,means)
        for k in range(0,kind,1):
            clusters[k] = []
        for feature in trnData:
            label = getLabel(feature,means)
            vec = []
            if clusters.has_key(label):
                vec = clusters[label]
            vec.append(feature)
            clusters[label] = vec
        print 'iter Num:%d\t var:%f' % (i,newVar)
    return means

def main():
    #set parameter
    train,kind,iter = getparamenter()

    #read train data
    trnData = loadData(train)

    #train Kmeans
    means = trainKmeans(trnData,kind,iter) 

    for mean in means:
        print mean

if __name__=="__main__":
    main()

