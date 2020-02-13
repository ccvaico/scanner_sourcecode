#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import sys

def genFinDataset(res_file, data_file, dataset_file):
    with open(res_file,'r') as f1:   # 扫描结果文件处理，提取源码漏洞位置
        res_line = f1.readline()
        location_list = []
        while res_line:
            if "Location" in res_line:
                location = re.findall(r'Location: (.*?)$', res_line)[0].strip()
                location_list.append(location)
            res_line = f1.readline()
    location_list = list(set(location_list))

    dataset = open(dataset_file, 'a+')
    with open(data_file,'r') as f2:  #代码分片文件处理
        data_line = f2.readline()
        l = 0
        while data_line:
            data_code = data_line.strip('\n').split('\t')[0]
            data_id = data_line.strip('\n').split('\t')[1]
            id_list = data_id.split(',')
            flag = 0
            for i in location_list:
                if i in id_list:
                    dataset.write(data_code + '\t' + "1" + '\n')  #有漏洞标签为1
                    location_list.remove(i)
                    flag = 1
                elif '-' in i:
                    vul_id = i.split('-')
                    arr = [str(x) for x in range(int(vul_id[0]),int(vul_id[1])+1)]
                    for j in arr:
                        if j in id_list:
                            dataset.write(data_code + '\t' + "1" + '\n')  #无漏洞标签为0
                            location_list.remove(i)
                            flag = 1
                            break
                else:
                    continue
            if flag==0:
                dataset.write(data_code + '\t' + "0" + '\n')
            data_line = f2.readline()
if __name__ == '__main__':
    # res_file = "test_data/test_file.sol.res"
    # data_file = "test_data/test_file.sol.res.dataset"
    # dataset_file = "test_data/test_file.sol.res.dataset.final"
    res_file = sys.argv[1]
    data_file = res_file+'.dataset'
    dataset_file = data_file+'.final'
    genFinDataset(res_file, data_file, dataset_file)


