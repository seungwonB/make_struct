import os
import re
import json
from collections import OrderedDict

# file_path = 'C:/Users/tmddn/Downloads/살인_JSON-20210809T051956Z-001/살인_JSON/대구지법_2014고합260_판결서/results'

def final_ocr(root_dir, f_name):
    f = open(root_dir + "/" + f_name, 'r', encoding='UTF8')
    readline = ''.join(list(f))

    # court_name 추출 - 법원이 속해있는 단어
    court_name = re.findall(r'\w*법원\w*', readline)

    # court_num 추출 - 법원[0]과 판결[0] 사이의 문장
    court_num1 = re.findall(r"법원", readline) # 법원을 찾고
    idx_cn1 = readline.index(court_num1[0]) # 찾은 list의 0번째 원소 index
    court_num2 = re.findall(r"판결", readline) # 판결을 찾고
    idx_cn2 = readline.index(court_num2[0]) # 찾은 list의 0번째 원소 index
    court_num = readline[idx_cn1 + 3 : idx_cn2] # 둘 사의의 문장 추출

    # case_num 추출 - 사건[0]과 피고인[0] 사이의 문장
    case_n = re.findall(r"사건", readline)
    idx_casenum = readline.index(case_n[0])
    try: # 피고인이 대부분이지만
        def_num = re.findall(r"피고인", readline)
        idx_def = readline.index(def_num[0])
    except: # 간혹 피감호청구인이라 나오는 경우 예외처리
        def_num = re.findall(r"피감호청구인", readline)
        idx_def = readline.index(def_num[0])
    case_num = readline[idx_casenum:idx_def]
    case_num = case_num.replace("사건","")

    # defendant 추출
    defendant = re.findall(r'피고인[^A-Z]*', readline)
    idx_defendant = readline.index(defendant[0])
    len_def = len(defendant[0])

    # prosecutor 추출
    prosecutor = re.findall(r'\w*기소\w*', readline)
    idx_prosecutor = readline.index(prosecutor[0])
    try:
        prosecutor2 = re.findall(r'\w*공판\w*', readline)
        idx_prosecutor2 = readline.index(prosecutor2[0])
    except: # 예외처리
        prosecutor2 = re.findall(r'\w*공\n판\w*', readline)
        idx_prosecutor2 = readline.index(prosecutor2[0])

    # defense 추출
    try:
        defense_name = re.findall(r"변호인", readline)
        idx_defense = readline.index(defense_name[0])
        case_date_defense = re.findall(r"판결선고", readline)
        idx_cd = readline.index(case_date_defense[0])

        defense = readline[idx_defense:idx_cd]
        if "변호인" in defense:
            defense = defense.replace("변호인", "")
    except: # 없는 경우
        defense = "Null"

    # case_date 추출
    case_date = re.findall(r'판결선고[^\n]+', readline)
    case_date = case_date[0].replace("판결선고", "")

    # case_summary 추출
    case_summary = re.findall(r'주문', readline)
    idx_summary = readline.index(case_summary[0])
    case_summary2 = re.findall(r'이유', readline)
    idx_summary2 = readline.index(case_summary2[0])

    # case_main 추출
    case_main = re.findall(r'이유', readline)
    idx_main = readline.index(case_main[0])
    try:
        case_main2 = re.findall(r'재판장', readline)
        idx_main2 = readline.index(case_main2[0])
    except: # 예외처리
        case_main2 = re.findall(r'판사', readline)
        idx_main2 = readline.index(case_main2[0])

    # judge 추출
    judge = re.findall(r'판사[^"]+', readline)
    idx_jud = readline.index(judge[0])
    if judge[0].find("준수사항") > 1: # 준수사항 내용 날려버리기
        idx_judge = judge[0].index("준수사항")
        judge[0] = readline[idx_jud:idx_jud+idx_judge]

    # case_footnote 추출
    input_files = os.listdir(root_dir)
    foot_list = []
    for file_name in input_files:
        if "주석.txt" in file_name:
            f2 = open(root_dir + '/' + file_name, 'r')
            read_f = ''.join(list(f2))
            foot_list.append(read_f)
            
    if len(foot_list) == 1: # 주석이 하나 있는 경우는 보기 좋게 str로 출력하기 위함
        case_footnote = foot_list[0]
    else:
        case_footnote = foot_list

    # json 형태로 저장
    file_data = OrderedDict()
    file_data["court_name"] = court_name[0]
    file_data["court_num"] = court_num
    file_data["case_info"] = {'case_num':court_name[0]+case_num,
                              'defendant':readline[idx_defendant+len_def],
                              'prosecutor':readline[idx_prosecutor-4:idx_prosecutor2+3],
                              'defense':defense,
                              'case_date':case_date
                              }
    file_data["case_summary"] = readline[idx_summary:idx_summary2]
    file_data["case_main"] = readline[idx_main:idx_main2]
    file_data["judge"] = judge[0]
    file_data["case_footnote"] = case_footnote

    # 출력해보기
    #print(json.dumps(file_data, ensure_ascii=False, indent="\t"))

    # 파일로 저장하기
    st_name = f_name.replace("_merged.txt", "_struct.json")

    with open(root_dir + "/" +st_name, 'w', encoding='utf-8') as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent="\t")

