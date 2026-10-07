import re, glob, subprocess, os
os.chdir(r"C:/Users/astk1/IdeaProjects/HowToLiveBetter-ko")
readme = open("README.md", encoding="utf-8").read()
m = re.search(r"^## (?:读懂数字|숫자)[^\n]*\n([\s\S]*?)(?=^## )", readme, re.M)
terms = []
if m:
    for line in m.group(1).splitlines():
        c = re.match(r"^\|\s*(.+?)\s*\|\s*.+\|$", line)
        if c and c.group(1) not in ("용어", "术语") and not re.match(r"^-+$", c.group(1)):
            terms += [t.strip() for t in re.split(r"、", c.group(1)) if t.strip()]
books = "\n".join(open(f, encoding="utf-8").read() for f in glob.glob("book/*.md"))
orphans = [t for t in terms if t not in books]
print(f"terms={len(terms)} orphans={len(orphans)}")
for t in orphans: print("  ORPHAN:", t)
