# Reviewer Investigation Protocol

How an AI reviewer should navigate a change to find issues. This governs *movement through the code*,
not *what a finding must prove* — evidence contract, severity, and suppression stay in
`finding-contract.md`, `severity-rubric.md`, and `false-positive-patterns.md`.

A reviewer is not a coding assistant. A coding assistant maps a whole area before it acts; a reviewer
starts from the diff, asks whether the change introduced a problem, and looks for the narrowest nearby
evidence. Broad repository browsing wastes cost and pulls the review off the changed lines. Anchor
every move to the diff.

## Protocol

1. **Start from the diff.** Turn each changed hunk into a specific review question
   (e.g. "does this new early return skip the retry?"). Investigate questions, not the whole module.
2. **Narrow before reading.** When repository access is available, use grep/glob to locate candidate
   lines first, then read only those ranges. Do not open files to map an area.
3. **Batch discovery.** Issue cheap discovery calls (grep/glob/file list) together, not one at a time.
4. **Read with known ranges.** Open a file only to answer a formed question, and only at the line
   range that answers it. No exploratory full-file reads.
5. **No search↔read ping-pong.** Batch focused reads after discovery. Do not alternate
   search → read → search → read; that pattern signals browsing, not investigating.
6. **Stay anchored.** Keep every step tied to a changed line or its nearest evidence. If a thread
   leaves the change's blast radius, stop and return to the diff.

## Degraded mode (diff only, no repository access)

When only a diff/patch/snippet is provided, steps 2–4 collapse to: reason from the changed lines and
the immediately surrounding context in the provided evidence. Do not invent repository structure. If
answering a review question requires code that is not in the provided evidence, raise it as a targeted
question instead of a finding.

## Relationship to evidence gating

Navigation does not license findings. A finding still requires change evidence plus supporting
evidence per `context-discovery.md`. This protocol makes the reviewer reach that evidence efficiently;
it does not lower the bar for reporting.
