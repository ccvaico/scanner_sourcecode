#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import sys
import pandas as pd

#保留字
key_word = ['pragma','solidity','import','as','from','public','private','internal','external','pure',
            'constant','view','payable','contract','function','event','returns','return','var','bool','int',
            'int8','int256','uint','uint8','uint256','address','bytes','bytes1','bytes2','bytes3','bytes4',
            'bytes5','bytes6','bytes7','bytes8','bytes9','bytes10','bytes11','bytes12','bytes13','bytes14',
            'bytes15','bytes16','bytes17','bytes18','bytes19','bytes20','bytes21','bytes22','bytes23',
            'bytes24','bytes25','bytes26','bytes27','bytes28','bytes29','bytes30','bytes31','bytes32',
            'string','enum','mapping','memory','storage','struct','require','new','this','self','calldata',
            'for','if','library','assert','indexed','constructor','modifier','emit','is','using','false','true','ether']

#运算符
operator = ['+','-','*','/','%','!','&&','||','==','!=','<=','<','>=','>',
            '&','|','^','~','<<','>>']

#界符
delimiters = ['{','}','[',']','(',')','.',';','"',"'",',']

#给源代码文件添加行号生成中间代码文件
def readfile(sourcefile):
    outputfile_name = sourcefile+".tmp"
    outputfile = open(outputfile_name,'a+')
    with open(sourcefile,'r') as f:
        line = f.readline()
        line_number = 1
        while line:
            line = line.strip('\r\n').strip(' ')
            out_line = line+'\t'+str(line_number)   #源代码与行号以\t分隔
            outputfile.write(out_line+'\n')
            line_number+=1
            line = f.readline()
    outputfile.close()

#对添加行号的代码文件进行过滤，去掉空行与注释
def filterResouce(tmp_file, filter_filename):
    filter_file = open(filter_filename,'a+')
    with open(tmp_file,'r') as f:
        line = f.readline()
        while line:
            code_line = line.split('\t')[0]
            line_num = line.split('\t')[1]
            if code_line == '' or code_line[0:2]=='//' or code_line[0]=='*':  #判断空行与单行注释
                pass
            elif code_line[0:2]=='/*':   #判断多行注释
                while not code_line.endswith('*/'):
                    line = f.readline()
                    code_line = line.split('\t')[0]
            elif '//' in code_line and code_line[0:2]!='//':
                subline = code_line.split('//')[0].strip(' ')
                line = subline+'\t'+str(line_num)
                filter_file.write(line)
            else:
                filter_file.write(line)
            line = f.readline()
    filter_file.close()

