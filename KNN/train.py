#!/usr/bin/python
import sys
import copy
import getopt

def usage():
  print '''Help Information:
  -h, --help: show help information;
  -r, --train: train file;
  -t, --test: test file;
  -k, --kst: k number;
  '''

def getclass(nest_label):
  lendic = {}
  for i in range(0,len(nest_label),1):
    if lendic.has_key(nest_label[i]):
      lendic[nest_label[i]] += 1
    else:
      lendic[nest_label[i]] = 1

  vec = sorted(lendic.iteritems(),key=lambda asd:asd[1],reverse=True)

  maxlen = vec[0][1]
  maxidx = {}
  for i in range(0,len(vec),1):
    if vec[i][1]<maxlen:
      break
    idx = 0
    for k in range(0,len(nest_label),1):
      if nest_label[k]==vec[i][0]:
        idx = k
        break
    maxidx[vec[i][0]] = idx

  vecmax = sorted(maxidx.iteritems(),key=lambda asd:asd[1],reverse=False)

  return vecmax[0][0]

def classify(testdata,orgdata,maxdata,mindata,label,kst):
  for i in range(0,len(testdata),1):
    if testdata[i] > maxdata[i]:
      testdata[i] = 1.0
    elif testdata[i] < mindata[i]:
      testdata[i] = 0.0
    elif maxdata[i]!=mindata[i]:
      testdata[i] = float(testdata[i] - mindata[i]) / (maxdata[i] - mindata[i])
    
  dist_dic = {}
  for i in range(0,len(orgdata),1):
    dist = 0
    for k in range(0,len(orgdata[i]),1):
      dist += (orgdata[i][k] - testdata[k])**2
    dist = dist**0.5
    dist_dic[i] = dist
     
  dist_ls = sorted(dist_dic.iteritems(),key=lambda asd:asd[1],reverse=False)

  nest_label = []
  if kst>len(dist_ls):
    kst = len(dist_ls)
  for i in range(0,kst,1):
    index = dist_ls[i][0]
    nest_label.append(label[index])

  return getclass(nest_label)
  
def autoNorm(orgdata):
  mindata = copy.deepcopy(orgdata[0])
  maxdata = copy.deepcopy(orgdata[0])
  for i in range(1,len(orgdata),1):
    for k in range(0,len(mindata),1):
      if orgdata[i][k] > maxdata[k]:
        maxdata[k] = orgdata[i][k]
      if orgdata[i][k] < mindata[k]:
        mindata[k] = orgdata[i][k]

  for i in range(0,len(orgdata),1):
    for k in range(0,len(orgdata[i]),1):
      if maxdata[k]!=mindata[k]:
        orgdata[i][k] = float(orgdata[i][k] - mindata[k]) / (maxdata[k] - mindata[k])
  return mindata,maxdata

if __name__=="__main__":
  #set parameter
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
  kst = 10
  for i, f in opts:
    if i in ("-h", "--help"):
      usage()
      sys.exit(1)
    elif i in ("-r", "--train"):
      train = f
    elif i in ("-t", "--test"):
      test = f
    elif i in ("-k", "--kst"):
      kst = int(f)
    else:
      assert False, "unknown option"
  
  print "start trian parameter \ttrain:%s\ttest:%s\tkst:%d" % (train,test,kst)

  #read train file
  orgdata = []
  label = []
  fin = open(train,'r')
  while 1:
    line = fin.readline()
    if not line:
      break
    ts = line.strip().split('\t')
    if len(ts)==4:
      try:
        lb1 = float(ts[0].strip())
        lb2 = float(ts[1].strip())
        lb3 = float(ts[2].strip())
        lb = int(ts[3].strip())
      except:
        continue
      data = []
      data.append(lb1)
      data.append(lb2)
      data.append(lb3)
      orgdata.append(data)
      label.append(lb)
  fin.close()

  #read test file
  testdata = []
  rlabel = []
  fin = open(test,'r')
  while 1:
    line = fin.readline()
    if not line:
      break
    ts = line.strip().split('\t')
    if len(ts)==4:
      try:
        lb1 = float(ts[0].strip())
        lb2 = float(ts[1].strip())
        lb3 = float(ts[2].strip())
        lb = int(ts[3].strip())
      except:
        continue
      data = []
      data.append(lb1)
      data.append(lb2)
      data.append(lb3)
      testdata.append(data)
      rlabel.append(lb)
  fin.close()

  mindata,maxdata = autoNorm(orgdata)

  errnum = 0
  for i in range(0,len(testdata),1):
    result_label = classify(testdata[i],orgdata,maxdata,mindata,label,kst)
    if result_label!=rlabel[i]:
      print "index:%d\tresult_label:%d\trlabel:%d" % (i,result_label,rlabel[i])
      errnum += 1
  print "errnum:%d\terrratio:%f" % (errnum,float(errnum)/len(testdata))

