---
name: fable-route-plan
description: Manually assess an entire Claude Code workflow for Claude Fable 5 fallback likelihood, dependency order, context exposure, and model routing. Run from an Opus session before execution.
argument-hint: "<workflow text, @file, or path>"
disable-model-invocation: true
context: fork
agent: fable-risk-assessor
effort: xhigh
---

Assess the complete workflow supplied in `$ARGUMENTS` before any implementation begins.

This is a routing and task-isolation exercise, not an attempt to defeat a safeguard. Apply the full instructions in the assessor agent and the rubric below.

## Routing rubric

Score the whole workflow before scoring individual tasks.

- **Low**: independently benign work with low-risk context. Use `fable_batch`.
- **Medium**: independently benign work with ambiguous, protocol-adjacent, or security-adjacent context. Use `fable_isolated`, one fresh Fable session per batch.
- **High**: protected or high-risk work, raw protected context, offensive security, substantive biology or chemistry, frontier-model extraction, or hidden-reasoning extraction. Use `opus` or `human_review`.
- **Unknown**: material intent, authorization, dependencies, or context cannot be determined. Use `opus` or `human_review`.

Route a task with `enables_sensitive` or `inseparable` whole-objective relation alongside the sensitive objective, even if the local wording looks benign. Build the dependency graph before ordering work. Preserve material intent and authorization context in every prompt.

Use `multiple` when more than one classifier family applies. Use high confidence only when the task and context are clear; likelihood and confidence are separate fields. Never use euphemisms, encoding, fragmentation, omitted context, or repeated rewording to obtain a different safeguard result.

Required behavior:

1. Display the assessment matrix and execution strategy first.
2. Evaluate the whole objective, cumulative effect, dependencies, required files, likely tool outputs, and relevant workspace context—not isolated wording alone.
3. Assign each atomic task a fallback-likelihood band, confidence, classifier family, whole-objective relation, and execution lane.
4. Route any task that enables or is inseparable from a high-risk objective with that objective, even when its local wording appears benign.
5. Order independently eligible low-risk work first, then independently eligible medium-risk work in isolated Fable sessions, while preserving genuine dependencies.
6. Generate separate Fable and Opus queues. Never put protected-task descriptions or raw protected context in the Fable queue.
7. Generate complete task prompts, acceptance checks, stop conditions, handoff contracts, and an initial checkpoint.
8. Do not execute project work. Only inspect, assess, and write routing artifacts.
9. Never use euphemisms, encoding, fragmentation, omitted material intent, or repeated rewording to obtain a different classifier result.
10. If information is missing, mark the affected item `unknown` and route conservatively rather than asking a follow-up.

Default output root: `.claude/fable-routing/<short-workflow-id>/`.