def genCNT_struct(filename, dataset_filename):
    filter_df = pd.read_csv(filename, sep='\t', names=['code', 'line_number'])
    dataset_file = open(dataset_filename, 'a+')  # 输出的数据集文件
    function_df = pd.DataFrame(columns=['name', 'parameters', 'startline', 'use_function', 'endline'])  # 函数信息表
    contract_df = pd.DataFrame(columns=['name', 'parents', 'startline', 'endline'])  # 合约信息表
    constructor_df = pd.DataFrame(columns=['name', 'parameters', 'startline', 'endline'])  # 复合语句控制结构信息表
    func_deli_list = []
    cons_deli_list = []
    cons_deli_list_tmp = []
    function = []
    constructor = []
    func_startline = 0
    for i in range(len(filter_df)):
        code = filter_df.iloc[i]['code']
        # 版本信息直接保存
        if str(code).startswith('pragma'):
            dataset_file.write(code + '\t' + str(filter_df.iloc[i]['line_number']) + '\n\t\n')
        # ----------------开始构建函数信息表----------------
        if str(code).startswith('function'):
            # 获取函数名称
            reg = r'function (.*?)\('
            function = re.findall(reg, str(code))
            # 获取函数参数

            if ')' not in str(code):    #以参数分行的函数形式
                func_fin = 0
                split_paras = []
                for j in range(i, len(filter_df)):
                    split_paras.append(str(filter_df.iloc[j]['code']))
                    if '{' in str(filter_df.iloc[j]['code']):
                        func_deli_list = ['{']
                        func_title = ''.join(split_paras)
                        reg = r'\((.*?)\)'
                        function_parameters = re.findall(reg, func_title)[0]
                        function_para = ''
                        para = re.split(" ", function_parameters)
                        for s in para:
                            if s not in key_word:
                                function_para = function_para + s
                        function.append(function_para)
                        func_startline = i + 1
                        function.append(func_startline)
                        func_fin = j
                        break
                for j in range(func_fin+1, len(filter_df)):
                    if len(func_deli_list)>=1:
                        if '{' in str(filter_df.iloc[j]['code']):
                            func_deli_list.append('{')
                        if '}' in str(filter_df.iloc[j]['code']):
                            func_deli_list.append('}')
                            if len(func_deli_list)%2==0:
                                use_function = ''
                                func_endline = j+1
                                function.append(use_function)
                                function.append(func_endline)
                                function_df.loc[len(function_df)] = function
                                function = []
                                func_deli_list = []
                                break
            else:
                reg = r'\((.*?)\)'
                function_parameters = re.findall(reg, str(code))[0]
                function_para = ''
                para = re.split(" ", function_parameters)
                for s in para:
                    if s not in key_word:
                        function_para = function_para + s
                function.append(function_para)
            # 获取函数开始行
            func_startline = i+1
            function.append(func_startline)
            if '{' in str(code):
                func_deli_list = ['{']
            else:
                func_endline = i+1
                use_function = ''
                function.append(use_function)
                function.append(func_endline)
        # 获取函数中的调用函数
        if len(func_deli_list) == 1:
            reg = r' = (.*?)\('
            if re.findall(reg, str(code)):
                use_function = re.findall(reg, str(code))[0]
                function.append(use_function)
            # 获取函数结束行
            for j in range(func_startline+1,len(filter_df)):    #考虑函数内部包含复合结构语句的情况
                if '{' in str(filter_df.iloc[j]['code']):
                    func_deli_list.append('{')
                if '}' in str(filter_df.iloc[j]['code']):
                    func_deli_list.append('}')
                    if len(func_deli_list) % 2 == 0:
                        func_endline = j + 1
                        if len(function) == 3:
                            use_function = ''
                            function.append(use_function)
                        function.append(func_endline)
                        # function_df.loc[len(function_df)] = function
                        # function = []
                        break
        if len(function) == 5:
            function_df.loc[len(function_df)] = function
            function = []
        # ----------------开始构建合约信息表----------------
        if str(code).startswith('contract'):
            contract_list = str(code).split(' ')
            contract_name = contract_list[1]
            contract = [contract_name]
            if len(contract_list) == 5:
                parent = contract_list[3]
                contract.append(parent)
            else:
                contract.append('')
            contract_startline = i+1
            contract.append(contract_startline)
            cont_deli_list = ['{']
            for j in range(i+1, len(filter_df)):
                if '{' in str(filter_df.iloc[j]['code']):
                    cont_deli_list.append('{')
                if '}' in str(filter_df.iloc[j]['code']):
                    cont_deli_list.append('}')
                    if len(cont_deli_list) % 2 == 0:
                        cont_endline = j + 1
                        contract.append(cont_endline)
                        # contract_df.loc[len(contract_df)] = contract
                        break
            if len(contract) == 4:
                contract_df.loc[len(contract_df)] = contract
                contract = []
        # ----------------开始构建构造函数信息表----------------
        if str(code).startswith('constructor'):
            constructor = ['constructor']
            if ')' not in str(code):    #以参数分行的函数形式
                cons_fin = 0
                split_paras = []
                for j in range(i, len(filter_df)):
                    split_paras.append(str(filter_df.iloc[j]['code']))
                    if '{' in str(filter_df.iloc[j]['code']):
                        cons_deli_list = ['{']
                        cons_title = ''.join(split_paras)
                        reg = r'\((.*?)\)'
                        cons_parameters = re.findall(reg, cons_title)[0]
                        cons_para = ''
                        para = re.split(" ", cons_parameters)
                        for s in para:
                            if s not in key_word:
                                cons_para = cons_para + s
                        constructor.append(cons_para)
                        cons_startline = i + 1
                        constructor.append(cons_startline)
                        cons_fin = j
                        break
                for j in range(cons_fin+1, len(filter_df)):
                    if len(cons_deli_list)>=1:
                        if '{' in str(filter_df.iloc[j]['code']):
                            cons_deli_list.append('{')
                        if '}' in str(filter_df.iloc[j]['code']):
                            cons_deli_list.append('}')
                            if len(cons_deli_list)%2==0:
                                cons_endline = j+1
                                constructor.append(cons_endline)
                                constructor_df.loc[len(constructor_df)] = constructor
                                constructor = []
                                cons_deli_list = []
                                break
            else:
                reg = r'\((.*?)\)'
                cons_parameters = re.findall(reg, str(code))[0]
                cons_para = ''
                para = re.split(" ", cons_parameters)
                for s in para:
                    if s not in key_word:
                        cons_para = cons_para + s
                constructor.append(cons_para)
                # 获取构造函数开始行
                cons_startline = i + 1
                constructor.append(cons_startline)
                # 获取构造函数结束行
                if '{' in str(code):
                    cons_deli_list_tmp = ['{']
        if len(cons_deli_list_tmp) == 1 and str(code).endswith('}'):
            cons_endline = i + 1
            constructor.append(cons_endline)
            cons_deli_list_tmp = []
        if len(constructor) == 4:
            constructor_df.loc[len(constructor_df)] = constructor
            constructor = []
    return contract_df, function_df, constructor_df

