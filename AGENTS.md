# AGENTS.md

这个仓库是《高性价比人生指南》的正文。

- **改这本书**（增删条目、改正文、动工具脚本）：规则全在 [CLAUDE.md](CLAUDE.md) 里，全部适用，先读完再动手。文件名叫 CLAUDE.md 只是历史原因，内容与工具无关。
- **用这本书回答问题**（有人问该不该做、值不值、怎么选、出事了先做什么、能领哪笔钱、犯不犯法）：按 [skills/life-decision-guide/SKILL.md](skills/life-decision-guide/SKILL.md) 执行，先查条目再答，答复里注明出自第几节第几条。装到别的目录去用的办法见 [skills/life-decision-guide/README.md](skills/life-decision-guide/README.md)。

## 한국어판 포크 상태 (2026-10-07)
- 이 리포는 eternity4719/HowToLiveBetter의 한국어 발췌판(CC BY 4.0, 변경 명시 의무).
- A단계: 절 1·2·3·4·13·14·20·22·28·30·34 (241조항) 한국어 번역. 나머지 23절·제도 docs는 삭제, upstream에 원문 있음.
- 조항 제목 끝 `**[C]**` = 중국 제도 항목 마크. 대장: `grep -rn '\[C\]\*\*' book/`.
- C단계 목표: [C] 항목을 한국 법령·제도로 치환. 도구: korean-law-mcp (chrisryugj/korean-law-mcp, 법제처 API) 또는 법제처 오픈API 직접 조회. 한국 법 추측 금지, 원전(관보·법령 원문) 확인 후 기재.
- 인용 기준(사용자 지시 2026-10-07 개정): **1순위 국내 원천** — 통계청 자료 기반(원시표) 및 식약처·질병관리청·후고보 등 공식 통계, 국내 언론 보도는 원천 수치 확인용 병행. **모든 수치는 원본(통계표·법령 원문) against 더블체크 필수.** 국내 원천이 없으면 서구권 1차 연구(메타분석·RCT·코호트, DOI/PubMed/WHO/CDC)를 싣되 결과와 출처를 명확히 기입. 중국 자료는 그 주제의 세계 유일 1차 데이터일 때만 병기 — 그 외 `[C]` 처리. 도구: korean-law-mcp(법령), e-Stat API·통계청 국가통계포털(수치).
- 파싱 불변량: `### N.` 항목 번호, `# N.` 절 번호, `<!-- 成本标签: -->` 기계태그는 중국어 원형 유지, 필드 라벨(비용:/쉬운 말:/혜택:/증거 등급:/출처:/비고:)은 index.html 정규식과 짝 — 한쪽만 바꾸지 말 것. 상호참조 형식 `제N절 M항`.
- README.md의 `](book/...)` 링크 목록 = index.html이 읽을 파일 목록의 원전. 절 추가/삭제 시 README 먼저.
- README.md의 `](book/...)` 링크 목록 = index.html이 읽을 파일 목록의 원전. 절 추가/삭제 시 README 먼저.
## A단계 완료 검증 (2026-10-07)
- 파서 검증: `node C:/tmp/parse-test.mjs` — index.html에서 parseReadme·XREF_RE 원문 슬라이스 실행. 241항 전 파싱, 빈필드 0, 가성비 40/109/92 = ground truth 일치.
- 항목 대조: `C:/tmp/align-check.py` — base-zh 태그 대비 항목번호/비용태그/등급/URL집합/争议 토큰 전 일치(0 이탈). 수리 후에도 재실행 유효(idempotent).
- 시각 스모크(카드 DOM 렌더)는 omp 브라우저 데몬 outage로 미수행 — 푸시 후 https://camof1ow.github.io/HowToLiveBetter-ko/ 에서 카드 241·필터 극고 40 확인.
- 잔여 C단계 목록 = `[C]` 75개 (grep -rl '\[C\]' book/). 미수록 23절 = upstream 원문 참고.
