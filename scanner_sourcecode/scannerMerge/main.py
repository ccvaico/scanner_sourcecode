#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from interval import Interval
from preprocessing import mythril_process, oyente_process, slither_process, listToString
from scanner_dict import reference1_dict

mythril_filename = '/Users/zhaofangyu/Desktop/scanner_sourcecode/scannerMerge/res_file/mythril_res.txt'
oyente_filename = '/Users/zhaofangyu/Desktop/scanner_sourcecode/scannerMerge/res_file/oyente_res.txt'
slither_filename = '/Users/zhaofangyu/Desktop/scanner_sourcecode/scannerMerge/res_file/slither_res.txt'

buglist1=mythril_process(mythril_filename)
buglist2=oyente_process(oyente_filename)
buglist3=slither_process(slither_filename)
list = buglist1+buglist2+buglist3

list_count = []
for i in range(len(list)):
    list_count.append(i)

list_address=[]
for i in list_count:
    bug_index1 = []
    bug_index1.append(i)
    for x in range(i+1,len(list)):
        if list[x][0]==list[i][0]:
            if re.findall("-",list[i][1]):
                g1 = re.search(" .*\-", list[i][1])
                num1 = g1.group()[1:-1]
                g2 = re.search("\-.*", list[i][1])
                num2 = g2.group()[1:]
                if list[x][1][10:] in Interval(num1,num2):
                    bug_index1.append(x)
                    list_count.remove(x)
            elif re.findall("-",list[x][1]):
                g1 = re.search(" .*\-", list[x][1])
                num1 = g1.group()[1:-1]
                g2 = re.search("\-.*", list[x][1])
                num2 = g2.group()[1:]
                if list[i][1][10:] in Interval(num1, num2):
                    bug_index1.append(x)
                    list_count.remove(x)
            else:
                if list[x][1] == list[i][1]:
                    bug_index1.append(x)
                    list_count.remove(x)
        else:
            continue
    list_address.append(bug_index1)

# for i in range(2,len(list)):
#     for x in list_address:
#         if len(x)!=1 and i in x:
#             list_address.remove([i])

# bug_index=[]
# [bug_index.append(i) for i in list_address if i not in bug_index]

bug_num=len(list_address)
for i in range(bug_num):
    bug_merge = []
    print "======No.",i+1, "======"
    for index in list_address[i]:
        bug_merge.extend(list[index])
    output_dict = {"Name": "", "ID": "", "Type": "", "Description": "", "Location": "", "Code": "",
                   "Reference[1]": "", "Reference[2]": ""}
    for item in bug_merge:
        if re.findall("Name: ",item):
            output_dict["Name"]=item[6:]
        elif re.findall("ID: ",item):
            output_dict["ID"]=item[4:]
            # print output_dict["ID"]
            if reference1_dict.has_key(output_dict["ID"]):
                output_dict["Reference[1]"]=reference1_dict[output_dict["ID"]]
            else:
                continue
        elif re.findall("Type: ",item):
            output_dict["Type"]=item[6:]
        elif re.findall("Description: ",item):
            output_dict["Description"]=item[13:]
        elif re.findall("Description1: ", item) and output_dict["Description"] == "":
            output_dict["Description"] = item[13:]
        elif re.findall("Location: ",item):
            output_dict["Location"]=item[10:]
        elif re.findall("Location1: ", item) and output_dict["Location"] == "":
            output_dict["Location"] = item[10:]
        elif re.findall("Code: ",item):
            output_dict["Code"]=item[6:]
        elif re.findall("Reference: ",item):
            output_dict["Reference[2]"]=item[11:-1]
        else:
            continue
    print "Name:",output_dict["Name"],"\n" \
          "ID:",output_dict["ID"],"\n" \
          "Description:",output_dict["Description"],"\n" \
          "Location:",output_dict["Location"],"\n" \
          "Code:",output_dict["Code"],"\n" \
          "Reference[1]:",output_dict["Reference[1]"],"\n" \
          "Reference[2]:",output_dict["Reference[2]"],"\n"
