#!/usr/bin/python
import sys
import getopt

def usage():
  print '''Help Information:
  -h, --help: show help information;
  -t, --train: train file;
  -r, --ratio: training ratio;
  -b, --bias: initial bias;
  -x, --slopex: initial slopex;
  -y, --slopey: initial slopey;
  '''

def getErrNum(errFlag):
  errnum = 0
  for i in range(0,len(errFlag),1):
    errnum += errFlag[i]
  return errnum

def getResult(data,slopex,slopey,bias):
  res = data[0]*slopex + data[1]*slopey + bias
  return res 

if __name__=="__main__":
  #set parameter
  try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:r:b:x:y:", ["help", "train=","ratio=","bias=","slopex=","slopey="])
  except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(1)

  sys.stderr.write("\ntrain.py : a python script for perception training.\n")
  sys.stderr.write("Copyright 2016 sxron, search, Sogou. \n")
  sys.stderr.write("Email: shixiang08abc@gmail.com \n\n")

  train = ''
  ratio = 0.1
  bias = 0.0
  slopex = 1.0
  slopey = 1.0
  for i, f in opts:
    if i in ("-h", "--help"):
      usage()
      sys.exit(1)
    elif i in ("-t", "--train"):
      train = f
    elif i in ("-r", "--ratio"):
      ratio = float(f)
    elif i in ("-b", "--bias"):
      bias = float(f)
    elif i in ("-x", "--slopex"):
      slopex = float(f)
    elif i in ("-y", "--slopey"):
      slopey = float(f)
    else:
      assert False, "unknown option"
  
  print "start trian parameter \ttrain:%s\tratio:%f\tbias:%f\tslopex:%f\tslopey:%f" % (train,ratio,bias,slopex,slopey)

  #read train file
  orgdata = []
  label = []
  fin = open(train,'r')
  while 1:
    line = fin.readline()
    if not line:
      break
    ts = line.strip().split('\t')
    if len(ts)==3:
      try:
        lbx = int(ts[0])
        lby = int(ts[1])
        lb = int(ts[2])
      except:
        continue
      data = []
      data.append(lbx)
      data.append(lby)
      orgdata.append(data)
      label.append(lb)
  fin.close()

  for i in range(0,len(label),1):
    print "%d\t%d\t%d" % (orgdata[i][0],orgdata[i][1],label[i])

  errFlag = []
  for i in range(0,len(label),1):
    errFlag.append(0)
 
  while 1:
    for i in range(0,len(label),1):
      errFlag[i] = 0
      result = getResult(orgdata[i],slopex,slopey,bias)
      if result*label[i]<0:
        slopex = slopex + orgdata[i][0]*label[i]*ratio  
        slopey = slopey + orgdata[i][1]*label[i]*ratio
        bias = bias + label[i]*ratio
        errFlag[i] = 1       

    errnum = getErrNum(errFlag)
    if errnum==0:
      break

  print "slopex:%f\tslopey:%f\tbias:%f\t" % (slopex,slopey,bias)




