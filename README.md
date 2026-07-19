# skills

AI 코딩 에이전트용 포터블 스킬 모음입니다. 각 스킬은 `SKILL.md`의 프론트매터와 본문을 진입점으로 삼고, 필요한 세부 절차는 가까운 `references/`, `reference/`, `examples/`, `agents/` 디렉터리에 둡니다.

## 구성

```text
<skill-name>/
  SKILL.md          # 스킬의 호출 조건과 최상위 절차
  references/       # 상황별 세부 지침
  reference/        # 일부 스킬의 세부 지침
  examples/         # 재사용 가능한 예시
  scripts/          # 결정적 검증·조작 스크립트
  agents/           # 런타임별 어댑터나 포팅 지침
```

모든 스킬이 모든 하위 디렉터리를 갖지는 않습니다. `SKILL.md`가 직접 가리키는 파일만 온디맨드로 읽는 것을 원칙으로 합니다.

스킬 디렉터리 밖의 최상위 [`examples/agents-md/`](examples/agents-md/)에는 이 스킬들을 설치한 다운스트림 프로젝트용 `AGENTS.md` 템플릿이 있습니다.

## 스킬 목록

| 스킬 | 사용할 때 |
| --- | --- |
| [`codebase-design`](codebase-design/SKILL.md) | 모듈 경계, 인터페이스, 리팩터링, 테스트 가능성, 의존성 주입, 결합도를 설계하거나 검토할 때 |
| [`coding-quality-guardrails`](coding-quality-guardrails/SKILL.md) | Go, Python, Java/Kotlin, TypeScript 작업에서 품질 저하, 테스트 게이밍, 과한 추상화, 약한 검증을 막아야 할 때 |
| [`compound-learning`](compound-learning/SKILL.md) | 완료·검증된 작업(태스크, 리뷰, 버그 수정, 설계 결정, 디버깅)에서 재사용 가능한 학습을 `_workspace/<task>/compound-learning.md`와 `docs/solutions/` 문서로 증류할 때. 진행 중 작업·불확실한 결과에는 미사용 |
| [`decompose-and-dispatch`](decompose-and-dispatch/SKILL.md) | 복잡한 목표를 원자적 작업 단위로 나누고 실행 가능한 디스패치 계획으로 바꿀 때 |
| [`diagnosing-bugs`](diagnosing-bugs/SKILL.md) | 버그, 회귀, 플래키 테스트, 실패 테스트, 깨진 UI 흐름, 성능 저하를 증거 기반으로 진단할 때 |
| [`domain-modeling`](domain-modeling/SKILL.md) | 도메인 용어, 글로서리, ADR, 컨텍스트 문서, 네이밍을 정렬할 때 |
| [`execute-dispatch-unit`](execute-dispatch-unit/SKILL.md) | 명확히 할당된 단일 작업 단위를 범위 안에서 실행하고 결과를 보고할 때 |
| [`flow-design`](flow-design/SKILL.md) | 새 로직의 분기, 부수효과, 순서 제약을 pseudocode나 Mermaid 다이어그램으로 고정하거나 기존 흐름을 문서화할 때 |
| [`oss-study`](oss-study/SKILL.md) | 오픈소스 코드베이스를 Diátaxis 기반 4가지 질문 모드로 구조화해 학습할 때 |
| [`overengineering-review`](overengineering-review/SKILL.md) | 새 추상화가 후속 회귀를 3건 이상 유발하거나, 테스트 통과 후 커밋 전 영속 필드·인터페이스 메서드·라이프사이클 상태·호환성 분기·과한 테스트 매트릭스가 추가됐을 때 불필요한 복잡도를 검토할 때. 단순화가 명시적으로 요청되지 않는 한 read-only |
| [`planning-grill`](planning-grill/SKILL.md) | 모호한 계획을 분해·실행 전에 코드 근거로 검증해 범위·수용기준·실패 모드를 벼릴 때. `decompose-and-dispatch` 상류에서 실행 |
| [`ready-code-review`](ready-code-review/SKILL.md) | 사람 또는 AI 리뷰어에게 줄 리뷰 컨텍스트, severity 정책, false-positive 억제 규칙, 리뷰 프롬프트를 준비할 때 |
| [`session-recipe`](session-recipe/SKILL.md) | 세션 기록 설정을 확인하고, 완료된 작업을 재생 가능한 recipe(dispatch packet 시퀀스)로 증류하거나, recipe.yaml을 검증·재생할 때. 세션 기록 자체는 저장소 밖의 `session-recorder` hook 도구가 담당(설치는 그 README 참고) |
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
| `planning-grill` | Sharpening a fuzzy plan (scope, acceptance criteria, failure modes) before decomposition or execution. |
| `decompose-and-dispatch` | Planning multi-step or multi-agent work. |
| `execute-dispatch-unit` | Executing one assigned bounded dispatch unit with explicit scope, dependencies, and verification. |
| `domain-modeling` | Aligning terminology or doing domain modeling. |
| `ready-code-review` | Preparing review context, reviewer instructions, prompts, severity calibration, or false-positive suppression before a human or AI review. |
| `overengineering-review` | Reviewing a change for unnecessary abstractions, duplicated policy, or scope expansion — during implementation after a new abstraction causes 3+ follow-up regressions, or after tests pass and before commit when persisted fields, interface methods, lifecycle states, or compatibility branches were added. |
| `compound-learning` | Capturing reusable learnings into the task workspace and `docs/solutions/` after a non-trivial task, review, bug fix, or debugging session is verified. |
```

### 프로젝트별 프롬프트

프로젝트별 프롬프트에는 그 repo에서 어떤 스킬을 어떤 순서로 조합할지만 둡니다. 새 프로젝트에는 [`examples/agents-md/`](examples/agents-md/)의 템플릿을 복사해 시작하고, 사용하는 런타임의 프로젝트 프롬프트 파일명에 맞게 옮겨 씁니다.

| 런타임 | 프로젝트 프롬프트 예시 |
| --- | --- |
| Codex | `<repo>/AGENTS.md` |
| Claude | `<repo>/CLAUDE.md` |
| Gemini | `<repo>/GEMINI.md` |

| 템플릿 | 시나리오 |
| --- | --- |
| [`standalone/`](examples/agents-md/standalone/AGENTS.md) | 이 저장소 스킬만 사용하는 프로젝트 |
| [`with-agent-team/`](examples/agents-md/with-agent-team/AGENTS.md) | [`agent-team`](https://github.com/tae2089/agent-team) CLI를 작업 원장으로 함께 쓰는 프로젝트. agent-team 동봉 스킬 중 `agent-team-*` CLI 조작 스킬만 쓰고 `recipe-*`/`persona-*`는 배제하는 라우팅 포함 |

이 저장소 자체의 [AGENTS.md](AGENTS.md)도 살아 있는 예시지만, 스킬 저장소 특화 라우팅이므로 일반 프로젝트에는 위 템플릿이 맞습니다.

## planning-grill 사용 예시

`planning-grill`은 [`decompose-and-dispatch`](decompose-and-dispatch/SKILL.md)로 분해하기 전에 모호한 계획을 코드 근거로 벼리는 상류 단계입니다. 파이프라인 위치는 다음과 같습니다.

```text
[모호한 의도] → planning-grill → [선명한 계획 + 수용기준] → decompose-and-dispatch → execute-dispatch-unit
```

먼저 코드·문서를 조사해 저장소가 답할 수 있는 것은 묻지 않고, 남은 결정 중 범위·소유자·작업 순서·수용기준·안전 경계를 바꾸는 것만 blocking 질문으로 던집니다. 질문은 한 턴에 하나, 4줄 Probe Format(필요할 때만 2-3개 선택지 목록을 덧붙임)으로 보냅니다. 예를 들어 "공개 API에 rate limiting 추가"라는 모호한 요청은 이렇게 좁힙니다.

```md
Current understanding: add rate limiting to the public API without breaking existing clients.
Blocked decision: limit key — per-IP vs per-API-key changes middleware shape and the test matrix.
Recommended answer: per-API-key with a per-IP fallback for unauthenticated routes (if wrong: authed clients sharing an IP throttle each other).
Question: should the limit be keyed on the API key rather than the source IP?
```

`추천 답안`은 필수이고 틀렸을 때의 대가를 함께 적어, 사용자가 후속 질문 없이 비용을 보고 판단할 수 있게 합니다. 답이 나오면 결정을 `_workspace/<task-name>/`에 기록하고, 저장소·window·초과 응답 형식 같은 나머지 차원을 같은 방식으로 좁힙니다. 수용기준과 작업 경계가 워커가 증거로 완료할 만큼 구체화되면 `SHARPENED` 상태로 `decompose-and-dispatch`에 넘깁니다. blocking 결정이 남아 있으면 `BLOCKED_ON_USER`, 지배적 blocker가 다른 스킬(용어→`domain-modeling`, 구조→`codebase-design`, 흐름→`flow-design`)의 몫이면 `ROUTED`로 종료합니다.

## 유지보수 원칙

변경 원칙:

- 스킬 본문은 최상위 절차만 담고, branch-specific 세부 사항은 직접 링크된 reference 파일에 둡니다.
- 예시, 템플릿, 스크립트, 자산은 해당 스킬 가까이에 둡니다.
- 문서만 바꾸는 작업은 구조 검사와 targeted `rg` 검색으로 검증합니다.
- 기존 README, `AGENTS.md`, skill frontmatter, `_workspace/` 작업 기록에서 확인한 근거를 우선합니다.

## 출처

`codebase-design`, `diagnosing-bugs`, `domain-modeling`, `writing-great-skills`는 Matt Pocock의 [`mattpocock/skills`](https://github.com/mattpocock/skills) commit `5d78bd0`를 기반으로 적용했습니다.

`planning-grill`의 선택지 목록 규칙은 [`devbrother2024/skills`](https://github.com/devbrother2024/skills)의 `deep-interview` 스킬 commit `de4998a`에서 가져왔습니다.

`compound-learning`은 [`tae2089/agent-team`](https://github.com/tae2089/agent-team)의 `recipe-agent-team-compound-learning` 스킬 commit `2354d37`을 agent-team CLI 의존 없이 포터블하게 적응했습니다.
