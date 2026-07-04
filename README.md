# skills

AI 코딩 에이전트용 포터블 스킬 모음. 각 스킬은 `SKILL.md`(프론트매터 + 본문)와 필요 시 `references/`·`examples/`로 구성되며, 트리거 조건이 충족되면 온디맨드로 로드됩니다.

## 스킬 목록

| 스킬 | 설명 |
| --- | --- |
| [`codebase-design`](codebase-design/SKILL.md) | 깊은 모듈·작은 인터페이스·깔끔한 seam 설계. 모듈 경계, 리팩터링, 인터페이스 형태, 테스트 가능성, 결합도, DI를 다룰 때. |
| [`coding-quality-guardrails`](coding-quality-guardrails/SKILL.md) | Go·Python·Java/Kotlin·TypeScript 품질 가드레일. 코딩·리뷰·리팩터링·테스트 수정·회귀 디버깅 시 AI slop·테스트 게이밍·과한 추상화를 차단. |
| [`decompose-and-dispatch`](decompose-and-dispatch/SKILL.md) | 복잡한 목표를 원자적 작업 단위로 분해하고 실행 가능한 디스패치 계획으로 매핑. 멀티스텝·멀티에이전트 작업 계획 시. |
| [`diagnosing-bugs`](diagnosing-bugs/SKILL.md) | 증거 기반 디버깅 루프. 버그·회귀·플래키·실패 테스트·성능 저하 재현 및 근본 원인 추적 시. |
| [`domain-modeling`](domain-modeling/SKILL.md) | 도메인 언어·결정 기록 정립. 용어 모호성, 글로서리, 유비쿼터스 언어, ADR, 네이밍 정렬 시. |
| [`execute-dispatch-unit`](execute-dispatch-unit/SKILL.md) | 할당된 단일 디스패치 패킷을 범위 안에서 실행하고 구조화된 완료 보고. `decompose-and-dispatch`의 실행자 짝. |
| [`flow-design`](flow-design/SKILL.md) | Pseudocode와 Mermaid 다이어그램으로 새 로직의 실패 지점을 드러내고 기존 흐름을 문서화. 로직/플로우 설계, 설계 다이어그램, 기존 코드 다이어그램 요청 시. |
| [`ready-code-review`](ready-code-review/SKILL.md) | Prepares review context briefs, PR/diff packages, severity rubrics, false-positive suppressions, AI reviewer prompts, and reusable reviewer instructions. |
| [`writing-great-skills`](writing-great-skills/SKILL.md) | 포터블 스킬 작성·리뷰·개선. SKILL.md 작성, 런타임 간 포팅, 트리거 문구·점진적 공개 감사 시. |

## 사용

스킬 디렉터리를 에이전트 런타임이 인식하는 스킬 경로(예: `~/.claude/skills/`)에 두면, 프론트매터의 `description` 트리거에 따라 자동으로 로드됩니다.

## 라우팅 가이드

전역 `~/.codex/AGENTS.md`에는 다음처럼 짧은 스킬 트리거만 두고, 여러 스킬을 어떤 순서로 조합할지는 각 repo의 `AGENTS.md`에 둡니다. 이 repo의 [AGENTS.md](AGENTS.md)는 스킬 작성·수정·리뷰 작업에 맞춘 라우팅 순서를 제공합니다.

```markdown
# 🛠️ Coding Skills

Apply these when their trigger conditions are met:

- `coding-quality-guardrails` — when writing, modifying, or reviewing code.
- `diagnosing-bugs` — when debugging bugs, regressions, flaky behavior, or failing tests.
- `flow-design` — when asked for pseudocode, a logic/flow plan, or a diagram; mandatory before implementing new logic with branching, side effects, resource lifecycles, or ordering constraints.
- `codebase-design` — when designing module boundaries, refactoring, or shaping interfaces.
- `decompose-and-dispatch` — when planning multi-step or multi-agent work.
- `execute-dispatch-unit` — when executing one assigned bounded dispatch unit with explicit scope, dependencies, and verification.
- `domain-modeling` — when aligning terminology or doing domain modeling.
- `ready-code-review` — when preparing review context before human or AI code review: PR/diff context packages, review briefs, reusable reviewer instructions, reviewer prompts, severity calibration, or false-positive suppression. Do not use it when performing the review itself.
```

- 새 `SKILL.md` 작성 또는 기존 스킬 개선: `writing-great-skills` -> `coding-quality-guardrails`
- 분기, 부수효과, 순서 제약이 있는 새 workflow 추가: `flow-design` -> `coding-quality-guardrails`
- 스킬 경계, reference 분리, 여러 스킬 조합 변경: `codebase-design` -> `coding-quality-guardrails`
- 깨진 invocation, validation 실패, 회귀 디버깅: `diagnosing-bugs` -> `coding-quality-guardrails`
- 큰 cross-skill 변경: `decompose-and-dispatch`로 작업을 나누고, 명확히 할당된 단위는 `execute-dispatch-unit`으로 실행
- 리뷰 요청 전 준비: `ready-code-review`로 context, non-goal, severity policy, false-positive suppression 정리

## flow-design Notes

`flow-design`은 코드 작성 전 새 로직의 분기·부수효과·실패 처리를 고정하거나, 기존 코드 흐름을 sequence/flowchart/state/component/ER 다이어그램으로 추적할 때 사용합니다.

- **Design path**: acceptance criteria 요약 -> 기존 integration point 검증(`file:line`) -> non-trivial 로직 pseudocode 작성 -> 필요 시 proposal diagram 렌더 -> implementation risks 보고.
- **Current-state diagrams**: 먼저 다이어그램이 답할 질문을 한 문장으로 고정하고, 읽은 코드 또는 스키마 증거만으로 그립니다.

자동 라우팅이 필요한 런타임 지침(`CLAUDE.md` / `AGENTS.md`)에는 다음 트리거를 둡니다:

```markdown
- `flow-design` — when asked for pseudocode or a logic/flow plan, a design diagram,
  or an existing-code diagram; also before implementing new logic with branches or side effects.
```

## 출처

`codebase-design`, `diagnosing-bugs`, `domain-modeling`, `writing-great-skills`는 Matt Pocock의 [`mattpocock/skills`](https://github.com/mattpocock/skills) (commit `5d78bd0`)를 기반으로 적용했습니다.
