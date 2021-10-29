import os
import re
import json
from collections import OrderedDict
from final_ocr2 import final_ocr

struct_list = []
res_list = []
def recursion(root_dir):
    global struct_list, res_list
    for files in os.listdir(root_dir):
        path = os.path.join(root_dir, files)
        ext = os.path.splitext(files)[-1]
        if ext != '.txt':
            if os.path.isdir(path):
                recursion(path)
                if "results" in files:
                    res_list.append(path)
        elif ext == '.txt':
            if os.path.isdir(path):
                recursion(path)

            if "merged" in files:
                struct_list.append(files)

    return struct_list, res_list

root_dir = 'C:/Users/tmddn/OneDrive/바탕 화면/수원고법/'

st_root, pre_root = recursion(root_dir)

for i in range(len(st_root)):
    final_ocr(pre_root[i], st_root[i])
    print(pre_root[i], st_root[i], "Done")