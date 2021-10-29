import os
import os.path
import re
import io
import sys, fileinput

ex_list = []
def to_merged(root_dir):
    global ex_list
    for files in os.listdir(root_dir):
        path = os.path.join(root_dir, files)
        ext = os.path.splitext(files)[-1]
        if ext != '.txt':
            if os.path.isdir(path):
               to_merged(path)
        elif ext == '.txt':
            if os.path.isdir(path):
                to_merged(path)
            if "merged" in files:
                merged_name = files.replace("_merged.txt", "")
                f = open(path, 'r', encoding='UTF8')
                readline = f.read()
                if "이야 \n" in readline:
                  ex_list.append(files)

root_dir = 'C:/Users/tmddn/OneDrive/바탕 화면/수원고법/'
to_merged(root_dir) # 이야 파일 list에 추가


for i in range(len(ex_list)):
    re_name = ex_list[i].replace("_merged.txt", "")
    full_dir = root_dir + re_name + "/results/" + ex_list[i]

    fin = open(full_dir, "rt", encoding="UTF8")
    fout = open(root_dir + re_name + "/results/merged.txt", "wt", encoding="UTF8")

    for line in fin:
        fout.write(line.replace('이야', '이유'))
    fin.close()
    fout.close()
    os.remove(full_dir)
    print(full_dir)
    os.rename(root_dir + re_name + "/results/merged.txt", full_dir)
