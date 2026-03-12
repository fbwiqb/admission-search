import json
import sys
import copy

sys.stdout.reconfigure(encoding='utf-8')

DATA_PATH = r"C:\Users\신도경\Desktop\업무 파일\03_클로드 코드\GIT\admission-search\data.json"

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

original_data = copy.deepcopy(data)
changes_log = []

def update_entry(sheet_name, match_criteria, updates):
    sheet = data.get(sheet_name, [])
    for i, entry in enumerate(sheet):
        matched = all(entry.get(k) == v for k, v in match_criteria.items())
        if matched:
            for field, new_value in updates.items():
                old_value = entry.get(field, "")
                if str(old_value) != str(new_value):
                    entry[field] = new_value
                    changes_log.append({
                        "sheet": sheet_name,
                        "idx": i,
                        "univ": entry.get("대학명", ""),
                        "field": field,
                        "old": old_value,
                        "new": new_value
                    })
            return True
    print(f"  ⚠ NOT FOUND: {sheet_name} / {match_criteria}")
    return False

def count_gaps(sheet_name, sheet_data, skip_fields=None):
    if skip_fields is None:
        skip_fields = {"출처"}
    total = 0
    empty = 0
    for entry in sheet_data:
        for k, v in entry.items():
            if k in skip_fields:
                continue
            total += 1
            if v == "" or v is None:
                empty += 1
    return empty, total


print("=" * 60)
print("BEFORE: 빈칸 현황 (변경 전)")
print("=" * 60)
sheets = ["수시_교과", "수시_종합", "논술", "정시", "교대", "고른기회", "경기권_국공립"]
before_gaps = {}
for s in sheets:
    e, t = count_gaps(s, original_data.get(s, []))
    pct = (e / t * 100) if t > 0 else 0
    before_gaps[s] = (e, t)
    print(f"  {s}: {e}/{t} 빈칸 ({pct:.1f}%)")

print("\n" + "=" * 60)
print("APPLYING CORRECTIONS...")
print("=" * 60)

# ===== Agent A: 수시_교과 =====
print("\n[Agent A] 수시_교과:")
update_entry("수시_교과", {"대학명": "성균관대", "전형명": "학교장추천"}, {"모집인원": "415"})
update_entry("수시_교과", {"대학명": "서울과기대", "전형명": "고교추천"}, {"모집인원": "509"})
update_entry("수시_교과", {"대학명": "가천대", "전형명": "학교장추천우수자"}, {"모집인원": "452"})

# ===== Agent A: 수시_종합 =====
print("\n[Agent A] 수시_종합:")
update_entry("수시_종합", {"대학명": "연세대", "전형명": "활동우수형"}, {"모집인원": "708"})
update_entry("수시_종합", {"대학명": "한양대", "전형명": "추천형"}, {"모집인원": "291"})
update_entry("수시_종합", {"대학명": "한양대", "전형명": "면접형"}, {"모집인원": "16"})
update_entry("수시_종합", {"대학명": "한국외대", "전형명": "면접형"}, {"모집인원": "487"})

# ===== Agent B: 논술 =====
print("\n[Agent B] 논술:")
update_entry("논술", {"대학명": "연세대"}, {"모집인원": "288"})
update_entry("논술", {"대학명": "경희대"}, {"모집인원": "471"})
update_entry("논술", {"대학명": "건국대"}, {"모집인원": "325"})
update_entry("논술", {"대학명": "동국대"}, {"모집인원": "280"})
update_entry("논술", {"대학명": "국민대"}, {"논술비율": "100%", "학생부비율": "0%"})
update_entry("논술", {"대학명": "가천대"}, {"논술비율": "100%", "학생부비율": "0%"})
update_entry("논술", {"대학명": "성신여대"}, {"논술비율": "100%", "학생부비율": "0%"})
update_entry("논술", {"대학명": "덕성여대"}, {"논술비율": "100%", "학생부비율": "0%"})
update_entry("논술", {"대학명": "삼육대"}, {
    "모집인원": "272",
    "논술비율": "100%",
    "학생부비율": "0%",
    "최저내용": "1개3등급이내(약학:국수과 3합5)",
    "최저유무": "O"
})
update_entry("논술", {"대학명": "서울과기대"}, {
    "최저내용": "2합7이내(2026기준)",
    "최저유무": "O"
})

