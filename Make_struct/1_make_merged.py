import os
import os.path
import json
import re

# 파일 경로
path = 'C:/Users/tmddn/OneDrive/바탕 화면/춘천지법/'

# page + 번호를 나타내는 i, ex) page1, page2
i = 0

# page1, page2 ... page11, page12 이렇게 page가 10을 넘어가는 경우
# merge를 하게 되면 page1 다음에 page2가 아닌 page10이 옴 
# 때문에 page1 다음 page2가 오게 하기 위하여 정렬하는 함수
def solution(files):
    global i
    answer = []
    list_sort = []
    for filename in files:
        # 판결서_page1.txt 파일만 검사하고 나머지는 다 pass하기 위함
        if ".txt" not in filename: # 파일이 txt가 아니면 제외
            continue
        elif "주석" in filename: # 주석이면 제외
            continue
        elif "문장정리" in filename: # 문장정리면 제외
            continue
        elif "merged" in filename: # merged면 제외
            continue
        ft = re.findall(r'page', filename) # 파일이름에서 page를 찾아
        ftxt = re.findall(r'txt', filename) # txt를 찾아
        index_ft = filename.index(ft[0]) # 찾은 page의 index를 찾아
        index_ftxt = filename.index(ftxt[0]) # 찾은 txt의 index를 찾아
        i += 1 # page 번호 증가
        sort_index = filename[index_ft+4:index_ftxt-1] # 그럼 숫자만 추출 돼, ex)1,2,3 .. 10,11,12
        answer.append(int(sort_index)) # 그 숫자들을 리스트에 담아서
        answer.sort() # 정렬

    for k in range(1, i+1):
        list_sort.append(filename[:index_ft]+"page"+str(k)+".txt") # 정상적인 순서로 파일이름 저☆장☆
    i = 0
    return list_sort

# page 하나하나를 merge 하는 함수
def textA(directory, o_name):
    # 결과 파일 생성
    out_file = open(o_name, 'w', encoding='UTF-8')

    # 폴더 내용물 목록 생성
    input_files = os.listdir(directory)
    # 정렬된 파일
    res_solution = solution(input_files)

    # 폴더 내용을 하나하나 읽어 하나로 합치는 반복문
    for filename in res_solution:
        # 텍스트 확장자가 아닌파일 걸러내기
        if ".txt" not in filename:
            continue
            
        # 파일 열기
        file = open(directory + "/" + filename, encoding='cp949')

        # 파일 내용 문자열로 저장
        content = file.read()
        # 문자열로 저장된 내용을 파일에 쓰기
        out_file.write(content)

        # 읽은 파일 종료 (저장)
        file.close()

    # 결과 파일 종료 (저장)
    out_file.close()

# 모든 폴더를 반복하는 함수
def to_merged(root_dir):
    for files in os.listdir(root_dir):
        path = os.path.join(root_dir, files)
        ext = os.path.splitext(files)[-1]
        if ext != '.txt':
            if ext == '.json': # json파일 걸러주기
                pass
            elif ext == '.png': # png파일 걸러주기
                pass
            elif files == "results": # 폴더 걸러주기
                pass
            else:
                # _merged 파일 생성
                outfile_name = root_dir + files + "/results/" + files + "_merged.txt"
                textA(root_dir + files + "/results", outfile_name)
                print(path)
            if os.path.isdir(path):
               to_merged(path)
        elif ext == '.txt':
            if files == "merged.txt":
                # merged 된 거 확인하기 위해 출력. 
                # 오류난 것들은 찾아가며 수작업으로 고침.
                print(root_dir)
            if os.path.isdir(path):
                to_merged(path)

to_merged(path)
