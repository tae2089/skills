# skills

AI 코딩 에이전트용 포터블 스킬 모음입니다. 각 스킬은 `SKILL.md`의 프론트매터와 본문을 진입점으로 삼고, 필요한 세부 절차는 가까운 `references/`, `reference/`, `examples/`, `agents/` 디렉터리에 둡니다.

## 구성

```text
<skill-name>/
  SKILL.md          # 스킬의 호출 조건과 최상위 절차
  references/       # 상황별 세부 지침
  reference/        # 일부 스킬의 세부 지침
  examples/         # 재사용 가능한 예시
  agents/           # 런타임별 어댑터나 포팅 지침
```

모든 스킬이 모든 하위 디렉터리를 갖지는 않습니다. `SKILL.md`가 직접 가리키는 파일만 온디맨드로 읽는 것을 원칙으로 합니다.

## 스킬 목록

| 스킬 | 사용할 때 |
| --- | --- |
| [`codebase-design`](codebase-design/SKILL.md) | 모듈 경계, 인터페이스, 리팩터링, 테스트 가능성, 의존성 주입, 결합도를 설계하거나 검토할 때 |
| [`coding-quality-guardrails`](coding-quality-guardrails/SKILL.md) | Go, Python, Java/Kotlin, TypeScript 작업에서 품질 저하, 테스트 게이밍, 과한 추상화, 약한 검증을 막아야 할 때 |
| [`decompose-and-dispatch`](decompose-and-dispatch/SKILL.md) | 복잡한 목표를 원자적 작업 단위로 나누고 실행 가능한 디스패치 계획으로 바꿀 때 |
| [`diagnosing-bugs`](diagnosing-bugs/SKILL.md) | 버그, 회귀, 플래키 테스트, 실패 테스트, 깨진 UI 흐름, 성능 저하를 증거 기반으로 진단할 때 |
| [`domain-modeling`](domain-modeling/SKILL.md) | 도메인 용어, 글로서리, ADR, 컨텍스트 문서, 네이밍을 정렬할 때 |
| [`execute-dispatch-unit`](execute-dispatch-unit/SKILL.md) | 명확히 할당된 단일 작업 단위를 범위 안에서 실행하고 결과를 보고할 때 |
| [`flow-design`](flow-design/SKILL.md) | 새 로직의 분기, 부수효과, 순서 제약을 pseudocode나 Mermaid 다이어그램으로 고정하거나 기존 흐름을 문서화할 때 |
| [`oss-study`](oss-study/SKILL.md) | 오픈소스 코드베이스를 Diátaxis 기반 4가지 질문 모드로 구조화해 학습할 때 |
| [`ready-code-review`](ready-code-review/SKILL.md) | 사람 또는 AI 리뷰어에게 줄 리뷰 컨텍스트, severity 정책, false-positive 억제 규칙, 리뷰 프롬프트를 준비할 때 |
| [`session-recipe`](session-recipe/SKILL.md) | 완료된 작업을 재생 가능한 recipe(dispatch packet 시퀀스)로 증류하거나 recipe.yaml을 재생할 때. 세션 기록은 저장소 밖의 `session-recorder` hook 도구가 담당(설치는 그 README 참고) |
| [`writing-great-skills`](writing-great-skills/SKILL.md) | `SKILL.md` 작성, 스킬 리뷰, 런타임 포팅, 트리거 문구, 점진적 공개 구조를 다듬을 때 |

## 설치

이 저장소 또는 개별 스킬 디렉터리를 Codex, Claude, Gemini 등 각 에이전트 런타임이 인식하는 스킬 경로에 둡니다. 설치 경로와 로드 방식은 런타임마다 다르지만, 이 README의 운영 모델은 동일합니다.

설치는 스킬 파일을 사용할 수 있게 만드는 단계입니다. 실제 운영에서는 아래처럼 전역 프롬프트와 프로젝트별 프롬프트를 나눠 라우팅 규칙을 둡니다.

## 프롬프트 배치

### 전역 프롬프트

전역 프롬프트에는 모든 프로젝트에서 공통으로 쓸 스킬 트리거만 짧게 둡니다. 긴 절차나 프로젝트별 조합 순서는 전역 프롬프트에 넣지 않습니다.

| 런타임 | 전역 프롬프트 예시 |
| --- | --- |
| Codex | `~/.codex/AGENTS.md` |
| Claude | `~/.claude/CLAUDE.md` |
| Gemini | `~/.gemini/GEMINI.md` |

```markdown
## Coding Skills

Apply these when their trigger conditions are met:

| Skill | Apply when |
| --- | --- |
| `coding-quality-guardrails` | Writing, modifying, or reviewing code. |
| `diagnosing-bugs` | Debugging bugs, regressions, flaky behavior, or failing tests. |
| `flow-design` | Pseudocode, logic/flow plans, diagrams, or new logic with branches, side effects, resource lifecycles, or ordering constraints. |
| `codebase-design` | Designing module boundaries, refactoring, or shaping interfaces. |
| `decompose-and-dispatch` | Planning multi-step or multi-agent work. |
| `execute-dispatch-unit` | Executing one assigned bounded dispatch unit with explicit scope, dependencies, and verification. |
| `domain-modeling` | Aligning terminology or doing domain modeling. |
| `ready-code-review` | Preparing review context, reviewer instructions, prompts, severity calibration, or false-positive suppression before a human or AI review. |
```

### 프로젝트별 프롬프트

프로젝트별 프롬프트에는 그 repo에서 어떤 스킬을 어떤 순서로 조합할지만 둡니다. 새 프로젝트에는 이 저장소의 [AGENTS.md](AGENTS.md)를 예시로 가져가고, 사용하는 런타임의 프로젝트 프롬프트 파일명에 맞게 옮겨 씁니다.

| 런타임 | 프로젝트 프롬프트 예시 |
| --- | --- |
| Codex | `<repo>/AGENTS.md` |
| Claude | `<repo>/CLAUDE.md` |
| Gemini | `<repo>/GEMINI.md` |

```markdown
# Project Guidance

Follow the global prompt rules first. This file only adds repository-specific routing.

## Skill Routing

- When creating or revising a `SKILL.md`, use `writing-great-skills` first.
- When modifying skill instructions, references, examples, or scripts, use `coding-quality-guardrails`.
- When a skill change introduces branching workflow, side effects, ordering constraints, or a new multi-step procedure, use `flow-design` before editing.
- When a change reshapes skill boundaries, splits or merges references, changes reusable interfaces, or affects how multiple skills compose, use `codebase-design` before editing.
- When debugging a broken skill workflow, failing validation, confusing invocation, or reported regression, use `diagnosing-bugs` before changing behavior.
- When preparing a skill package for human or AI review, use `ready-code-review`.
- For large cross-skill changes, use `decompose-and-dispatch`; execute clearly assigned units with `execute-dispatch-unit`.
```

## 유지보수 원칙

변경 원칙:

- 스킬 본문은 최상위 절차만 담고, branch-specific 세부 사항은 직접 링크된 reference 파일에 둡니다.
- 예시, 템플릿, 스크립트, 자산은 해당 스킬 가까이에 둡니다.
- 문서만 바꾸는 작업은 구조 검사와 targeted `rg` 검색으로 검증합니다.
- 기존 README, `AGENTS.md`, skill frontmatter, `_workspace/` 작업 기록에서 확인한 근거를 우선합니다.

## 출처

`codebase-design`, `diagnosing-bugs`, `domain-modeling`, `writing-great-skills`는 Matt Pocock의 [`mattpocock/skills`](https://github.com/mattpocock/skills) commit `5d78bd0`를 기반으로 적용했습니다.
