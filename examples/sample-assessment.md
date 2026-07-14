# Example Assessment Output

## Baseline

Context baseline: **medium** because the repository contains networking code and an unrelated authorized security workstream.

| ID | Task | Dependencies | Likelihood | Confidence | Family | Whole-objective relation | Lane |
|---|---|---|---|---|---|---|---|
| T1 | Apply design tokens to account settings | — | Low | High | None | Independent benign | Fable batch |
| T2 | Fix HTTP cache TTL regression and tests | — | Medium | Medium | Cyber-adjacent | Independent benign | Isolated Fable |
| T3 | Execute authorized penetration-test workstream | — | High | High | Cyber | Safety-sensitive | Opus |
| T4 | Write release notes for T1 and T2 | T1, T2 | Low | High | None | Independent benign | Fable batch |

## Strategy

1. Run T1 in a fresh Fable session.
2. Run T2 alone in another fresh Fable session with ask-before-switch enabled. On a flag, stop and route T2 to Opus rather than rewording it.
3. Run T3 only in the Opus session. Do not expose its brief or transcript to Fable.
4. After T1 and T2 complete, run T4 in a cleared or new Fable session.

This is illustrative only; real classification depends on the actual workflow and workspace context.
