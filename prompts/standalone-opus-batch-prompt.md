# Standalone Opus Batch Prompt Template

```text
Execute exactly this Opus-routed batch and stop.

BATCH ID:
[ID]

OBJECTIVE AND FULL RELEVANT CONTEXT:
[Complete context, including authorization assumptions and any safety-sensitive facts needed for correct execution.]

DEPENDENCIES / INPUTS:
- [Paths, task IDs, or artifacts]

REQUIRED WORK:
- [Work]

ALLOWED EDITS:
- [Paths]

ACCEPTANCE CHECKS:
- [Checks]

HANDOFF CONTRACT:
Produce only these artifacts for later independently safe batches:
- [Artifact path and exact contents/constraints]

Do not copy the full conversation or unnecessary sensitive procedures into the handoff. Do not begin a later Fable batch. Update [checkpoint path], report the result, and stop.
```
