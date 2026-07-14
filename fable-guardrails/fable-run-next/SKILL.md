---
name: fable-run-next
description: Manually execute exactly one reviewed Fable-eligible batch from a generated queue, write a checkpoint, and stop at the model-routing boundary.
argument-hint: "<path-to-fable-queue.json> [batch-id]"
disable-model-invocation: true
context: fork
agent: fable-safe-worker
effort: high
---

Execute exactly one reviewed batch from the Fable queue identified by `$ARGUMENTS`.

## Session boundary

Run this skill in a fresh Fable session for the selected batch, with automatic model switching disabled. The batch must already have been assessed in a dedicated Opus session. This runner performs one batch and stops; it never starts the next batch automatically.

## Routing matrix

This runner enforces a route plan; it does not replace the whole-workflow assessment. Use the following matrix when checking the selected batch:

| Band | Typical triggers | Required lane |
|---|---|---|
| `low` | Independently benign product code, UI, documentation, tests, or data work with low-risk context | Normal `fable_batch` |
| `medium` | Security-adjacent code, protocols, networking, raw logs, biomedical terms, ML infrastructure, ambiguous context, or plausible output-side triggering | `fable_isolated`, fresh session, automatic switching disabled |
| `high` | Malware, unauthorized access, credential attacks, exploit weaponization, offensive security, substantive biology or chemistry, frontier-model extraction, hidden reasoning, or raw high-risk artifacts | Opus or human review; do not run here |
| `unknown` | Missing intent, authorization, dependency, file, or context information | Opus or human review; request reassessment |

Any task marked `enables_sensitive` or `inseparable` inherits the sensitive objective's lane, even when the local edit appears benign. Likelihood and confidence are separate fields. A low likelihood label is not permission to run an enabling task.

### Trigger families

- **Cyber** — high-risk indicators include malware, destructive effects, defense evasion, exfiltration, unauthorized access, credential attacks, authentication bypass, privilege escalation, lateral movement, persistence, exploit weaponization, escapes, penetration testing, red teaming, bug-bounty exploitation, and critical-infrastructure assessment. Medium indicators include vulnerability identification, OSINT, enumeration, TLS or protocol research, low-level networking, incident artifacts, security logs, advisories, and secure-code fixes in an ambiguous context.
- **Biology and chemistry** — high-risk indicators include substantive research, dangerous lab methods, molecular mechanisms, experimental design, pathogen or vector engineering, and detailed wet-lab procedures. Medium indicators include biomedical terminology, literature processing, sequence pipelines, chemical names, or routine code inside a substantive life-science repository.
- **Frontier-model development** — high-risk indicators include capability extraction, imitation, distillation, or competitive development at scale. Medium indicators include training infrastructure, evaluations, synthetic-data systems, output harvesting, or ambiguous optimization work.
- **Reasoning extraction** — requests for hidden chain-of-thought, private scratchpads, or verbatim internal reasoning are high likelihood. Route requests for conclusions, assumptions, criteria, or verification steps instead.

Do not expose Opus transcripts, protected procedures, or unrelated sensitive context to Fable. Never disguise intent, omit authorization, split a sensitive objective into harmless-looking prompts, or retry altered wording after a flag.

## Stop conditions

Stop and mark the batch for reassessment when:

- the queue is not pending or its dependencies or handoffs are missing;
- the selected files, objective, authorization, or acceptance checks differ from the assessment;
- newly discovered context changes the likelihood, classifier family, or whole-objective relation;
- the served model is not Fable when Fable is required;
- the platform reports a refusal, fallback, model switch, or model mismatch;
- the task would materially enable or complete a sensitive objective.

Do not continue on a fallback model and do not start another batch in the same invocation.

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
