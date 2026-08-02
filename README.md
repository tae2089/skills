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
| [`to-issues`](to-issues/SKILL.md) | spec을 리뷰 가능한 크기의 작업 단위로 쪼개 issue로 기록할 때(`task.md` Plan / GitHub sub-issue) |
| [`to-spec`](to-spec/SKILL.md) | 코드·테스트·설정·문서·인프라를 고치기 전에 계약과 설계를 spec으로 남길 때(`_workspace/` 파일 / GitHub Issues) |
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
| `to-spec` | Writing the contract and design before editing any project file — local `_workspace/` or GitHub Issues. |
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

각 단계는 독립 트리거를 가지므로 전부 거칠 필요는 없습니다. 계획 대화만 필요하면 `planning-grill`에서 멈추고, 이미 티켓이 있으면 `to-issues`부터 시작합니다. `decompose-and-dispatch`는 앞 단계와 의존이 없습니다 — 돌릴 대상을 인자로 받고, **목표와 의존** 두 필드만 있으면 누가 만든 티켓이든 실행합니다. `scope`와 `verify:`는 있으면 쓰고 없으면 보고합니다. 병렬 subagent는 각자 worktree에서 돌기 때문에 파일 겹침은 스케줄링 문제가 아니라 병합 충돌이 됩니다. 대신 worktree는 **파일이 안 겹치는 깨짐**을 숨깁니다 — 한쪽이 심볼 이름을 바꾸고 다른 쪽이 옛 이름을 부르면 둘 다 초록불인데 합치면 깨집니다. dispatch는 병합하지 않고, 남은 브랜치와 "합친 뒤 전체 검증 한 번"을 보고합니다.

백엔드는 `to-spec`이 정해 `.tracker` 한 줄짜리 파일에 캐시하고, `to-issues`가 같은 순서로 읽습니다 — 먼저 `_workspace/<task-name>/.tracker`, 없으면 `_workspace/.tracker`. 저장소 하나에 공유 백엔드 작업과 로컬 작업이 섞일 수 있기 때문입니다.

| 백엔드 | to-spec 산출물 | to-issues 산출물 |
| --- | --- | --- |
| `local` | `task.md` Contract + `implementation.md` | `task.md` Plan 항목 |
| `github` | `type:design` issue + `type:prd` issue | PRD의 native sub-issue |

Jira·Linear·Notion처럼 백엔드 파일이 없는 트래커는 `local`로 쓰고 나중에 MCP로 밀어 넣습니다 — 백엔드가 아니라 발행 단계입니다. 계약 네 조각이 티켓 본문이 되고 `task.md`는 링크만 남깁니다.

계약과 설계는 서로 다른 문서입니다. 계약은 **무엇을** 만들고 **언제 끝난 것인지**를, 설계는 **어떻게** 그리고 **왜**를 담습니다. 계약이 접근 방식으로 흘러가면 확인 가능한 기준이 아니게 됩니다. `github`에서는 계약 문서 맨 앞에 무슨 문제를 누구를 위해 푸는지 한 줄을 둡니다 — 팀원은 이 대화 없이 티켓만 열기 때문입니다. `local`은 그 줄을 두지 않습니다.

`to-spec`이 남기는 것은 여섯 조각입니다.

| 조각 | 내용 | 상한 |
| --- | --- | --- |
| Contract | 기대 동작, 인수 기준. 한 줄마다 **계기**와 **관찰 가능한 결과**를 담습니다 | 5 bullet |
| Non-Goals | 넣을 법한데 범위 밖인 것 | 3 bullet, 없으면 섹션 생략 |
| Test Cases | 실제 입력 → 실제 기대 출력. `TC-1`, `TC-2`로 번호를 붙입니다 | 상한 없음, 실패 케이스 최소 하나 |
| Verification | 그 케이스들을 **어떻게 확인하는지**. 고치기 전 실패 / 프로젝트 전체 / 실물 한 번 | 3개 고정 |
| Implementation | 접근, 가정, 영향 모듈, 위험, 엣지 케이스, 검토 후 버린 대안 | 12 bullet, 항상 작성 |
| Walkthrough | append-only 이벤트 로그. **항상 로컬**, 공유 백엔드에 안 올라감 | — |

Contract·Non-Goals·Verification은 한 곳에 같이 둡니다. `local`이면 `task.md`, `github`이면 `type:prd` issue입니다. `to-issues`가 만든 작업 단위가 링크로 가리키는 곳이 바로 여기라, subagent가 반드시 닿는 유일한 문서이기 때문입니다.

