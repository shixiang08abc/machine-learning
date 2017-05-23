#!/usr/bin/python
import sys
import copy
import math
import getopt

def usage():
    print '''Help Information:
    -h, --help: show help information;
    -r, --train: train file;
    -t, --test: test file;
    '''

def getparamenter():
    try:
      opts, args = getopt.getopt(sys.argv[1:], "hr:t:k:", ["help", "train=","test=","kst="])
    except getopt.GetoptError, err:
      print str(err)
      usage()
      sys.exit(1)

    sys.stderr.write("\ntrain.py : a python script for perception training.\n")
    sys.stderr.write("Copyright 2016 sxron, search, Sogou. \n")
    sys.stderr.write("Email: shixiang08abc@gmail.com \n\n")

    train = ''
    test = ''
    for i, f in opts:
      if i in ("-h", "--help"):
        usage()
        sys.exit(1)
      elif i in ("-r", "--train"):
        train = f
      elif i in ("-t", "--test"):
        test = f
      else:
        assert False, "unknown option"
  
    print "start trian parameter \ttrain:%s\ttest:%s" % (train,test)

    return train,test

def loaddata(train):
    datavec = []
    fin = open(train,'r')
    while 1:
        line = fin.readline()
        if not line:
            break
        line = line.strip()
        datavec.append(line)
    fin.close

    return datavec

def separatebyclass(trainvec):
    separated = {}
    for line in trainvec:
        ts = line.strip().split(':')
        if len(ts)!=2:
            continue
        try:
            classify = int(ts[0])
            feas = ts[1].strip().split(' ')
            fea_vec = []
            for i in range(0,len(feas),1):
                score = float(feas[i])
                fea_vec.append(score)
        except:
            continue

        value = []
        if separated.has_key(classify):
            value = separated[classify]
        value.append(fea_vec)
        separated[classify] = value
                
    return separated

def mean(vec):
    sum = 0.0
    for i in range(0,len(vec),1):
        sum = sum + float(vec[i])
    return sum/len(vec)

def stdev(vec):
    avg = mean(vec)
    var = 0.0
    for i in range(0,len(vec),1):
      score = float(vec[i])
      var = var + math.pow(vec[i]-avg,2)
    var = var/(len(vec)-1)
    return math.sqrt(var)

def summarize(value):
    sumValue = []
    for i in range(0,len(value[0]),1):
        vec = []
        resVec = []
        for k in range(0,len(value),1):
            score = float(value[k][i])
            vec.append(score)
        avg = mean(vec)
        var = stdev(vec)
        resVec.append(avg)
        resVec.append(var)
        sumValue.append(resVec)
    return sumValue

def summarizeByClass(classdic):
    sumdic = {}
    for key,value in classdic.items():
        sumdic[key] = summarize(value)
    return sumdic

def calculateProbability(x,avg,var):
    exponent = math.exp(-(math.pow(x-avg,2)/(2*math.pow(var,2))))
    return (1 / (math.sqrt(2*math.pi) * var)) * exponent

def calculateClassProbabilities(testVec,sumDic):
    probabilities = {}
    for classValue,classSummaries in sumDic.items():
        probabily = 1.0
        for i in range(0,len(classSummaries),1):
            avg = float(classSummaries[i][0])
            var = float(classSummaries[i][1])
            x = float(testVec[i])
            probabily = probabily * calculateProbability(x,avg,var)
        probabilities[classValue] = probabily
    return probabilities

def getClass(probabilities):
    prob = sorted(probabilities.iteritems(),key=lambda d:d[1],reverse = True)
    return prob[0][0]

def getPredictions(testvec,sumDic):
    testNum = 0
    rightNum = 0
    for i in range(0,len(testvec),1):
        ts = testvec[i].strip().split(':')
        if len(ts)!=2:
            continue
        try:
            targetClass = int(ts[0])
            feas = ts[1].strip().split(' ')
            feaVec = []
            for i in range(0,len(feas),1):
                score = float(feas[i])
                feaVec.append(score)
        except:
            continue

        testNum += 1
        probabilities = calculateClassProbabilities(feaVec,sumDic)
        if targetClass==getClass(probabilities):
            rightNum += 1
    print 'testNum:%d\trightNum:%d\tratio:%f' % (testNum,rightNum,float(rightNum)/testNum)

def main():
    #set parameter
    train,test = getparamenter()
    trainvec = loaddata(train)
    testvec  =loaddata(test)
    
    #Separate by class
    classdic = separatebyclass(trainvec)

    #feature means and variance for class
    sumDic = summarizeByClass(classdic)

    #prediction
    getPredictions(testvec,sumDic)

if __name__=="__main__":
    main()
