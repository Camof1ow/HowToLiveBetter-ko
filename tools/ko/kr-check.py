import re, sys, os, json
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TAG = re.compile(r"^\x3c!-- 成本标签:.*?--\>", re.M)
ENTRY = re.compile(r"^### (\d+)\. (.+)$", re.M)
URL = re.compile(r"https?://[^\s)>\]\"，。;、（）(]+")

def taglist(t): return TAG.findall(t)
def entries(t): return [(m.group(1), m.group(2).replace(" **[C]**","").replace(" **[W]**","").strip()) for m in ENTRY.finditer(t)]
def urlmap(t):
    pos = [(m.start(), m.group(1)) for m in ENTRY.finditer(t)]
    out = {}
    for i,(s,n) in enumerate(pos):
        e = pos[i+1][0] if i+1 < len(pos) else len(t)
        out[n] = sorted(set(URL.findall(t[s:e])))
    return out

def check(orig_path, kr_path):
    if not os.path.exists(kr_path): return {"file": kr_path, "issues": ["MISSING"]}
    o = open(orig_path, encoding="utf-8").read()
    k = open(kr_path, encoding="utf-8").read()
    iss = []
    ot, kt = taglist(o), taglist(k)
    if ot != kt:
        drift = [i+1 for i in range(min(len(ot),len(kt))) if ot[i] != kt[i]] or ["count"]
        iss.append(f"TAG DRIFT {drift[:8]}")
    if [n for n,_ in entries(o)] != [n for n,_ in entries(k)]: iss.append("entry number drift")
    if len(entries(o)) != len(entries(k)): iss.append(f"entry count {len(entries(o))}->{len(entries(k))}")
    if len(re.findall(r"^- (?:成本|说人话|收益|证据等级|来源|备注)：", k, re.M)): iss.append("zh-label lines")
    zh_heads = [h for h in re.findall(r"^### \d+\. (.+)$", k, re.M)
                if re.search(r"[\u4e00-\u9fff]", re.sub(r"[(（「『'\"《][^()（）「」『』'\"》]*[)）」』'\"》]", "", h))]
    if zh_heads: iss.append(f"zh-headings {zh_heads[:2]}")
    if len(re.findall(r"^#{1,2} ", k, re.M)) != 1: iss.append("H1/H2 count != 1")
    # URL 불변: [C] 마크가 남아있거나(미해결=보존 대상), 원본에서 제거된 게 아닌 한 동일해야 함
    ou, ku = urlmap(o), urlmap(k)
    oc = dict((n, ("[C]" in h or "[W]" in h)) for n, h in re.findall(r"^### (\d+)\. (.*)$", o, re.M))
    kc = dict((n, ("[C]" in h or "[W]" in h)) for n, h in re.findall(r"^### (\d+)\. (.*)$", k, re.M))
    viol = []
    for n in set(ou) & set(ku):
        if ou[n] != ku[n] and not oc.get(n) and not _drf_added(ou[n], ku[n]):
            viol.append(n)
    resolved = [n for n in set(oc) if oc[n] and not kc.get(n, True)]
    if viol: iss.append(f"URL diff outside [C]-resolved: {viol[:6]}")
    # 라벨 무결성 하드체크: 항목마다 6라벨 전부 존재 + 등급 문자 파싱 (손상/융합 줄 차단)
    pos = [m.start() for m in ENTRY.finditer(k)] + [len(k)]
    bad = []
    for i in range(len(pos) - 1):
        seg = k[pos[i]:pos[i+1]]
        head = ENTRY.findall(k)[i] if i < len(ENTRY.findall(k)) else ("?", "")
        labs = set(re.findall(r"^- (비용|쉬운 말|혜택|증거 등급|출처|비고)[:：]", seg, re.M))
        missing = {"비용","쉬운 말","혜택","증거 등급","출처","비고"} - labs
        if missing or not re.search(r"^- 증거 등급[:：]\s*[ABC]", seg, re.M):
            bad.append((head[0], sorted(missing) or "grade"))
    if bad: iss.append(f"LABEL INTEGRITY {bad[:4]}")
    won_r = len(re.findall(r"^- (?:비용|쉬운 말)[:：](?!.*환산).*위안", k, re.M))
    if won_r: iss.append(f"위안 in reader fields={won_r}")
    won_c = len(re.findall(r"^- (?:혜택|비고)[:：](?!.*환산).*위안", k, re.M))
    cn = len(re.findall(r"^- (?:비용|쉬운 말)[:：](?!.*중국).*중국", k, re.M))
    return {"file": kr_path, "issues": iss, "c_resolved": len(resolved),
            "won_in_cited_lines": won_c, "bare_china_reader_fields": cn, "entries": len(entries(k))}

def _drf_added(a, b):
    added, removed = set(b) - set(a), set(a) - set(b)
    kr_official = ("law.go.kr","go.kr","korea.kr","kdca","nhis","mfds","khepi","mods","mohw","nhic","er-api","fire.","police","mps","nip.")
    cn_gov = ("gov.cn","chinacdc","nmpa","cnnic","ndcpa","court.gov","spp.gov","119.gov","wjw.","beijing","sh.gov","gd.gov","yn","tj.","hunan","sc.gov","zj","jiangsu","nhc.")
    added_ok = all(any(s in u for s in kr_official) for u in added)
    removed_ok = all(any(s in u for s in cn_gov) for u in removed)
    return added_ok and removed_ok

if __name__ == "__main__":
    for orig, kr in zip(sys.argv[1::2], sys.argv[2::2]):
        print(json.dumps(check(orig, kr), ensure_ascii=False))
