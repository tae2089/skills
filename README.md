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
| [`decompose-and-dispatch`](decompose-and-dispatch/SKILL.md) | `to-issues`가 만든 issue를 의존 순서대로 subagent에 넘겨 실행할 때 |
| [`diagnosing-bugs`](diagnosing-bugs/SKILL.md) | 버그, 회귀, 플래키 테스트, 실패 테스트, 깨진 UI 흐름, 성능 저하를 증거 기반으로 진단할 때 |
| [`domain-modeling`](domain-modeling/SKILL.md) | 도메인 용어, 글로서리, ADR, 컨텍스트 문서, 네이밍을 정렬할 때 |
| [`flow-design`](flow-design/SKILL.md) | 새 로직의 분기, 부수효과, 순서 제약을 pseudocode나 Mermaid 다이어그램으로 고정하거나 기존 흐름을 문서화할 때 |
| [`oss-study`](oss-study/SKILL.md) | 오픈소스 코드베이스를 Diátaxis 기반 4가지 질문 모드로 구조화해 학습할 때 |
| [`overengineering-review`](overengineering-review/SKILL.md) | 새 추상화가 후속 회귀를 3건 이상 유발하거나, 테스트 통과 후 커밋 전 영속 필드·인터페이스 메서드·라이프사이클 상태·호환성 분기·과한 테스트 매트릭스가 추가됐을 때 불필요한 복잡도를 검토할 때. 단순화가 명시적으로 요청되지 않는 한 read-only |
| [`planning-grill`](planning-grill/SKILL.md) | 모호한 계획·결정을 실행 전에 한 번에 한 질문씩 캐물어 합의에 도달할 때. 사실은 직접 조사하고 결정만 사용자에게 넘김. 파일은 만들지 않음 |
| [`ready-code-review`](ready-code-review/SKILL.md) | 사람 또는 AI 리뷰어에게 줄 리뷰 컨텍스트, severity 정책, false-positive 억제 규칙, 리뷰 프롬프트를 준비할 때 |
| [`to-issues`](to-issues/SKILL.md) | spec을 리뷰 가능한 크기의 작업 단위로 쪼개 issue로 기록할 때(`task.md` Plan / Jira sub-task / GitHub sub-issue) |
| [`to-spec`](to-spec/SKILL.md) | 코드·테스트·설정·문서·인프라를 고치기 전에 계약과 설계를 spec으로 남길 때(`_workspace/` 파일 / Jira+Confluence / GitHub Issues) |
| [`writing-great-skills`](writing-great-skills/SKILL.md) | `SKILL.md` 작성, 스킬 리뷰, 런타임 포팅, 트리거 문구, 점진적 공개 구조를 다듬을 때 |

## 설치

이 저장소 또는 개별 스킬 디렉터리를 Codex, Claude, Gemini 등 각 에이전트 런타임이 인식하는 스킬 경로에 둡니다. 설치 경로와 로드 방식은 런타임마다 다르지만, 이 README의 운영 모델은 동일합니다.

| 런타임 | 전역 스킬 경로 |
| --- | --- |
| Claude | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Gemini | `~/.gemini/skills/` |

권장 방식은 저장소를 한 곳에 두고 각 스킬을 심볼릭 링크로 거는 것입니다. 링크는 저장소를 고치는 즉시 반영되므로 사본이 뒤처지지 않습니다.

```bash
REPO=~/path/to/skills
DEST=~/.claude/skills

for d in "$REPO"/*/; do
  name=$(basename "$d")
  case "$name" in _workspace|examples) continue ;; esac
  ln -sfn "$d" "$DEST/$name"
done
```

사본으로 설치했다면 저장소를 고칠 때마다 직접 동기화해야 합니다. 이때 **삭제된 스킬이 남는 것**이 가장 흔한 사고입니다. 설치본에만 남은 옛 스킬은 계속 로드되고, 없어진 스킬을 가리키는 라우팅과 함께 조용히 오작동합니다.

```bash
REPO=~/path/to/skills
DEST=~/.claude/skills

# 추가·수정만 반영
for d in "$REPO"/*/; do
  name=$(basename "$d")
  case "$name" in _workspace|examples) continue ;; esac
  rsync -a --delete "$d" "$DEST/$name/"
done
```

`--delete`는 스킬 하나 안쪽에만 겁니다. 스킬 경로 전체에 걸면 이 저장소에서 오지 않은 다른 스킬까지 지웁니다.

저장소에서 스킬을 삭제했다면 설치본에서도 직접 지워야 합니다. 무엇이 남았는지는 아래로 확인합니다.

