#!/bin/bash
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO" || { echo "FATAL: cd 실패" >&2; exit 1; }
KR=$(ls book/*-kr.md 2>/dev/null | wc -l)
[ "$KR" -eq 13 ] || { echo "FATAL: *-kr.md = $KR (13 기대)"; exit 1; }
PY="/c/Users/astk1/AppData/Local/Programs/Python/Python310/python.exe"
[ -x "$PY" ] || { echo "FATAL: python 없음"; exit 1; }

XRE="제(7|8|9|10|11|12|15|16|17|18|19|21|23|24|25|26|27|29|31|32|33)절|(?:(?<!\d))(7|8|9|10|11|12|15|16|17|18|19|21|23|24|25|26|27|29|31|32|33)\.[0-9]+ 항목|(?:(?<!\d))(7|8|9|10|11|12|15|16|17|18|19|21|23|24|25|26|27|29|31|32|33)장\b"
echo "== dangling 잔존 (_kr, 0 = PASS)"
grep -noP "$XRE" book/*-kr.md || true
D=$(grep -hoP "$XRE" book/*-kr.md | wc -l); echo "dangling_hits=$D"

echo "== 마크 대장 (_kr)"
C=$(cat $(ls book/*-kr.md) | grep -c '\[C\]\*\*'); W=$(cat $(ls book/*-kr.md) | grep -c '\[W\]\*\*')
echo "C_now=$C W_now=$W"

echo "== 항목 수 (_kr 합계 241 = PASS)"
E=$(cat $(ls book/*-kr.md) | grep -c '^### '); echo "entries=$E"

echo "== 등급 분포"
cat $(ls book/*-kr.md) | grep '^- 증거 등급:' | sort | uniq -c || echo "GRADE-GREP-FAIL"

echo "== parse-test (SEAM true + TOTAL)"
PT=$(node tools/ko/parse-test.mjs 2>&1 | grep -E "^SEAM|^TOTAL" || true)
echo "$PT"
S=$(echo "$PT" | grep -c "^SEAM links==disk: true")

echo "== URL 렌더 (한글 URL 잔존 = 오탐 가능, 참고용)"
grep -lP 'https?://[^\s<>"()]*[\x{AC00}-\x{D7A3}]' book/*-kr.md || true

echo "== kr-check (11절 issues [] = PASS)"
"$PY" -X utf8 - << 'PYEOF' > /tmp/kr-summary.txt 2>&1
import json,subprocess,glob,os
pairs=[]
for k in sorted(glob.glob("book/*-kr.md")):
    o=k.replace("-kr.md",".md")
    if not os.path.exists(o): o=k
    pairs+= [o,k]
out=subprocess.run(["C:/Users/astk1/AppData/Local/Programs/Python/Python310/python.exe","-X","utf8","tools/ko/kr-check.py"]+pairs,capture_output=True,text=True,encoding="utf-8").stdout
f=0; n=0
for L in out.splitlines():
    try:
        d=json.loads(L); n+=1
        if d.get("issues"):
            f+=1; print("KRFAIL",d["file"],d["issues"][:2])
    except Exception:
        print("KRPARS",L[:80])
print("KRCOUNT",n)
if f==0 and n>0: print("KRPASS")
PYEOF
grep -v "^{" /tmp/kr-summary.txt || true
KRF=$(grep -c "^KRFAIL\|^KRPARS" /tmp/kr-summary.txt || true)
KRN=$(grep "^KRCOUNT" /tmp/kr-summary.txt | grep -oP '\d+' || echo 0)
grep -q "^KRPASS" /tmp/kr-summary.txt || true

echo "== align-check"
A=$( { "$PY" -X utf8 tools/ko/align-check.py 2>&1 | tee /tmp/align-latest.json | grep -oP '"verdict": "\w+"' | sort | uniq -c; } || true)
echo "$A"
OKC=$(echo "$A" | grep '"verdict": "OK"' | grep -oP '\d+' | head -1); [ -z "$OKC" ] && OKC=0
echo "== 스왑 상세"
grep -o '"e[0-9]* grade[^"]*"' /tmp/align-latest.json 2>/dev/null | head -6 || echo "(grade 변경 없음)"

echo "== 용어 고아"
"$PY" -X utf8 tools/ko/gloss-orphan.py | grep -v ORPHAN || true

echo "== SUMMARY"
if [ "$D" -eq 0 ] && [ "$E" -eq 317 ] && [ "$S" -eq 1 ] && [ "$OKC" -eq "$KR" ]  && [ "$KRF" -eq 0 ] && [ "$KRN" -eq 13 ]; then
  echo "PASS (dangling0·317·SEAM·align$KR·URL0·krcheck13·gr-0)"
else
  echo "CHECK: D=$D E=$E S=$S align=$OKC/$KR  krF=$KRF krN=$KRN"
fi
