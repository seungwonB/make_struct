import os
import re
import json
from collections import OrderedDict

# file_path = 'C:/Users/tmddn/Downloads/살인_JSON-20210809T051956Z-001/살인_JSON/대구지법_2014고합260_판결서/results'

def final_ocr(root_dir, f_name):
    f = open(root_dir + "/" + f_name, 'r', encoding='UTF8')

    readline = ''.join(list(f))
    court_name = re.findall(r'\w*법원\w*', readline)

    court_num1 = re.findall(r"법원", readline)
    idx_cn1 = readline.index(court_num1[0])
    court_num2 = re.findall(r"판결", readline)
    idx_cn2 = readline.index(court_num2[0])
    court_num = readline[idx_cn1 + 3:idx_cn2]

    # if len(re.findall(r'\w*사부\w*', readline)) != 0:
    #     court_num = re.findall(r'\w*사부\w*', readline)
    # else:
    #     court_num = ["Null"]

    # if len(re.findall(r'\w*고합\w*', readline)) != 0:
    #     case_num = re.findall(r'\w*고합\w*', readline)
    # elif len(re.findall(r'\w*고단\w*', readline)) != 0:
    #     case_num = re.findall(r'\w*고단\w*', readline)

    case_n = re.findall(r"사건", readline)
    idx_casenum = readline.index(case_n[0])

    def_num = re.findall(r"피고인", readline)
    idx_def = readline.index(def_num[0])

    case_num = readline[idx_casenum:idx_def]
    case_num = case_num.replace("사건","")

    # defendant = re.findall(r'피고인[^A-Z]*', readline)
    # idx_defendant = readline.index(defendant[0])
    # len_def = len(defendant[0])
    defendant1 = re.findall(r"피고인", readline)
    idx_defendant1 = readline.index(defendant1[0])
    try:
        defendant2 = re.findall(r"항소인", readline)
        idx_defendant2 = readline.index(defendant2[0])
    except:
        defendant2 = re.findall(r"검사", readline)
        idx_defendant2 = readline.index(defendant2[0])

    defendant = readline[idx_defendant1:idx_defendant2]
    defendant = defendant.replace("피고인", "")

    try:
        appellant1 = re.findall(r"항소인", readline)
        idx_appellant1 = readline.index(appellant1[0])
        appellant2 = re.findall(r"\n검사", readline)
        idx_appellant2 = readline.index(appellant2[0])

        appellant = readline[idx_appellant1:idx_appellant2]
        appellant = appellant.replace("항소인", "")

    except:
        appellant = "Null"


    prosecutor = re.findall(r'\w*기소\w*', readline)
    idx_prosecutor = readline.index(prosecutor[0])
    try:
        prosecutor2 = re.findall(r'\w*공판\w*', readline)
        idx_prosecutor2 = readline.index(prosecutor2[0])
    except:
        prosecutor2 = re.findall(r'\w*공\n판\w*', readline)
        idx_prosecutor2 = readline.index(prosecutor2[0])


    origin = "원심판결"
    try:
        idx_original1 = readline.index(origin)
    except:
        origin = "제1심판결"
        idx_original1 = readline.index(origin)

    #original1 = re.findall(r"원심판결", readline)
    #idx_original1 = readline.index(original1[0])
    original2 = re.findall(r"판결선고", readline)
    idx_original2 = readline.index(original2[0])
    original = readline[idx_original1:idx_original2]
    original = original.replace(origin,"")

    #defense = re.findall(r'변호사[^\n]+', readline)
    try:
        defense_name = re.findall(r"변호인", readline)
        idx_defense = readline.index(defense_name[0])
        case_date_defense = re.findall(origin, readline)

        idx_cd = readline.index(case_date_defense[0])

        defense = readline[idx_defense:idx_cd]
        if "변호인" in defense:
            defense = defense.replace("변호인", "")
    except:
        defense = "Null"

    case_date = re.findall(r'판결선고[^\n]+', readline)
    case_date = case_date[0].replace("판결선고", "")
    case_summary = re.findall(r'주문', readline)
    idx_summary = readline.index(case_summary[0])
    case_summary2 = re.findall(r'이유', readline)
    idx_summary2 = readline.index(case_summary2[0])
    case_main = re.findall(r'이유', readline)
    idx_main = readline.index(case_main[0])
    try:
        case_main2 = re.findall(r'재판장', readline)
        idx_main2 = readline.index(case_main2[0])
    except:
        case_main2 = re.findall(r'판사', readline)
        idx_main2 = readline.index(case_main2[0])

    judge = re.findall(r'판사[^"]+', readline)
    idx_jud = readline.index(judge[0])
    if judge[0].find("준수사항") > 1:
        idx_judge = judge[0].index("준수사항")
        judge[0] = readline[idx_jud:idx_jud+idx_judge]

    input_files = os.listdir(root_dir)
    foot_list = []
    for file_name in input_files:
        if "주석.txt" in file_name:
            f2 = open(root_dir + '/' + file_name, 'r')
            read_f = ''.join(list(f2))
            foot_list.append(read_f)


    if len(foot_list) == 1:
        case_footnote = foot_list[0]
    else:
        case_footnote = foot_list

    file_data = OrderedDict()
    file_data["court_name"] = court_name[0]
    file_data["court_num"] = court_num
    file_data["case_info"] = {'case_num':court_name[0]+case_num,
                              'defendant':defendant,
                              'appellant':appellant,
                              'prosecutor':readline[idx_prosecutor-4:idx_prosecutor2+3],
                              'defense':defense,
                              'original':original,
                              'case_date':case_date
                              }
    file_data["case_summary"] = readline[idx_summary:idx_summary2]
    file_data["case_main"] = readline[idx_main:idx_main2]
    file_data["judge"] = judge[0]
    file_data["case_footnote"] = case_footnote

    #print(json.dumps(file_data, ensure_ascii=False, indent="\t"))


    st_name = f_name.replace("_merged.txt", "_struct.json")

    with open(root_dir + "/" +st_name, 'w', encoding='utf-8') as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent="\t")

