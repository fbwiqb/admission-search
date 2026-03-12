import json, sys, copy
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\신도경\Desktop\업무 파일\03_클로드 코드\GIT\admission-search\data.json'
d = json.load(open(path, 'r', encoding='utf-8'))

jonghap_info = {
    ('서울대','의예과'): {'전형명': '일반전형/지역균형', '면접유무': 'O', '2차전형': '면접'},
    ('연세대','의예과'): {'전형명': '활동우수형', '면접유무': 'O', '2차전형': '면접'},
    ('고려대','의예과'): {'전형명': '계열적합형/학업우수형', '면접유무': 'O', '2차전형': '면접'},
    ('성균관대','의예과'): {'전형명': '과학인재/탐구형인재', '면접유무': 'O', '2차전형': '면접'},
    ('울산대','의예과'): {'전형명': '학생부종합', '면접유무': 'O', '2차전형': 'MMI면접'},
    ('가톨릭대','의예과'): {'전형명': '학교장추천/가톨릭지도자추천', '면접유무': 'O', '2차전형': '인적성면접'},
    ('한양대','의예과'): {'전형명': '면접형/서류형', '면접유무': 'O', '2차전형': '면접'},
    ('중앙대','의학부'): {'전형명': '탐구형인재/성장형인재', '면접유무': 'O', '2차전형': '서류확인면접'},
    ('경희대','의예과'): {'전형명': '네오르네상스', '면접유무': 'O', '2차전형': '제시문면접'},
    ('이화여대','의예과'): {'전형명': '면접형/서류형', '면접유무': 'O', '2차전형': '면접'},
    ('가천대','의예과'): {'전형명': '가천의약학', '면접유무': 'O', '2차전형': '면접'},
    ('아주대','의예과'): {'전형명': 'ACE전형', '면접유무': 'O', '2차전형': '면접'},
    ('인하대','의예과'): {'전형명': '인하미래인재', '면접유무': 'O', '2차전형': '면접'},
    ('부산대','의예과'): {'전형명': '학생부종합/지역인재', '면접유무': 'O', '2차전형': '면접'},
    ('경북대','의예과'): {'전형명': '학생부종합/지역인재', '면접유무': 'O', '2차전형': '면접'},
    ('건국대(글)','의예과'): {'전형명': 'KU자기추천', '면접유무': 'O', '2차전형': '면접'},
    ('한림대','의예과'): {'전형명': '학생부종합', '면접유무': 'O', '2차전형': 'MMI면접'},
    ('부산대','약학부'): {'전형명': '학생부종합/지역인재', '면접유무': 'O', '2차전형': '면접'},
    ('가천대','약학과'): {'전형명': '가천의약학', '면접유무': 'O', '2차전형': '면접'},
    ('삼육대','약학과'): {'전형명': '세움인재', '면접유무': 'O', '2차전형': '면접'},
    ('경희대','치의예과'): {'전형명': '네오르네상스', '면접유무': 'O', '2차전형': '제시문면접'},
    ('경북대','치의예과'): {'전형명': '학생부종합/지역인재', '면접유무': 'O', '2차전형': '면접'},
    ('경희대','한의예과'): {'전형명': '네오르네상스', '면접유무': 'O', '2차전형': '제시문면접'},
    ('원광대','한의예과'): {'전형명': '학생부종합', '면접유무': 'O', '2차전형': '면접'},
    ('가천대','한의예과'): {'전형명': '가천의약학', '면접유무': 'O', '2차전형': '면접'},
    ('건국대','수의예과'): {'전형명': 'KU자기추천', '면접유무': 'O', '2차전형': '면접'},
    ('경북대','수의예과'): {'전형명': '학생부종합/지역인재', '면접유무': 'O', '2차전형': '면접'},
}

new_list = []
added_jonghap = set()

for item in d['의약학']:
    univ = item['대학명']
    dept = item.get('학과', '')
    typ = item.get('전형유형', '')
    key = (univ, dept)

    if typ == '종합/논술':
        jonghap = copy.deepcopy(item)
        jonghap['전형유형'] = '종합'
        jonghap['전형구분'] = '종합'
        if key in jonghap_info:
            info = jonghap_info[key]
            jonghap['전형명'] = info['전형명']
            jonghap['면접유무'] = info['면접유무']
            jonghap['2차전형'] = info['2차전형']
        new_list.append(jonghap)
        added_jonghap.add(key)

        nonsul = copy.deepcopy(item)
        nonsul['전형유형'] = '논술'
        nonsul['전형구분'] = '논술'
        nonsul['전형명'] = '논술전형'
        new_list.append(nonsul)

    elif typ == '논술':
        new_list.append(item)

        if key in jonghap_info and key not in added_jonghap:
            jonghap = copy.deepcopy(item)
            jonghap['전형유형'] = '종합'
            jonghap['전형구분'] = '종합'
            info = jonghap_info[key]
            jonghap['전형명'] = info['전형명']
            jonghap['면접유무'] = info['면접유무']
            jonghap['2차전형'] = info['2차전형']
            jonghap['면접유형'] = ''
            jonghap['모집인원'] = ''
            new_list.append(jonghap)
            added_jonghap.add(key)

    elif typ == '종합':
        new_list.append(item)
        added_jonghap.add(key)
    else:
        new_list.append(item)

d['의약학'] = new_list
json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(f'의약학 항목: {len(d["의약학"])}개 (기존 27개)')
print()
type_count = {}
for item in d['의약학']:
    t = item.get('전형유형','')
    type_count[t] = type_count.get(t, 0) + 1
print('전형유형 분포:', type_count)
print()
for item in d['의약학']:
    print(f"  {item['대학명']} {item.get('학과','')} | {item.get('전형유형','')} | {item.get('전형명','')}")
