#!/usr/bin/python
import sys
import copy
import math
import getopt

def usage():
    print '''Help Information:
    -h, --help: show help information;
    -r, --train: train file;
    -m, --sim: similarity;
    '''

def getparamenter():
    try:
      opts, args = getopt.getopt(sys.argv[1:], "hr:m:", ["help", "train=","sim="])
    except getopt.GetoptError, err:
      print str(err)
      usage()
      sys.exit(1)

    sys.stderr.write("\ntrain.py : a python script for perception training.\n")
    sys.stderr.write("Copyright 2016 sxron, search, Sogou. \n")
    sys.stderr.write("Email: shixiang08abc@gmail.com \n\n")

    train = ''
    sim = ''
    for i, f in opts:
      if i in ("-h", "--help"):
        usage()
        sys.exit(1)
      elif i in ("-r", "--train"):
        train = f
      elif i in ("-m", "--sim"):
        sim = f
      else:
        assert False, "unknown option"
  
    print "start trian parameter \ttrain:%s\tsim:%s" % (train,sim)

    return train,sim

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

def getDist(value,mean):
    dist = 0.0
    feature = []
    valuets = value.strip().split(' ')
    for term in valuets:
        feature.append(term)
    for i in range(0,len(feature),1):
        dist += (float(feature[i])-float(mean[i]))*(float(feature[i])-float(mean[i]))
    return dist

def getStr(vec):
    str = ""
    for tmp in vec:
        str = str + " " + tmp.strip()
    str = str.strip()
    return str

def trainSiglePass(trnData,sim):
    result = {}
    for i in range(0,len(trnData),1):
        Flag = 1
        for key,value in result.items():
            dist =getDist(key,trnData[i])
            if dist<sim:
                value.append(getStr(trnData[i]))
                result[key] = value
                Flag = 0
                break
        if Flag:
            key = getStr(trnData[i])
            vec = []
            result[key] = vec
    return result

def main():
    #set parameter
    train,sim = getparamenter()

    #read train data
    trnData = loadData(train)

    #single-pass
    result = trainSiglePass(trnData,float(sim))
    print result

if __name__=="__main__":
    main()

