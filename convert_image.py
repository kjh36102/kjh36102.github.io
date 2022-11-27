# ======== 페이지 정보 =============================
GITHUB_USER = 'kjh36102'
REPOSITORY_NAME = 'kjh36102.github.io'
BRANCH_NAME = 'master'
# ==================================================

import sys
import os
import re
import requests

file_path = sys.argv[1]
file_path = os.path.abspath(file_path)

if len(sys.argv) != 2:
    print('Args length not match')
    sys.exit()


#입력받은 경로에서 정보 추출
path_splits = file_path.split('\\')
path_splits.pop()
post_dir = path_splits.pop()
category = path_splits.pop()

URL_BASE = f'https://raw.githubusercontent.com/{GITHUB_USER}/{REPOSITORY_NAME}/{BRANCH_NAME}/_posts/{category}/{post_dir}/'

#파일 읽기
origin_file = open(file_path, 'r', encoding='utf-8')
origin_raw = origin_file.read()
origin_file.close()

#정규식으로 이미지부분만 가져오기
regex = '!\[.*\]\(.*\)'
find_list = re.findall(regex, origin_raw)

#변환 및 오류검출
cnt_success = 0
cnt_failed = 0

for elem in find_list:
    if 'https' in elem: continue

    tag_split = str.split(elem, '(')
    img_name = tag_split[1][:-1]
    
    print('\tTarget Image:', img_name, end='     ')

    converted_url = (URL_BASE + img_name).replace(' ', '%20')

    status_code = requests.get(converted_url).status_code

    if status_code == 200:
        origin_raw = origin_raw.replace(elem, tag_split[0] + '(' + converted_url + ') <!-- CONVERTED -->')
        cnt_success += 1
        print('...DONE')
    else :
        origin_raw = origin_raw.replace(elem, elem + ' <!-- ERROR -->')
        cnt_failed += 1
        print('...FAILED')

#파일에 쓰기
target_file = open(file_path, 'w', encoding='utf-8')
target_file.writelines(origin_raw)
target_file.close()

print(f'* Converting All Done!\t\tTOTAL: {cnt_success + cnt_failed}\tSUCCESS: {cnt_success}\tFAILED: {cnt_failed}')