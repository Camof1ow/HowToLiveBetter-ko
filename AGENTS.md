# AGENTS.md

这个仓库是《高性价比人生指南》的正文。

- **改这本书**（增删条目、改正文、动工具脚本）：规则全在 [CLAUDE.md](CLAUDE.md) 里，全部适用，先读完再动手。文件名叫 CLAUDE.md 只是历史原因，内容与工具无关。
- **用这本书回答问题**（有人问该不该做、值不值、怎么选、出事了先做什么、能领哪笔钱、犯不犯法）：按 [skills/life-decision-guide/SKILL.md](skills/life-decision-guide/SKILL.md) 执行，先查条目再答，答复里注明出自第几节第几条。装到别的目录去用的办法见 [skills/life-decision-guide/README.md](skills/life-decision-guide/README.md)。

## 한국어판 포크 상태 (2026-10-07)
- 이 리포는 eternity4719/HowToLiveBetter의 한국어 발췌판(CC BY 4.0, 변경 명시 의무).
- A단계: 절 1·2·3·4·13·14·20·22·28·30·34 (241조항) 한국어 번역. 나머지 23절·제도 docs는 삭제, upstream에 원문 있음.
- 조항 제목 끝 `**[C]**` = 중국 제도 항목 마크. 대장: `grep -rn '\[C\]\*\*' book/`.
- C단계 목표: [C] 항목을 한국 법령·제도로 치환. 도구: korean-law-mcp (chrisryugj/korean-law-mcp, 법제처 API) 또는 법제처 오픈API 직접 조회. 한국 법 추측 금지, 원전(관보·법령 원문) 확인 후 기재.
- 파싱 불변량: `### N.` 항목 번호, `# N.` 절 번호, `<!-- 成本标签: -->` 기계태그는 중국어 원형 유지, 필드 라벨(비용:/쉬운 말:/혜택:/증거 등급:/출처:/비고:)은 index.html 정규식과 짝 — 한쪽만 바꾸지 말 것. 상호참조 형식 `제N절 M항`.
- README.md의 `](book/...)` 링크 목록 = index.html이 읽을 파일 목록의 원전. 절 추가/삭제 시 README 먼저.
