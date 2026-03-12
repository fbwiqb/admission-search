import json, sys, copy
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\신도경\Desktop\업무 파일\03_클로드 코드\GIT\admission-search\data.json'
d = json.load(open(path, 'r', encoding='utf-8'))
backup = copy.deepcopy(d)

changes = []

def log(sheet, univ, field, old, new):
    changes.append(f"[{sheet}] {univ}: {field} '{old}' → '{new}'")

# === 수시_교과 ===
for item in d['수시_교과']:
    if item['대학명'] == '고려대':
        old = item['전형방법']
        item['전형방법'] = '교과90%+서류10%'
        log('수시_교과', '고려대', '전형방법', old, item['전형방법'])

        old = item['최저내용']
        item['최저내용'] = '국수영탐(탐구1과목) 4합7이내, 한국사4이내'
        log('수시_교과', '고려대', '최저내용', old, item['최저내용'])

        old = item.get('2027변경사항', '')
        item['2027변경사항'] = '★교과90%+서류10%(비교과→서류), 최저4합7(탐구1과목)'
        log('수시_교과', '고려대', '2027변경사항', old, item['2027변경사항'])

# === 수시_종합 ===
for item in d['수시_종합']:
    if item['대학명'] == '서강대' and '일반I' in item.get('전형명', ''):
        old_m = item.get('면접유무', '')
        old_2 = item.get('2차전형', '')
        item['면접유무'] = 'O'
        item['2차전형'] = '면접'
        log('수시_종합', '서강대 일반I', '면접유무', old_m, 'O')
        log('수시_종합', '서강대 일반I', '2차전형', old_2, '면접')

# === 논술 ===
for item in d['논술']:
    if item['대학명'] == '동덕여대':
        old = item.get('최저내용', '')
        item['최저내용'] = '2합6이내'
        log('논술', '동덕여대', '최저내용', old, item['최저내용'])

        old = item.get('2027변경사항', '')
        item['2027변경사항'] = '★최저강화(2합7→2합6)'
        log('논술', '동덕여대', '2027변경사항', old, item['2027변경사항'])

# === 정시 모집군 ===
jeongsi_groups = {
    '경희대': '나',
    '한국외대': '나',
    '이화여대': '가',
    '부산대': '가/나',
    '전남대': '가/나',
    '충남대': '가/나',
}
for item in d['정시']:
    if item['대학명'] in jeongsi_groups and item.get('모집군') == '-':
        old = item['모집군']
        item['모집군'] = jeongsi_groups[item['대학명']]
        log('정시', item['대학명'], '모집군', old, item['모집군'])

# === 정시 한양대 반영비율 ===
for item in d['정시']:
    if item['대학명'] == '한양대':
        old_kuk = item.get('국어비율', '')
        old_su = item.get('수학비율', '')
        old_eng = item.get('영어반영', '')
        old_tam = item.get('탐구비율', '')
        item['국어비율'] = '인문35/자연25'
        item['수학비율'] = '인문30/자연40'
        item['영어반영'] = '10%'
        item['탐구비율'] = '인문25/자연25'
        log('정시', '한양대', '국어비율', old_kuk, item['국어비율'])
        log('정시', '한양대', '수학비율', old_su, item['수학비율'])
        log('정시', '한양대', '영어반영', old_eng, item['영어반영'])
        log('정시', '한양대', '탐구비율', old_tam, item['탐구비율'])

# === 의약학 빈칸 채우기 ===
for item in d['의약학']:
    univ = item['대학명']
    dept = item.get('학과', '')

    if univ == '성균관대' and '의예' in dept:
        if not item.get('사탐허용(정시)'):
            item['사탐허용(정시)'] = 'X(과탐only, 가산5%)'
            log('의약학', f'{univ} {dept}', '사탐허용(정시)', '', item['사탐허용(정시)'])

    elif univ == '울산대' and '의예' in dept:
        if not item.get('사탐허용(수시)'):
            item['사탐허용(수시)'] = 'X'
            log('의약학', f'{univ} {dept}', '사탐허용(수시)', '', 'X')
        if not item.get('사탐허용(정시)'):
            item['사탐허용(정시)'] = 'X'
            log('의약학', f'{univ} {dept}', '사탐허용(정시)', '', 'X')

    elif univ == '가톨릭대' and '의예' in dept:
        if not item.get('사탐허용(수시)'):
            item['사탐허용(수시)'] = 'O'
            log('의약학', f'{univ} {dept}', '사탐허용(수시)', '', 'O')

    elif univ == '한양대' and '의예' in dept:
        if not item.get('면접유형'):
            item['면접유형'] = '2단계면접(서류→면접)'
            log('의약학', f'{univ} {dept}', '면접유형', '', item['면접유형'])

    elif univ == '중앙대' and '의' in dept:
        if not item.get('면접유형'):
            item['면접유형'] = '2단계면접(서류70%+면접30%)'
            log('의약학', f'{univ} {dept}', '면접유형', '', item['면접유형'])

    elif univ == '경희대' and '의예' in dept:
        if not item.get('면접유형'):
            item['면접유형'] = '제시문면접'
            log('의약학', f'{univ} {dept}', '면접유형', '', item['면접유형'])

    elif univ == '이화여대' and '의예' in dept:
        if not item.get('면접유형'):
            item['면접유형'] = '서류기반면접'
            log('의약학', f'{univ} {dept}', '면접유형', '', item['면접유형'])

    elif univ == '아주대' and '의예' in dept:
        if not item.get('사탐허용(정시)'):
            item['사탐허용(정시)'] = 'O'
            log('의약학', f'{univ} {dept}', '사탐허용(정시)', '', 'O')

    elif univ == '인하대' and '의예' in dept:
        if not item.get('사탐허용(정시)'):
            item['사탐허용(정시)'] = 'O(과탐 가산3~10%)'
            log('의약학', f'{univ} {dept}', '사탐허용(정시)', '', item['사탐허용(정시)'])

    elif univ == '가천대' and '의예' in dept:
        if not item.get('면접유형'):
            item['면접유형'] = '2단계면접(인성+적합성+의사소통)'
            log('의약학', f'{univ} {dept}', '면접유형', '', item['면접유형'])
        if not item.get('사탐허용(수시)'):
            item['사탐허용(수시)'] = 'X'
            log('의약학', f'{univ} {dept}', '사탐허용(수시)', '', 'X')
        if not item.get('사탐허용(정시)'):
            item['사탐허용(정시)'] = 'X(과탐2과목)'
            log('의약학', f'{univ} {dept}', '사탐허용(정시)', '', item['사탐허용(정시)'])

    elif '건국대' in univ and '의예' in dept:
        if not item.get('면접유형'):
            item['면접유형'] = '면접(확인필요)'
            log('의약학', f'{univ} {dept}', '면접유형', '', item['면접유형'])

    elif univ == '한림대' and '의예' in dept:
        if not item.get('면접유형'):
            item['면접유형'] = 'MMI(인성+상황+모의상황)'
            log('의약학', f'{univ} {dept}', '면접유형', '', item['면접유형'])

# === 한국외대 정시 영어기준 ===
for item in d['정시']:
    if item['대학명'] == '한국외대' and not item.get('영어기준'):
        item['영어기준'] = '최저포함(추정)'
        log('정시', '한국외대', '영어기준', '', item['영어기준'])

# === Save ===
json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(f"총 {len(changes)}건 수정 완료:")
print()
for c in changes:
    print(f"  {c}")