# ===== Agent D: 고른기회 =====
print("\n[Agent D] 고른기회:")
update_entry("고른기회", {"대학명": "한양대"}, {"모집인원": "118(2026기준)"})
update_entry("고른기회", {"대학명": "전남대", "전형유형": "지역인재"}, {"모집인원": "1028"})
update_entry("고른기회", {"대학명": "충남대", "전형유형": "지역인재"}, {"모집인원": "662"})
update_entry("고른기회", {"대학명": "고려대", "전형유형": "사회배려"}, {
    "전형구분": "종합",
    "전형방법": "1단계:서류3배수→2단계:1단계60%+면접40%(2026기준)"
})

# ===== Agent D: 경기권_국공립 =====
print("\n[Agent D] 경기권_국공립:")
update_entry("경기권_국공립", {"대학명": "고려대", "캠퍼스": "세종"}, {
    "전형방법": "논술100%/교과100%/종합서류100%"
})
update_entry("경기권_국공립", {"대학명": "삼육대"}, {
    "최저내용": "논술1개3등급/교과2합7/약학3합5"
})
update_entry("경기권_국공립", {"대학명": "홍익대", "캠퍼스": "세종"}, {
    "최저내용": "없음(2026기준)"
})
update_entry("경기권_국공립", {"대학명": "공주대"}, {"최저내용": "미정"})
update_entry("경기권_국공립", {"대학명": "서경대"}, {"최저내용": "미정"})
update_entry("경기권_국공립", {"대학명": "제주대"}, {"최저내용": "미정"})

# ===== Entry count verification =====
print("\n" + "=" * 60)
print("ENTRY COUNT VERIFICATION")
print("=" * 60)
all_ok = True
for s in sheets:
    orig_count = len(original_data.get(s, []))
    new_count = len(data.get(s, []))
    status = "OK" if orig_count == new_count else "MISMATCH!"
    if orig_count != new_count:
        all_ok = False
    print(f"  {s}: {orig_count} → {new_count} [{status}]")

# ===== Change log =====
print("\n" + "=" * 60)
print(f"CHANGE LOG: 총 {len(changes_log)}건 변경")
print("=" * 60)
by_sheet = {}
for c in changes_log:
    by_sheet.setdefault(c['sheet'], []).append(c)

for sheet_name, items in by_sheet.items():
    print(f"\n  [{sheet_name}] ({len(items)}건)")
    for c in items:
        old_display = c['old'] if c['old'] != "" else "(빈칸)"
        print(f"    #{c['idx']} {c['univ']} / {c['field']}: {old_display} → {c['new']}")

# ===== After gaps =====
print("\n" + "=" * 60)
print("AFTER: 빈칸 현황 (변경 후)")
print("=" * 60)
for s in sheets:
    e_before, t = before_gaps[s]
    e_after, t2 = count_gaps(s, data.get(s, []))
    improved = e_before - e_after
    pct_before = (e_before / t * 100) if t > 0 else 0
    pct_after = (e_after / t2 * 100) if t2 > 0 else 0
    arrow = f" (↓{improved}건 개선)" if improved > 0 else ""
    print(f"  {s}: {e_before}→{e_after}/{t2} ({pct_before:.1f}%→{pct_after:.1f}%){arrow}")

# ===== Save =====
with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\ndata.json 저장 완료")
print(f"총 변경: {len(changes_log)}건")
if all_ok:
    print("엔트리 수 검증: ALL OK")
else:
    print("엔트리 수 검증: MISMATCH DETECTED!")
