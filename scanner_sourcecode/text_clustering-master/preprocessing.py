#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from scanner_dict import mythril_dict, oyente_dict, slither_dict, oyente_id, slither_id

#将每一条漏洞从list转换成string
def listToString(buglist):
    for i in range(len(buglist)):
        buglist[i]=" ".join(buglist[i])
    return buglist

##mythril扫描结果处理
##返回一个分别包含每一条漏洞的列表
def mythril_process(filename):
    linelist = []
    buglist = []
    numlist = []
    file=open(filename)
    for line in file:
        if line == '\n':
            continue
        if re.findall('PC address:', line):
            continue
        if re.findall('Estimated Gas Usage:', line):
            continue
        if re.findall('--------------------', line):
            continue
        if re.findall('In file:',line):
            # print line
            l=line.split(":")
            # print l
            # print len(l)
            if len(l)==3:
                line=l[2]
                # print line
        linelist.append(line)
    length = len(linelist)
    if length == 0:  ##漏洞为空的情况，避免出错跳出
        print
        'mythril empty buglist!'
        pass
    else:
        for i in range(length):
            linelist[i] = linelist[i].strip()  ##去除每一行开头的空格
            if re.findall('====', linelist[i]):
                numlist.append(i)
                if i == 0:
                    continue
                else:
                    sublist = linelist[numlist[-2]:i]
                    buglist.append(sublist)
                    sublist = []
        buglist.append(linelist[numlist[-1]:])
        for bug in buglist:
            swc_id=bug[1].split(": ")[1]
            bug[0]="Name: "+mythril_dict[swc_id]
            bug[1]="ID: "+swc_id
            bug[5]="Description: "+bug[5]
            bug[6]="Location: "+bug[6]
            code = " ".join(bug[7:])
            bug[7]="Code: "+code
            del (bug[8:])
            tmp=bug[1]
            bug[1]=bug[6]
            bug[6]=tmp
    return buglist

##oyente扫描结果处理
##返回一个分别包含每一条漏洞的列表
def oyente_process(filename):
    linelist=[]
    numlist=[]
    buglist=[]
    file = open(filename)
    for line in file:
        line=line.strip()
        if re.findall("Warning", line):
            l=line.split(':')
            l[-4]="Location: "+l[-4]
            l[-2]="Type:"+l[-2]
            l[-1]="Name: "+oyente_dict[l[-1][1:-1]]
            linelist.append(l[-4])
            linelist.append(l[-2])
            linelist.append(l[-1])
        elif re.findall('INFO',line):
            continue
        elif re.findall('WARNING',line):
            continue
        elif re.findall('Flow',line):
            continue
        else:
            linelist.append(line)
    for i in range(len(linelist)):
        if re.findall("Location",linelist[i]):
            numlist.append(i)
            if len(numlist)==1:
                continue
            else:
                sublist = linelist[numlist[-2]:i]
                buglist.append(sublist)
    if len(numlist)==0:
        return buglist
    buglist.append(linelist[numlist[-1]:])
    for bug in buglist:
        s = " ".join(bug[3:])
        bug[3] = "Code: " + s
        del (bug[4:])
        tmp=bug[1]
        bug[1]=bug[0]
        bug[0]=bug[2]
        bug[2]=tmp
        bug.append("ID: "+oyente_id[bug[0][6:]])
    return buglist

##slither扫描结果处理
##返回一个分别包含每一条漏洞的列表
def slither_process(filename):
    linelist=[]
    numlist=[]
    buglist=[]
    file=open(filename)
    for line in file:
        linelist.append(line)
    length=len(linelist)
    for i in range(length):
        if re.findall("INFO:Detectors",linelist[i]):
            numlist.append(i+1)
            if len(numlist)==1:
                continue
            else:
                sublist=linelist[numlist[-2]:i]
                buglist.append(sublist)
                sublist=[]
    buglist.append(linelist[numlist[-1]:-1])
    for bug in buglist:
        if re.findall("Old version",bug[0]):
            location="1"
            description=bug[0][:-1]
            name = re.search("\#.*\x1b", bug[-1]).group()[1:-1]
            reference = bug[-1]
        else:
            location=re.search("\#.*\)",bug[0]).group()[1:-1]
            description=re.search("\).*\n",bug[0]).group()[1:-1]
            name=re.search("\#.*\x1b",bug[-1]).group()[1:-1]
            reference=bug[-1]
        del(bug[:])
        bug.append("Name: "+slither_dict[name])
        bug.append("Location1: "+location)
        bug.append("Description1: "+description)
        bug.append("ID: "+slither_id[name])
        bug.append(reference)
    return buglist


