import subprocess, re, json, os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CHAPS = ["01-不要早死","02-不要慢慢死","03-不要浪费精力","04-不要浪费时间","05-不要浪费钱","06-反面清单",
         "13-紧急情况","14-账号与信息安全","20-刚出生的孩子怎么带","22-怎么放松",
         "28-别为了外形把身体搞坏","30-上学以后的孩子","34-家里的常备药别吃出事"]
ENTRY = re.compile(r"^### (?:(\d+)\.)?(\d+)\. (.+)$", re.M)
TAG = re.compile(r"^\x3c!-- 成本标签:.*?--\>", re.M)
GRADE = re.compile(r"(?:证据等级|증거 등급)\s*[:：]\s*([ABC])")
NOTE = re.compile(r"^- (?:备注|비고)\s*[:：](.*)$", re.M)
URL = re.compile(r"https?://[^\s)\]\"，。;；]+")
URL = re.compile(r"https?://[^\s)>\]\"，。;、（）()]+")
H12 = re.compile(r"^#{1,2} ", re.M)

def git_show(n, path):
    r = subprocess.run(["git","show",f"{n}:{path}"],capture_output=True,text=True,encoding="utf-8")
    return r.stdout if r.returncode==0 else None

def parse(text):
    pos = [(m.start(), m.group(2)) for m in ENTRY.finditer(text)]
    ents = {}
    for i,(s,n) in enumerate(pos):
        e = pos[i+1][0] if i+1 < len(pos) else len(text)
        seg = text[s:e]
        tm = TAG.search(seg); gm = GRADE.search(seg); nm = NOTE.search(seg)
        ents[n] = {"tag": tm.group(0) if tm else None,
                   "grade": gm.group(1) if gm else None,
                   "urls": sorted(set(URL.findall(seg))),
                   "note": nm.group(1).strip() if nm else None}
    return ents

KO={"01-不要早死":"제01장-이르게-죽지-마라-kr","02-不要慢慢死":"제02장-천천히-죽어가면-안-된다-kr","03-不要浪费精力":"제03장-에너지-낭비하지-않기-kr","04-不要浪费时间":"제04장-시간-낭비하지-말라-kr","05-不要浪费钱":"제05장-돈-낭비하지-마라-kr","06-反面清单":"제06장-반대로-할-목록-kr","13-紧急情况":"제13장-긴급-상황-먼저-할-일-kr","14-账号与信息安全":"제14장-계정과-정보-보안-kr","20-刚出生的孩子怎么带":"제20장-갓-태어난-아기-돌보기-kr","22-怎么放松":"제22장-긴장-푸는-법-kr","28-别为了外形把身体搞坏":"제28장-외모-때문에-몸-망치지-마라-kr","30-上学以后的孩子":"제30장-학교에-들어간-뒤의-아이-kr","34-家里的常备药别吃出事":"제34장-집-상비약-먹다가-탈-안-나게-kr"}
def check(ch):
    p = f"book/{KO.get(ch, ch)}.md"
    orig = git_show("base-zh", f"book/{ch}.md") or git_show("upstream/main", f"book/{ch}.md")
    if orig is None: return f"SKIP {p} no baseline"
    tr = open(p, encoding="utf-8").read()
    if not re.search(r"쉬운 말|비용|혜택", tr): return f"PENDING {p}"
    c_base_path = re.sub(r"book/제(\d+)장-", r"book/\1-", p).replace("-kr", "")
    c_base_content = git_show("c-base", c_base_path)
    if c_base_content is None:
        head = orig
        hm = {m[1]: True for m in re.findall(r"^### (?:(\d+)\.)?(\d+)\. (.*)$", head, re.M)}
    else:
        head = c_base_content
        hm = {m[1]: bool(re.search(r"\[C\]|\[W\]", m[2])) for m in re.findall(r"^### (?:(\d+)\.)?(\d+)\. (.*)$", head, re.M)}
    o, t = parse(orig), parse(tr)
    issues = []
    infos = []
    if set(o) != set(t):
        issues.append(f"entry set diff only-orig={sorted(set(o)-set(t))} only-tr={sorted(set(t)-set(o))}")
    if len(H12.findall(tr)) != 1:
        issues.append(f"H1/H2 count={len(H12.findall(tr))} (must be 1)")
    zh_fields = len(re.findall(r"^- (?:成本|说人话|收益|证据等级|来源|备注)：", tr, re.M))
    if zh_fields:
        issues.append(f"UNTRANSLATED field lines={zh_fields}")
    zh_heads = [h for h in re.findall(r"^### (?:\d+\.)?\d+\. (.+)$", tr, re.M)
                if re.search(r"[\u4e00-\u9fff]", re.sub(r"[(（「『'\"《][^()（）「」『』'\"》]*[)）」』'\"》]", "", h))]
    if zh_heads:
        issues.append(f"UNTRANSLATED headings={len(zh_heads)}: {zh_heads[:3]}")
    zh_disputed = [n for n in o if o[n]["note"] and o[n]["note"].startswith("争议")]
    for n in sorted(set(o) & set(t), key=int):
        if o[n]["tag"] != t[n]["tag"]:
            issues.append(f"e{n} tag drift: {o[n]['tag']!r} -> {t[n]['tag']!r}")
        if o[n]["grade"] != t[n]["grade"]:
            (infos if hm.get(n, False) else issues).append(f"e{n} grade {o[n]['grade']}->{t[n]['grade']}")
        if o[n]["urls"] != t[n]["urls"]:
            added = sorted(set(t[n]["urls"]) - set(o[n]["urls"]))[:2]
            missing = sorted(set(o[n]["urls"]) - set(t[n]["urls"]))[:3]
            swapped = hm.get(n, False)
            (infos if swapped else issues).append(f"e{n} URL diff{'(마크-스왑 의도)' if swapped else ''} +{added} -{missing}")
    moved = {}
    for n in zh_disputed:
        first = (t.get(n) or {}).get("note") or ""
        head = first[:8].split(".")[0].split(" ")[0]
        if not first.startswith("争议"):
            moved[head] = moved.get(head, 0) + 1
    todo_orig = [n for n in o if any(x in (o[n]["note"] or "") + (o[n]["urls"] and " ".join(o[n]["urls"]) or "") for x in ["待核实","TODO"])]
    markers = tr.count(" **[C]**")
    han = [ln for ln in tr.splitlines() if re.search(r"[\u4e00-\u9fff]", ln)
           and "成本标签" not in ln and not re.match(r"^- 비고[:：]\s*争议", ln)
           and not re.match(r"^#{1,2} \d+\. ", ln)]
    verdict = "ISSUES" if issues else "OK"
    return json.dumps({"file": p, "verdict": verdict, "c_swaps": infos, "entries": len(t), "markers": markers,
                       "dispute_moved_to": moved, "han_residue_lines": len(han),
                       "sample_residue": [x[:50] for x in han[:3]],
                       "issues": issues[:10]}, ensure_ascii=False)

for c in CHAPS:
    print(check(c))
