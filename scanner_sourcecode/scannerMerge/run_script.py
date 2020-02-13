import logging
import os,json,time,sys
import subprocess
# from progressbar import *
# from tqdm import *

filename=input("Please input filePath: ")

print('--------------------------------------------------------------')
print('Mythril scanning....')
# progress = ProgressBar()
# for i in progress(range(10)):
#     time.sleep(1)
cmd1="/home/minelab/anaconda3/bin/myth -x --solv 0.4.24 "+filename+"> res_file/mythril_res.txt"
pipe1=subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
pipe1.communicate()

print('--------------------------------------------------------------')
print('Oyente scanning....')
# progress = ProgressBar()
# for i in progress(range(10)):
#     time.sleep(1)
cmd2="(python /home/minelab/contracts_scanners/oyente/oyente/oyente.py -s "+filename+")"+" 2> res_file/oyente_res.txt"
pipe2=subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
pipe2.communicate()

print('--------------------------------------------------------------')
print('Slither scanning....')
# progress = ProgressBar()
# for i in progress(range(10)):
#     time.sleep(1)
cmd3="(/home/minelab/anaconda3/bin/slither "+filename+")"+" 2> res_file/slither_res.txt"
pipe3=subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
pipe3.communicate()

# print('--------------------------------------------------------------')
# print('Securify scanning....')
# progress = ProgressBar()
# for i in progress(range(10)):
#     time.sleep(1)
# cmd4="cd securify/securify-master && (java -jar build/libs/securify-0.1.jar -fs "+"../../"+filename+")"+" 2> ../../res_file/securify_res.txt"
# pipe=subprocess.Popen(cmd4, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
'''
for i in range(1000000):
    log1 = logging.info(subprocess.Popen.poll(pipe1))
    log2 = logging.info(subprocess.Popen.poll(pipe2))
    log3 = logging.info(subprocess.Popen.poll(pipe3))
    print(log1,log2,log3)
    if log1==0 and log2==0 and log3==0:
        break
    time.sleep(1)
'''
os.system("python2 main.py")
