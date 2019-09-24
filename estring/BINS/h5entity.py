from estring.h5entity import h5
from estring.h5entity import _kl
from estring.h5entity import _vl
import sys

def tab_strict(kl,vl,cmd):
    tabs = []
    for i in range(len(kl)):
        k = kl[i]
        v = vl[i]
        if(cmd==k):
            tabs = v
            break;
        elif(k.startswith(cmd)):
            tabs.append(k)
        else:
            pass
    return(tabs)


def tab_loose(kl,vl,cmd):
    tabs = []
    for i in range(len(kl)):
        k = kl[i]
        v = vl[i]
        if(cmd==k):
            tabs = v
            break;
        elif(cmd in k):
            tabs.append(k)
        else:
            pass
    return(tabs)


def tab_loose(kl,vl,cmd):
    tabs = []
    for i in range(len(kl)):
        k = kl[i]
        v = vl[i]
        if(cmd==k):
            tabs = v
            break;
        elif(cmd in k):
            tabs.append(k)
        else:
            pass
    return(tabs)


def parr(tabs):
    if(len(tabs)==1):
        print(tabs)
    else:
        for each in tabs:
            print(each)


cmd = ""

try:
    cmd = sys.argv[1]
except:
    cmd = ""
else:
    pass

def loose():
    tabs = tab_loose(_kl,_vl,cmd)
    parr(tabs)


def strict():
    tabs = tab_strict(_kl,_vl,cmd)
    parr(tabs)
