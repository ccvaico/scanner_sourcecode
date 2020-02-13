# scanner_sourcecode
```
├── .DS_Store
├── .idea
│   ├── misc.xml
│   ├── modules.xml
│   ├── scanner_sourcecode.iml
│   └── workspace.xml
├── DLscanner               # 深度学习检测方法
│#使用整合扫描器扫描从以太坊上爬取的solidity源代码文件，将每个源代码扫描
│#结果保存在filename.sol.res文件中，filename为源代码文件名(新科研楼服务器
│#/home/minelab/zhaofangyu/DLscanner/genDataset目录下有shell脚本)
│   ├── .DS_Store
│   ├── __init__.py
│   ├── genDataset         # 生成数据集相关代码
│   │   ├── .DS_Store
│   │   ├── __init__.py
│   │   ├── genDataset.py #与.res文件对应为源代码分片打标签生成数据集
│   │   ├── lexer.py       #solidity源代码文件词性分析、分片
│   │   └── test_data      #测试数据目录
│   │       ├── .DS_Store
│   │       ├── test_file.sol   #源代码测试数据
│   │       └── test_file.sol.res  #源代码扫描结果
│   └── model               #模型训练相关代码
│       ├── 3embeddings-conv1d.ipynb   #CNN模型
│       ├── data_process.py              #数据处理代码
│       ├── embeddings-tfidf-lstm.ipynb  #embedding+tfidf的lstm模型
│       ├── model.py     #attention、双向LSTM/GRU模型函数
│       ├── test.csv     #测试集数据
│       ├── train.csv    #训练集数据
│       └── train.py     #模型训练代码
├── scannerMerge      #整合扫描器部分
│#mythril、oyente、slither三个扫描器安装在新科研楼服务器上，运行命令分别为：
│#mythril：/home/minelab/anaconda3/bin/myth -x --solv 0.4.24 filename 
│#oyente：python/home/minelab/contracts_scanners/oyente/oyente/oyente.py -s │#filename
│#slither：/home/minelab/anaconda3/bin/slither filename
│   ├── .DS_Store
│   ├── ScanDocker     #整合扫描器（取名为ScanDocker）
│   │   ├── .DS_Store
│   │   ├── .idea
│   │   │   ├── inspectionProfiles
│   │   │   │   └── profiles_settings.xml
│   │   │   ├── misc.xml
│   │   │   ├── modules.xml
│   │   │   ├── skynet.iml
│   │   │   └── workspace.xml
│   │   ├── app      #前端相关代码
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── migrations
│   │   │   │   └── __init__.py
│   │   │   ├── models.py
│   │   │   ├── tests.py
│   │   │   └── views.py
│   │   ├── db.sqlite3
│   │   ├── manage.py   #启动前端（python manage.py runserver 0.0.0.0:9001）
│   │   ├── skynet    #前端相关代码
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   └── wsgi.py
│   │   ├── static    #该目录下包含前端相关js文件（未全部显示）
│   │   │   └── .DS_Store
│   │   └── templates #该目录下包含前端相关静态html文件及图片等（未全部显示）
│   │       └── .DS_Store
│   ├── __init__.py
│   ├── main.py   #扫描器统一漏洞处理输出（主要运行代码）
│   ├── preprocessing.py   #扫描器漏洞预处理
│   ├── preprocessing.pyc
│   ├── res_file   #扫描器扫描结果文件
│   │   ├── mythril_res.txt
│   │   ├── oyente_res.txt
│   │   └── slither_res.txt
│   ├── run_script.py   #三个扫描器并行检测，调用main.py输出最终结果（服务器端主要运行代码）
│   ├── scanner_dict.py  #扫描器漏洞映射字典
│   ├── scanner_dict.pyc
│   └── server.py   #建立websocket连接，后台调用扫描器与漏洞输出代码，为前端上传扫描结果
└── text_clustering-master  #k-means聚类方法
    ├── .DS_Store
    ├── .gitignore
    ├── .idea
    │   ├── misc.xml
    │   ├── modules.xml
    │   ├── text_clustering-master.iml
    │   └── workspace.xml
    ├── __pycache__
    │   ├── k_means.cpython-36.pyc
    │   └── similarity.cpython-36.pyc
    ├── auto_cluster.py    #手肘法获取聚类的k值
    ├── auto_cluster.pyc
    ├── clustering.py      #聚类输出结果（主要运行代码）
    ├── k_means.py          #k_means实现
    ├── k_means.pyc
    ├── preprocessing.py   #扫描器漏洞预处理
    ├── preprocessing.pyc
    ├── scanner_dict.py     #扫描器漏洞映射字典
    ├── scanner_dict.pyc
    ├── scanner_res
    │   ├── .DS_Store
    │   ├── my_visibility_not_set.txt
    │   ├── oy_visibility_not_set.txt
    │   └── sl_visibility_not_set.txt
    ├── similarity.py   #相似度计算
    ├── similarity.pyc
    ├── vectorizer.py   #tf-idf实现，词向量转换
    └── vectorizer.pyc

```
