from numpy import *
from scipy import *
from math import log
import operator

#����������ݵ���Ũ�أ�
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)  
    labelCounts = {}  #����ֵ䣨��������Ϊ���������ĸ���Ϊֵ��
    for featVec in dataSet:
        currentLabel = featVec[-1]  
        if currentLabel not in labelCounts.keys():  #��û��ӵ��ֵ��������
            labelCounts[currentLabel] = 0;
        labelCounts[currentLabel] += 1;
    shannonEnt = 0.0  
    for key in labelCounts:  #���ÿ�����͵���
        prob = float(labelCounts[key])/numEntries  #ÿ�����͸���ռ���еı�ֵ
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt;  #������

#���ո����������������ݼ�
def splitDataSet(dataSet, axis, value):
    retDataSet = []  
    for featVec in dataSet:  #��dataSet�����еĵ�axis�е�ֵ����value�ķ����ݼ�
        if featVec[axis] == value:      #ֵ����value�ģ�ÿһ��Ϊ�µ��б�ȥ����axis�����ݣ�
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])  
            retDataSet.append(reducedFeatVec) 
    return retDataSet  #���ط������¾���

#ѡ����õ����ݼ����ַ�ʽ
def chooseBestFeatureToSplit(dataSet):  
    numFeatures = len(dataSet[0])-1  #�����Եĸ���
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1  
    for i in range(numFeatures):  #���������Ե���Ϣ����
        featList = [example[i] for example in dataSet]  
        uniqueVals = set(featList)  #��i�����Ե�ȡֵ����ֵͬ��������
        newEntropy = 0.0  
        splitInfo = 0.0;
        for value in uniqueVals:  #���i������ÿ����ֵͬ����*���ǵĸ���
            subDataSet = splitDataSet(dataSet, i , value)  
            prob = len(subDataSet)/float(len(dataSet))  #�����ֵ��i�������еĸ���
            newEntropy += prob * calcShannonEnt(subDataSet)  #��i�����Ը�ֵ���ڵ������
            splitInfo -= prob * log(prob, 2);
        infoGain = (baseEntropy - newEntropy) / splitInfo;  #�����i�����Ե���Ϣ������
        print infoGain;    
        if(infoGain > bestInfoGain):  #������Ϣ������������Ϣ������ֵ�Լ����ڵ��±���ֵi��
            bestInfoGain = infoGain  
            bestFeature = i  
    return bestFeature  

#�ҳ����ִ������ķ�������
def majorityCnt(classList):  
    classCount = {}  
    for vote in classList:  
        if vote not in classCount.keys(): classCount[vote] = 0  
        classCount[vote] += 1  
    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]  

#������
def createTree(dataSet, labels):  
    classList = [example[-1] for example in dataSet];    #������Ҫ��������ѵ�����ݵĽ���б������������б���[N, N, Y, Y, Y, N, Y]��
    if classList.count(classList[0]) == len(classList):  #������е�ѵ�����ݶ�������һ������򷵻ظ����
        return classList[0];  
    if (len(dataSet[0]) == 1):  #ѵ������ֻ����������ݣ�û���κ�����ֵ���ݣ������س��ִ������ķ�������
        return majorityCnt(classList);

    bestFeat = chooseBestFeatureToSplit(dataSet);   #ѡ����Ϣ�����������Խ��з֣�����ֵ�����������б���±꣩
    bestFeatLabel = labels[bestFeat]  #�����±����������Ƶ����ĸ��ڵ�
    myTree = {bestFeatLabel:{}}  #��bestFeatLabelΪ���ڵ㽨һ������
    del(labels[bestFeat])  #�������б���ɾ���Ѿ���ѡ���������ڵ������
    featValues = [example[bestFeat] for example in dataSet]  #�ҳ�����������ѵ�����ݵ�ֵ�������б�
    uniqueVals = set(featValues)  #��������Ե�����ֵ�ü��ϣ����ϵ�Ԫ�ز����ظ���
    for value in uniqueVals:  #���ݸ����Ե�ֵ�����ĸ�����֧
        subLabels = labels[:]  
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)  #���ݸ�����֧�ݹ鴴����
    return myTree  #���ɵ���

#ʵ�þ��������з���
def classify(inputTree, featLabels, testVec):  
    firstStr = inputTree.keys()[0]  
    secondDict = inputTree[firstStr]  
    featIndex = featLabels.index(firstStr)  
    for key in secondDict.keys():  
        if testVec[featIndex] == key:  
            if type(secondDict[key]).__name__ == 'dict':  
                classLabel = classify(secondDict[key], featLabels, testVec)  
            else: classLabel = secondDict[key]  
    return classLabel  

#��ȡ�����ĵ��е�ѵ�����ݣ����ɶ�ά�б�
def createTrainData():
    lines_set = open('../data/ID3/Dataset.txt').readlines()
    labelLine = lines_set[2];
    labels = labelLine.strip().split()
    lines_set = lines_set[4:11]
    dataSet = [];
    for line in lines_set:
        data = line.split();
        dataSet.append(data);
    return dataSet, labels


#��ȡ�����ĵ��еĲ������ݣ����ɶ�ά�б�
def createTestData():
    lines_set = open('../data/ID3/Dataset.txt').readlines()
    lines_set = lines_set[15:22]
    dataSet = [];
    for line in lines_set:
        data = line.strip().split();
        dataSet.append(data);
    return dataSet

myDat, labels = createTrainData()  
myTree = createTree(myDat,labels) 
print myTree
bootList = ['outlook','temperature', 'humidity', 'windy'];
testList = createTestData();
for testData in testList:
    dic = classify(myTree, bootList, testData)
    print dic
