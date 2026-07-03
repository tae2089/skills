# Agent Skills

AI 코딩 에이전트(Claude Code, Codex, Gemini 등)용 포터블 skill 모음. 각 skill은 `SKILL.md`(최상위 절차와 호출 메타데이터)와 분기별로 로드되는 `references/` 파일들로 구성된 디렉토리다.

## Skills

| Skill | 역할 |
|---|---|
| `codebase-design` | 아키텍처를 잡거나 리뷰할 때 deep module, 작은 인터페이스, seam, adapter를 설계한다. |
| `coding-quality-guardrails` | Go/Python 작업 품질 게이트: AI slop, 테스트 게이밍, 과추상화, 부실 검증 방지. |
| `decompose-and-dispatch` | 목표를 원자적 작업 단위로 쪼개고 각 단위를 최적 실행자에 매핑한다. |
| `diagnosing-bugs` | 증거 우선 디버깅 루프: 피드백 루프 구축 → 재현 → 최소화 → 가설 → 수정 → 회귀 테스트. |
| `domain-modeling` | 프로젝트 용어, 용어집, 의사결정 기록을 벼린다 (DDD식 ubiquitous language, ADR). |
| `execute-dispatch-unit` | 배정된 작업 단위 하나를 scope 안에서 수행하고 구조화된 보고를 반환한다. |
| `flow-design` | Structures designs as pseudocode and Mermaid diagrams to expose implementation failure points before code exists; derives test scenarios from branches when needed. |
| `writing-great-skills` | skill 자체를 리뷰·작성·정제한다: 메타데이터, progressive disclosure, 완료 기준. |

## 설치 (Claude Code)

skill 디렉토리를 `~/.claude/skills/`로 복사한다:

```sh
cp -R <skill-name> ~/.claude/skills/
```

다음 세션부터 인식된다.

## flow-design Notes

The goal is not the picture; it is **reducing implementation failure**. It fills the altitude gap in spec-driven workflows: requirements say "what", design docs say "which component", but line-level control flow is often left unstated. Validation holes and unhandled branches leak at that altitude.

- **Design path (default)**: summarize acceptance criteria -> verify existing code integration points (`file:line`) -> fix non-trivial logic as numbered pseudocode -> render a proposed diagram when useful -> report **implementation risks**. Derive scenarios from branch arms only when tests/scenarios were requested or when handing off to a TDD test list such as `task.md`.
- **Current-state diagrams (supporting)**: sequence/flowchart/state/component/ER for existing code. Draw only what was read and carry paths to closure. Use this to understand the current shape that the design must fit.

To enable automatic routing, add routing to global or project agent instructions (`CLAUDE.md` / `AGENTS.md`). Example:

```markdown
- `flow-design` — when asked for pseudocode, a logic/flow plan, code flow, or
  diagrams; also before implementing non-trivial new logic.
```
