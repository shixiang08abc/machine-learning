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
      opts, args = getopt.getopt(sys.argv[1:], "hr:t:", ["help", "train=","test="])
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

def main():
    #set parameter
    train,test = getparamenter()

if __name__=="__main__":
    main()