Non-Goals는 방향이 어긋나는 것을 막습니다. 구현자가 손댈 법한 인접 모듈, 디프가 유도하는 정리 작업, 두 번째 호출자가 필요로 할 일반화 — 이런 것에 씁니다. 아무도 시도하지 않을 것은 적지 않습니다. 검토했다 버린 접근은 non-goal이 아니라 설계 노트입니다.

Test Cases는 계약을 실제 값으로 옮긴 것입니다. 계약이 규칙이면 TC는 그 규칙의 실례 하나입니다. 읽는 곳이 셋입니다 — 구현자는 이걸 먼저 테스트로 쓰고, `to-issues`는 각 작업 단위의 `verify:`가 어느 케이스를 도는지 여기서 가져오며(`covers: TC-1, TC-3`), 리뷰어는 목록을 대조합니다. `to-issues`는 어느 unit도 안 덮는 TC(빠뜨린 작업)와 어느 TC도 안 가리키는 unit(시키지 않은 작업)을 양쪽으로 확인합니다. 그래서 **TC 개수에 상한이 없습니다** — 상한을 두면 unit 개수에 상한을 두는 것과 같아집니다. 대신 두 가지로 거릅니다. 틀렸을 때 만드는 물건이 달라지는 케이스만 남기고, 같은 코드 경로를 타는 케이스는 하나로 접습니다(`port: "eighty"`와 `port: "abc"`는 한 개). 접으면서 뺀 값들이 없어지는 건 아닙니다 — 그 값들을 전부 도는 건 테스트 파일이 할 일입니다.

정해지지 않은 값은 지어내지 않고 `[NEEDS CLARIFICATION: 무엇이 안 정해졌는지]`로 그 자리에 남깁니다. 추측한 값은 계약이 되고, 뒷단계는 그게 결정된 값인지 구별하지 못합니다. `grep -rn "NEEDS CLARIFICATION"`으로 찾아 `planning-grill`로 돌아갑니다.

Test Cases와 Verification은 층이 다릅니다. TC는 **무엇이 참이어야 하는가**를 실제 값으로 적은 것이고, Verification은 **그걸 어떻게 확인하는가**를 적은 명령입니다. 그래서 Verification에는 케이스를 나열하지 않습니다 — 케이스별 확인은 테스트 파일이 하고, 그 테스트 파일이 TC에서 나옵니다. TC가 스무 개여도 Verification은 세 항목입니다. 값을 다시 쓰지 않고 번호로 가리킵니다(`TC-1`).

세 항목이 각각 다른 실패를 잡습니다. **고치기 전에 실패하는 것을 먼저 확인** — 실패한 적 없는 테스트는 아무것도 검사한다는 증거가 없습니다. 초록불은 생각보다 약한 증거입니다. 코드를 짠 쪽이 테스트도 짜면 둘이 서로 맞으면서 계약과 어긋날 수 있습니다. **프로젝트 전체** — spec의 Verification은 전체를 돌고 작업 단위의 `verify:`는 자기 범위만 돌아서 둘이 같은 명령이 될 수 없습니다. **실물 한 번 손으로** — 스위트는 초록인데 바이너리가 안 뜨는 경우를 잡습니다. 전체 검증을 자동으로 돌려주는 스킬은 없습니다. `task.md`의 체크 안 된 항목이 유일한 표시입니다.

버그 수정은 계약 대신 재현 / 현재 동작 / 기대 동작을 씁니다. TC-1이 재현이고, 첫 검증 항목이 고치기 전 그 테스트가 실패하는 것입니다.

`decompose-and-dispatch`는 부모의 Non-Goals만 subagent 프롬프트에 그대로 복사합니다. 이미 잘못된 것을 만들기 시작한 subagent는 링크를 따라가지 않기 때문입니다.

산출물의 산문 — 계약, 비목표, 설계 노트, 로그 — 은 사용자 언어로 씁니다. 명령·파일 경로·라벨(`type:prd`)·상태값(`Todo`/`Done`)은 검색 대상이라 그대로 둡니다.

`planning-grill`은 저장소가 답할 수 있는 사실은 직접 조사하고, 결정만 한 턴에 하나씩 사용자에게 묻습니다. 모든 질문에 추천 답과 **틀렸을 때의 대가**를 함께 적어, 사용자가 후속 질문 없이 비용을 보고 판단하게 합니다.

```text
Recommended: per-API-key, with a per-IP fallback for unauthenticated routes.
If wrong: authed clients behind one shared IP throttle each other.
```

GitHub 이슈 생성이나 팀 트래커 푸쉬는 팀에 보이고 되돌리기 번거로우므로, `to-spec`과 `to-issues` 모두 공유 백엔드 첫 쓰기 전에 무엇을 만들지 알리고 확인을 받습니다.

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
