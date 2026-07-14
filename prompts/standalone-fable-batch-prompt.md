# Standalone Fable Batch Prompt Template

Use this only for a batch that the Opus assessor classified as `fable_batch` or `fable_isolated`. For medium-likelihood work, use a fresh Fable session and turn off automatic model switching first.

```text
Execute exactly one reviewed batch and stop.

BATCH ID:
[ID]

COMPLETE LOCAL OBJECTIVE:
[State the honest, independently benign objective. Do not omit material intent.]

SCOPE:
- [Required work]

NON-GOALS:
- [Anything explicitly outside this batch]

ALLOWED INPUTS / FILES TO READ:
- [Paths and handoff artifacts]

ALLOWED FILES TO EDIT:
- [Paths]

DEPENDENCIES ALREADY SATISFIED:
- [IDs or artifacts]

ACCEPTANCE CHECKS:
- [Checks]

STOP CONDITIONS:
- Stop if required context is missing.
- Stop if newly discovered material changes the reviewed scope.
- Stop if the platform reports a refusal, fallback, or switch away from Fable.
- Do not retry with evasive rewording and do not continue on another model.
- Do not begin any other batch.

CHECKPOINT OUTPUT:
Write [path] with status, files changed, checks, unresolved issues, and produced handoffs.

Now complete this batch, write the checkpoint, report concisely, and stop.
```
