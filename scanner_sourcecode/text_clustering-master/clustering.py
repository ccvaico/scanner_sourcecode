#!/usr/bin/python
# -*- coding: UTF-8 -*-
from vectorizer import cluster_paragraphs
from random import shuffle
from preprocessing import mythril_process, oyente_process, slither_process, listToString

mythril_filename = 'scanner_res/my_visibility_not_set.txt'
oyente_filename = 'scanner_res/oy_visibility_not_set.txt'
slither_filename = 'scanner_res/sl_visibility_not_set.txt'

buglist1=mythril_process(mythril_filename)
mythril_buglist=listToString(buglist1)
# print "mythril_buglist:",mythril_buglist
# print("mythril_buglist_length:",len(mythril_buglist))

buglist2=oyente_process(oyente_filename)
oyente_buglist=listToString(buglist2)
# print "oyente_buglist:",oyente_buglist
# print("oyente_buglist_length:",len(oyente_buglist))

buglist3=slither_process(slither_filename)
slither_buglist=listToString(buglist3)
# print "slither_buglist:",slither_buglist
# print("slither_buglist_length:",len(slither_buglist))

list = mythril_buglist+oyente_buglist+slither_buglist
# print("list_length:",len(list))
shuffle(list)

clusters = cluster_paragraphs(list)
k=len(clusters)
print("k:",len(clusters))

for i in range(k):
    print("\n")
    print('Group {}:'.format(i))
    print('========\n')
    print('\n-----\n'.join(t for t in clusters[i]))