def genDataset(filename, dataset_filename, function_df, contract_df, constructor_df):
    # dataset_file = open(dataset_filename,'a+')
    filter_df = pd.read_csv(filename, sep='\t', names=['code', 'line_number'])
    #函数分片
    for j in range(len(function_df)):
        func_startline = function_df.iloc[j]['startline']
        func_endline = function_df.iloc[j]['endline']
        func_subdata = filter_df[func_startline-1:func_endline]
        if func_startline==func_endline:
            func_subdata = filter_df[func_startline-1:func_endline]
        l = ['','']
        func_subdata_tmp = func_subdata.copy()
        func_subdata_tmp.loc[len(func_subdata)+2] = l
        func_subdata_tmp.to_csv(dataset_filename, header=None, mode='a',index=None, sep='\t')
    #构造函数分片
    for k in range(len(constructor_df)):
        cons_startline = constructor_df.iloc[k]['startline']
        cons_endline = constructor_df.iloc[k]['endline']
        cons_subdata = filter_df[cons_startline-1:cons_endline]
        if cons_startline==cons_endline:
            cons_subdata = filter_df[cons_startline-1:cons_endline]
        l = ['','']
        cons_subdata_tmp = cons_subdata.copy()
        cons_subdata_tmp.loc[len(cons_subdata)+2] = l
        cons_subdata_tmp.to_csv(dataset_filename, header=None, mode='a',index=None, sep='\t')
    #合约分片
    for i in range(len(contract_df)):
        cont_startline = contract_df.iloc[i]['startline']
        cont_endline = contract_df.iloc[i]['endline']
        cont_subdata = filter_df[cont_startline-1:cont_endline]
        if cont_startline == cont_endline:
            cont_subdata = filter_df[cont_startline - 1:cont_endline]
        #函数分片
        for j in range(len(function_df)):
            func_startline = function_df.iloc[j]['startline']
            func_endline = function_df.iloc[j]['endline']
            func_subdata = filter_df[func_startline-1:func_endline]
            if func_startline==func_endline:
                func_subdata = filter_df[func_startline-1:func_endline]
            # 从合约片段中去掉函数片段
            if func_startline > cont_startline and func_endline < cont_endline:
                num_list = func_subdata['line_number'].tolist()
                for num in num_list:
                    cont_subdata = cont_subdata[~(cont_subdata['line_number'].isin([num]))]
        #构造函数分片
        for k in range(len(constructor_df)):
            cons_startline = constructor_df.iloc[k]['startline']
            cons_endline = constructor_df.iloc[k]['endline']
            cons_subdata = filter_df[cons_startline-1:cons_endline]
            if cons_startline==cons_endline:
                cons_subdata = filter_df[cons_startline-1:cons_endline]
            #从合约片段中去掉构造函数片段
            if cons_startline > cont_startline and cons_endline < cont_endline:
                num_list = cons_subdata['line_number'].tolist()
                for num in num_list:
                    cont_subdata = cont_subdata[~(cont_subdata['line_number'].isin([num]))]
        if len(cont_subdata)>2:
            l = ['', '']
            cont_subdata_tmp = cont_subdata.copy()
            cont_subdata_tmp.loc[len(cont_subdata) + 2] = l
            cont_subdata_tmp.to_csv(dataset_filename, header=None, mode='a',index=None, sep='\t')

def transDataset(dataset_filename, fin_dataset_filename):
    fin_dataset_file = open(fin_dataset_filename, 'a+')
    line_list = []
    id_list = []
    with open(dataset_filename,'r') as f:
        line = f.readline()
        while line:
            if line.split('\t')[0]=='':
                code = ' '.join(line_list)
                id = ','.join(id_list)
                fin_dataset_file.write(code+'\t'+id+'\n')
                line_list = []
                id_list = []
                line = f.readline()
                continue
            l = line.strip().split('\t')
            line_list.append(l[0])
            id_list.append(l[1])
            line = f.readline()
    fin_dataset_file.close()

if __name__ == '__main__':
    # source_file = sys.argv[1]
    source_file = "/Users/zhaofangyu/Desktop/scanner_sourcecode/DLscanner/genDataset/test_data/test_file.sol"
    tmp_file = source_file+'.tmp'
    filter_file = source_file+'.filter'
    dataset_file = source_file+'.dataset'
    fin_dataset_file = source_file+'.res.dataset'

    readfile(source_file)
    filterResouce(tmp_file, filter_file)
    contract_df, function_df, constructor_df = genCNT_struct(filter_file, dataset_file)
    genDataset(filter_file, dataset_file,function_df, contract_df, constructor_df)
    # transDataset(dataset_file, fin_dataset_file)


