import json, sys
sys.stdout.reconfigure(encoding='utf-8')

DATA_PATH = r"C:\Users\신도경\Desktop\업무 파일\03_클로드 코드\GIT\admission-search\data.json"

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

changes = 0

for entry in data["고른기회"]:
    if entry.get("대학명") == "중앙대" and entry.get("전형유형") == "농어촌":
        entry["모집인원"] = "141(정원내71+정원외70)"
        print(f"  중앙대/농어촌: 모집인원 -> 141")
        changes += 1

    if entry.get("대학명") == "전북대" and entry.get("전형유형") == "지역인재":
        entry["전형구분"] = "교과+종합"
        entry["모집인원"] = "지역인재1유형691+2유형146+기회균형77=914"
        entry["전형방법"] = "교과:학생부/종합:서류평가"
        entry["최저유무"] = "O(지역인재)/X(기회균형)"
        entry["최저내용"] = "지역인재O/기회균형X"
        print(f"  전북대/지역인재: 5필드 업데이트")
        changes += 5

    if entry.get("대학명") == "서강대" and entry.get("전형유형") == "기초생활":
        entry["모집인원"] = "24"
        print(f"  서강대/기초생활: 모집인원 -> 24")
        changes += 1

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{changes}건 추가 수정 완료")
