#!/bin/bash
set -uo pipefail
cd "/c/Users/astk1/IdeaProjects/HowToLiveBetter-ko" || { echo "FATAL: cd 실패 — Git Bash로 실행 중인가?" >&2; exit 1; }
n=$(ls book/*.md 2>/dev/null | grep -vc -- "-kr.md")
[ "$n" -eq 11 ] || { echo "FATAL: book 비-kr = $n (11 기대) — 게이트 무효" >&2; exit 1; }
PY="${PY:-}"; [ -n "$PY" ] && "$PY" -c "" 2>/dev/null || PY=""; if [ -z "$PY" ]; then for c in "C:/Users/astk1/AppData/Local/Programs/Python/Python310/python.exe" "/c/Users/astk1/AppData/Local/Programs/Python/Python310/python.exe" python py python3; do if "$c" -c "" 2>/dev/null; then PY="$c"; break; fi; done; fi
command -v "$PY" >/dev/null || { echo "FATAL: python 없음 (PY 변수로 지정 가능)" >&2; exit 1; }

XRE="제(5|6|7|8|9|10|11|12|15|16|17|18|19|21|23|24|25|26|27|29|31|32|33)절 [0-9]+항"
echo "== dangling 잔존 ('제N절 M항' 형태, 미수록 절만; 0 = PASS)"
grep -noP "$XRE" book/*.md || true
D=$(grep -hoP "$XRE" book/*.md | wc -l); echo "dangling_hits=$D"

echo "== 마크 대장 (c-base 대비 감소분 = 지역화 완료)"
NB=$(ls book/*.md | grep -v -- '-kr.md'); C=$(cat $NB | grep -c '\[C\]\*\*'); W=$(cat $NB | grep -c '\[W\]\*\*')
echo "C_now=$C W_now=$W"

echo "== 등급 분포 (변형 라벨 주의: 'B (...' 포함)"
grep -h '^- 증거 등급:' book/*.md | sort | uniq -c || echo "GRADE-GREP-FAIL"

echo "== 항목 수 (241 = PASS)"
E=$(cat $(ls book/*.md | grep -v -- '-kr.md') | grep -c '^### '); echo "entries=$E"

echo "== parse-test (SEAM+TOTAL)"
PT=$(node "tools/ko/parse-test.mjs" 2>&1 | grep -E "^SEAM|^TOTAL" || true)
echo "$PT"
S=$(echo "$PT" | grep -c "^SEAM links==disk: true")

echo "== URL·구분자 렌더 검사 (한글 URL 미인코딩 / 출처 구분자 — 각 hit 수동 확인)"
grep -nP 'https?://[^\s<>"()]*[\x{AC00}-\x{D7A3}]' book/*.md || true
grep -nP '^- 출처:.*[가-힣];' book/*.md | grep -v '；' || true

echo "== align-check (11 OK 기대)"
A=$( { "$PY" tools/ko/align-check.py 2>&1 | tee /tmp/align-latest.json | grep -oP '"verdict": "\w+"' | sort | uniq -c; } || true)
echo "$A"
OKC=$(echo "$A" | grep '"verdict": "OK"' | grep -oP '\d+' | head -1); [ -z "$OKC" ] && OKC=0
echo "== 스왑 상세 (grade/dispute — 읽고 승인)"
grep -oP '"e\d+ grade[^"]*"|"dispute_moved_to": \{[^}]+\}' /tmp/align-latest.json 2>/dev/null || echo "( 없음 )"

echo "== 용어사전 고아 용어"
"$PY" tools/ko/gloss-orphan.py || echo "GLOSS-ORPHAN-FAIL"

echo "== 재조정 필요 하드코드 (수동 대조)"
grep -nE "극고 40|고 109|보통 92|A급 114|B급 109|C급 18|500%|-500|114개|40개|재작성 예정|\[C\] 표시|\[W\] 표시|3~4천 위안|C 82|W 3|争议 38|待核实 1" README.md index.html AGENTS.md || true

echo "== SUMMARY"
if [ "$D" -eq 0 ] && [ "$E" -eq 241 ] && [ "$S" -eq 1 ] && [ "$OKC" -eq 11 ]; then
  echo "PASS (dangling0·241항·SEAM·align11)"
else
  echo "CHECK: dangling=$D entries=$E seam=$S align_ok=$OKC/11"
fi
