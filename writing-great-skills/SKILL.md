---
name: writing-great-skills
description: Review, create, or refine portable agent skills for predictable behavior, progressive disclosure, clean invocation metadata, concise instructions, reference splitting, trigger wording, and no-op pruning. Use when writing SKILL.md files, porting skills across Codex, Claude, Gemini, or other agent runtimes, auditing skill quality, or improving skill context load and execution reliability.
---

# Writing Great Skills

Use this skill to make portable agent skills predictable: the agent should take the same process each run, even when outputs differ by task.

Adapted from Matt Pocock's `writing-great-skills` skill in `mattpocock/skills` at commit `5d78bd0903420f97c791f834201e550c765699f8`.

## Review Loop

1. Identify the skill's job and the exact situations that should trigger it.
2. Check whether it should be model-invoked or explicit-only in each host runtime.
3. Keep `SKILL.md` as the top-level procedure, not a warehouse of every detail.
4. Move branch-specific or long reference material into directly linked `references/` files.
5. Remove duplicate meanings and no-op instructions.
6. Sharpen completion criteria so the agent cannot stop early.
7. Validate metadata, file structure, and examples against actual use.

## Invocation Metadata

The description is the retrieval surface. Put "when to use" triggers in frontmatter, not in the body.

Good descriptions:

- Start with the leading action or domain.
- Include genuinely distinct trigger branches.
- Avoid synonyms that repeat the same branch.
- Mention important file types, tools, or task shapes when they affect invocation.

If a skill should only run when explicitly named, use the host runtime's explicit-invocation mechanism if available. Otherwise make the description narrow enough that accidental invocation is unlikely.

## Runtime Portability

Keep `SKILL.md` host-neutral. Do not require Codex `$skill`, Claude slash commands, Gemini commands, or a specific subagent API in the core instructions.

Put host-specific invocation details in adapter files under `agents/` or equivalent runtime packaging:

- OpenAI/Codex adapter prompts may use `$skill-name`.
- Claude adapter prompts may use the project's Claude command or skill syntax when one exists.
- Gemini adapter prompts may use the project's Gemini command or skill syntax when one exists.
- If a host has no stable invocation syntax, use natural-language prompts such as "Use the <skill-name> skill..."

When one skill refers to another, write "use the `other-skill` skill if available" in the body instead of embedding one host's invocation syntax.

## Information Hierarchy

Place information at the highest level that needs it, and no higher:

- `SKILL.md`: core procedure, decision points, completion criteria, and links to references.
- `references/`: details loaded only for a branch, variant, framework, example set, or longer rubric.
- `scripts/`: deterministic operations that should not be rewritten each time.
- `assets/`: templates or files used as output material.

Avoid deeply nested references. Link reference files directly from `SKILL.md`.

## Split Or Prune

Split a skill when:

- A branch has a distinct trigger and can stand alone.
- Later steps cause the agent to rush earlier legwork.
- The body is carrying details that only one path needs.

Prune a skill when:

- A sentence does not change behavior.
- The same rule appears in multiple places.
- A paragraph explains what a capable agent already does by default.
- The skill preserves stale setup notes, rationale, or history that does not affect execution.

## Completion Criteria

Every workflow step should end with a checkable condition. Prefer criteria such as:

- "All changed files are listed."
- "Every work unit has dependencies and verification."
- "The exact failing command has been run and reported."

Avoid vague criteria such as "be thorough", "consider edge cases", or "make it good" unless followed by concrete checks.

Read `references/glossary.md` when reviewing a skill and you need the vocabulary for issues such as context load, progressive disclosure, duplication, no-op instructions, or premature completion.
