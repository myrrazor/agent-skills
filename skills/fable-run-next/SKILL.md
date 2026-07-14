---
name: fable-run-next
description: Manually execute exactly one reviewed Fable-eligible batch from a generated queue, write a checkpoint, and stop at the model-routing boundary.
---

Execute exactly one reviewed batch from the Fable queue identified by `$ARGUMENTS`.

Rules:

1. Read only the queue, its referenced batch prompt, listed inputs, and files necessary to complete that batch.
2. Do not read the complete route plan, assessment narrative, Opus queue, Opus prompts, or unrelated workflow material.
3. Confirm that the batch is pending, its dependencies and handoff artifacts are satisfied, and its scope is independently complete.
4. Perform only that batch. Do not start the next batch, even when time remains.
5. If newly encountered context materially changes the reviewed scope, stop and mark the batch `needs_reassessment`.
6. If the platform reports a refusal, model fallback, model mismatch, or a switch away from Fable, stop. Do not continue the batch on another model and do not repeatedly rephrase it.
7. Run only the acceptance checks listed in the batch prompt, plus minimal checks needed to verify edits.
8. Write the requested checkpoint and concise handoff. Report files changed, checks run, unresolved issues, and the next queue action.
9. Never conceal intent, encode content, split an ineligible objective into smaller prompts, or omit safety-relevant context to change routing.
10. Stop after the checkpoint.
