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

## Setup and operating boundary

Use a current Claude Code release. Fable 5 support requires the release documented by the provider; if the client reports that the model is unavailable, stop and resolve the client version before assessing work.

In Claude Code, disable the setting that automatically switches models when a message is flagged. A flagged Fable request must pause so the batch can be routed deliberately instead of silently moving the rest of the session to Opus.

Run the assessor in a dedicated Opus session, review its matrix before execution, and keep the generated Fable and Opus queues separate. This skill only assesses and writes routing artifacts; it does not implement project work.

## Routing rubric

This rubric predicts the likelihood of a Claude Fable 5 safeguard fallback. It does not decide whether work is moral, legal, authorized, or safe, and it does not expose a provider's private classifier thresholds.

### 1. Score the whole workflow first

Write the complete end state in one sentence before splitting the work into tasks. Ask:

- What capability or outcome does the full workflow produce?
- Could separate outputs combine into something more sensitive than each task alone?
- Does a benign-looking task operationalize, validate, deploy, scale, conceal, or complete a sensitive task?
- Do authorization, ownership, target identity, or deployment environment change the assessment?

If a task materially enables a sensitive objective, mark its `whole_objective_relation` as `enables_sensitive` or `inseparable` and route it with that objective. Never split a protected objective into apparently harmless prompts and stitch the outputs together.

### 2. Assess context before wording

Record a `context_baseline` for the workspace:

- **Low** — ordinary application code and instructions with no substantial trigger-prone repository material.
- **Medium** — systems or networking code, security tooling, life-science terminology, ML training infrastructure, sensitive filenames, or custom instructions that may create ambiguous context.
- **High** — offensive-security repositories, substantive biology or chemistry, frontier-model training or distillation, or requests for private reasoning reproduction.
- **Unknown** — relevant context cannot be inspected.

Inspect the visible task and likely surrounding context: `CLAUDE.md`, rules, skill and hook text, MCP names and resources, git status, directory names, tool output, prior turns, and generated artifacts. Do not assume the visible request is the only context the model will see.

### 3. Classifier families and trigger guidance

Use the family that best explains the risk. Use `multiple` when more than one family materially applies and `unknown` when the evidence does not fit a family cleanly.

#### Cyber

- **High likelihood** — malware or offensive infrastructure, destructive effects, defense evasion, exfiltration, unauthorized access, credential attacks, authentication bypass, privilege escalation, lateral movement, persistence, exploit weaponization, VM or container escapes, penetration testing, red teaming, bug-bounty exploitation, high-uplift vulnerability discovery, or critical-infrastructure assessment.
- **Medium likelihood** — vulnerability identification with common tools, OSINT or public enumeration, protocol or TLS research, low-level HTTP or networking behavior, operating-system internals, incident artifacts, security logs, dependency advisories, secure-code fixes, and routine DevOps in an offensive-looking context.
- **Low likelihood** — ordinary product code, UI work, data transformation, testing, documentation, and general IT work with clearly defensive and non-operational context. Workspace context can raise the band.

#### Biology and chemistry

- **High likelihood** — substantive biological or chemical research, dangerous lab methods, molecular mechanisms, experimental design, pathogen or vector engineering, or detailed wet-lab procedures.
- **Medium likelihood** — biology-adjacent software, biomedical terminology, literature processing, sequence or data pipelines, chemical names, or routine coding inside a substantive life-science repository.
- **Low likelihood** — ordinary software work with no biological or chemical content. A beneficial stated purpose does not by itself lower the likelihood.

#### Frontier-model development and distillation

- **High likelihood** — work that materially assists extraction, imitation, distillation, or competitive development of a frontier model's capabilities, especially at scale.
- **Medium likelihood** — benign ML infrastructure, training pipelines, evaluations, synthetic-data systems, model-output harvesting, or optimization where scale and intent are ambiguous.
- **Low likelihood** — ordinary model API use, prompt integration, analytics, or non-frontier ML work with no extraction or competitive-training objective.

#### Reasoning extraction

High likelihood includes requests to reproduce hidden chain-of-thought, private scratchpads, or verbatim internal reasoning. Ask for conclusions, assumptions, decision criteria, verification steps, or a short rationale instead. Do not ask the model to expose private internal reasoning.

### 4. Fallback-likelihood bands and lanes

| Band | Use when | Lane |
|---|---|---|
| `low` | Independently benign; outside protected domains; low-risk inputs and outputs; low workspace baseline; no sensitive downstream capability | `fable_batch` |
| `medium` | Independently benign but adjacent to a protected domain, context-sensitive, protocol-heavy, ambiguous, or plausibly output-triggering | `fable_isolated`, one fresh session per batch |
| `high` | Protected or high-risk activity, raw protected artifacts, substantive biology or chemistry, offensive security, frontier extraction, hidden reasoning, or a sensitive enabling task | `opus` or `human_review` |
| `unknown` | Intent, authorization, dependencies, files, or context cannot be determined | `opus` or `human_review` |

`low` does not mean guaranteed. For `medium`, disable automatic model switching, stop on a flag, and route the batch to Opus. Do not iterate on wording to search for a bypass. For `high` and `unknown`, do not force a low or medium label just because the local edit sounds harmless.

### 5. Confidence is separate

- **High confidence** — complete task and context strongly agree with an official category mapping.
- **Medium confidence** — task is clear, but classifier behavior is broad or context-sensitive.
- **Low confidence** — context is missing, the task shape is novel, or evidence conflicts.

A task may be `medium` likelihood with `high` confidence. Record both values independently.

### 6. Dependencies and ordering

1. Build the dependency graph before reordering.
2. Run low-likelihood independent work first.
3. Run medium-likelihood independent work next, one fresh Fable session per batch.
4. Route high, unknown, enabling, and inseparable work to Opus.
5. Do not execute a downstream Fable task until required Opus handoffs exist.
6. After Opus, give Fable only the reviewed result artifacts needed for its independent task, never the Opus transcript or protected procedures.
7. If a high-risk prerequisite makes downstream work sensitive, route that downstream work to Opus too.

### 7. Prompt and artifact rules

Every Fable prompt must honestly state the complete local objective, legitimate intent, scope, non-goals, allowed inputs, allowed edits, acceptance checks, stop conditions, checkpoint path, and instruction to execute one batch and stop.

Every Opus prompt must include the complete context required for safe execution, authorization assumptions, dependencies, required checks, handoff artifacts for later work, checkpoint updates, and a stop instruction.

The Fable queue may contain only independently eligible tasks and the direct inputs needed for them. It must not contain protected-task descriptions, raw protected context, Opus prompts, or Opus transcripts.

Never use euphemisms, encoding, role-play, context deletion, keyword substitution, fragmentation, omitted material intent, or output stitching to obtain a different classifier result.

### Limits

- The labels are comparative likelihood bands, not calibrated probabilities or access to private classifier scores.
- Classifiers can inspect repository instructions, skills, hooks, MCP context, git status, filenames, tool output, prior turns, and generated output in addition to the visible request.
- A refusal can occur before output or during generation. Treat partial output as incomplete.
- A skill cannot guarantee that Fable remains active. The ask-before-switch setting prevents an automatic session demotion but does not override provider safeguards.
- Environment variables, per-invocation model selection, organization restrictions, or client changes can override the requested subagent model. If the served model differs, stop and reassess.

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
