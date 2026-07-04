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
| [`ready-code-review`](ready-code-review/SKILL.md) | 사람 또는 AI 리뷰어에게 줄 리뷰 컨텍스트, severity 정책, false-positive 억제 규칙, 리뷰 프롬프트를 준비할 때 |
| [`writing-great-skills`](writing-great-skills/SKILL.md) | `SKILL.md` 작성, 스킬 리뷰, 런타임 포팅, 트리거 문구, 점진적 공개 구조를 다듬을 때 |

## 사용

이 저장소 또는 개별 스킬 디렉터리를 에이전트 런타임이 인식하는 스킬 경로에 둡니다. 예를 들어 Codex 개인 스킬은 보통 `~/.codex/skills/`, Claude 스킬은 `~/.claude/skills/` 같은 위치에서 로드됩니다.

런타임은 보통 `SKILL.md` 프론트매터의 `name`과 `description`을 검색 표면으로 사용합니다. 스킬 본문은 호출된 뒤에 읽히므로, 호출 조건은 프론트매터에 명확히 두고 긴 세부 지침은 직접 연결된 reference 파일로 분리합니다.

## 유지보수 규칙

이 repo에서 스킬을 만들거나 수정할 때는 [AGENTS.md](AGENTS.md)를 먼저 확인합니다. 현재 핵심 라우팅은 다음과 같습니다.

| 작업 | 우선 사용할 스킬 |
| --- | --- |
| 새 `SKILL.md` 작성 또는 기존 스킬 개선 | `writing-great-skills` |
| 스킬 지침, reference, example, script 수정 | `coding-quality-guardrails` |
| 분기, 부수효과, 순서 제약이 있는 새 workflow 추가 | `flow-design` |
| 스킬 경계, reference 분리, 여러 스킬 조합 변경 | `codebase-design` |
| 깨진 invocation, validation 실패, 회귀 디버깅 | `diagnosing-bugs` |
| 큰 cross-skill 변경 분해 | `decompose-and-dispatch` |
| 명확히 할당된 작업 단위 실행 | `execute-dispatch-unit` |
| 리뷰 요청 전 컨텍스트 패키지 준비 | `ready-code-review` |

변경 원칙:

- 스킬 본문은 최상위 절차만 담고, branch-specific 세부 사항은 직접 링크된 reference 파일에 둡니다.
- 예시, 템플릿, 스크립트, 자산은 해당 스킬 가까이에 둡니다.
- 문서만 바꾸는 작업은 구조 검사와 targeted `rg` 검색으로 검증합니다.
- 기존 README, `AGENTS.md`, skill frontmatter, `_workspace/` 작업 기록에서 확인한 근거를 우선합니다.

## 출처

`codebase-design`, `diagnosing-bugs`, `domain-modeling`, `writing-great-skills`는 Matt Pocock의 [`mattpocock/skills`](https://github.com/mattpocock/skills) commit `5d78bd0`를 기반으로 적용했습니다.