```bash
skill_names() { (cd "$1" && ls -d */) | tr -d / | grep -vE '^(_workspace|examples)$' | sort; }

comm -13 <(skill_names "$REPO") <(skill_names "$DEST")
```

출력된 이름 중 이 저장소에서 삭제한 스킬만 골라 지웁니다. 다른 출처의 스킬도 함께 나오므로 목록을 그대로 `rm`에 넘기지 마세요.

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
| `planning-grill` | Stress-testing a fuzzy plan, decision, or idea into a shared understanding, one question at a time. |
| `to-spec` | Writing the contract and design before editing any project file — local `_workspace/`, Jira + Confluence, or GitHub Issues. |
| `to-issues` | Breaking a written spec into ordered, reviewable work units recorded as issues. |
| `decompose-and-dispatch` | Running an existing issue list by giving each issue to a subagent, in dependency order. |
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

## 계획 파이프라인

모호한 의도에서 실행까지 네 단계입니다. 각 스킬은 한 가지만 하고, 앞 단계 산출물만 읽습니다.

```text
[모호한 의도]
  → planning-grill   대화로 합의 도출 (파일 안 만듦)
  → to-spec          합의를 spec으로 저장 — 계약 + 설계
  → to-issues        spec을 리뷰 단위 issue로 쪼갬
  → decompose-and-dispatch   issue마다 subagent 실행
```

각 단계는 독립 트리거를 가지므로 전부 거칠 필요는 없습니다. 계획 대화만 필요하면 `planning-grill`에서 멈추고, 이미 티켓이 있으면 `to-issues`부터 시작합니다.

백엔드는 `to-spec`이 한 번 정해 `_workspace/.tracker`에 캐시하고, 뒤 단계는 그것을 읽기만 합니다.

| 백엔드 | to-spec 산출물 | to-issues 산출물 |
| --- | --- | --- |
| `local` | `task.md` Contract + `implementation.md` | `task.md` Plan 항목 |
| `jira` | Confluence seed page + Jira PRD 티켓 | PRD의 sub-task |
| `github` | `type:seed` issue + `type:prd` issue | PRD의 native sub-issue |

`planning-grill`은 저장소가 답할 수 있는 사실은 직접 조사하고, 결정만 한 턴에 하나씩 사용자에게 묻습니다. 모든 질문에 추천 답과 **틀렸을 때의 대가**를 함께 적어, 사용자가 후속 질문 없이 비용을 보고 판단하게 합니다.

```text
Recommended: per-API-key, with a per-IP fallback for unauthenticated routes.
If wrong: authed clients behind one shared IP throttle each other.
```

Jira 티켓·Confluence 페이지·GitHub 이슈 생성은 팀에 보이고 되돌리기 번거로우므로, `to-spec`과 `to-issues` 모두 공유 백엔드 첫 쓰기 전에 무엇을 만들지 알리고 확인을 받습니다.

## 유지보수 원칙

변경 원칙:

- 스킬 본문은 최상위 절차만 담고, branch-specific 세부 사항은 직접 링크된 reference 파일에 둡니다.
- 예시, 템플릿, 스크립트, 자산은 해당 스킬 가까이에 둡니다.
- 문서만 바꾸는 작업은 구조 검사와 targeted `rg` 검색으로 검증합니다.
- 기존 README, `AGENTS.md`, skill frontmatter, `_workspace/` 작업 기록에서 확인한 근거를 우선합니다.

## 출처

`codebase-design`, `diagnosing-bugs`, `domain-modeling`, `planning-grill`, `writing-great-skills`는 Matt Pocock의 [`mattpocock/skills`](https://github.com/mattpocock/skills) commit `5d78bd0`를 기반으로 적용했습니다. `planning-grill`은 그중 `grilling` 스킬을 거의 그대로 따르되, 추천 답에 틀렸을 때의 대가를 함께 적는 규칙 하나를 더했습니다.

Interview → spec 분리는 Q00의 [`ouroboros`](https://github.com/Q00/ouroboros/blob/main/README.ko.md)에서 영향을 받았고, 이 저장소에서는 LLM 점수 대신 `planning-grill` → `to-spec` → `to-issues` 단계 분리로 적용했습니다.

`compound-learning`은 [`tae2089/agent-team`](https://github.com/tae2089/agent-team)의 `recipe-agent-team-compound-learning` 스킬 commit `2354d37`을 agent-team CLI 의존 없이 포터블하게 적응했습니다.
