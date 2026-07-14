# Fable 5 Fallback-Likelihood and Routing Rubric

This rubric predicts the likelihood of a Claude Fable 5 safeguard fallback. It does not determine whether a request is morally acceptable, legal, or authorized, and it does not expose Anthropic's private classifier thresholds.

## 1. Score the whole workflow before the parts

First write the complete end state in one sentence. Then ask:

- What capability or outcome does the full workflow produce?
- Do the outputs of separate tasks combine into something more sensitive than each task alone?
- Does a benign-looking task operationalize, validate, deploy, scale, conceal, or complete a sensitive task?
- Are authorization, ownership, target identity, or deployment environment material?

If a task materially enables a sensitive objective, set `whole_objective_relation` to `enables_sensitive` or `inseparable` and route it with that objective. Never split a protected objective into apparently harmless prompts and stitch the outputs together.

## 2. Assess context before prompt wording

Set a `context_baseline` for the environment:

- **Low**: ordinary application code and instructions, no substantial trigger-prone repository material.
- **Medium**: systems/networking code, security tooling, life-science terminology, ML training infrastructure, sensitive filenames, or custom instructions that may introduce ambiguous context.
- **High**: offensive-security repositories, substantive biology/chemistry work, frontier-model training or distillation work, or instructions that request private reasoning reproduction.
- **Unknown**: relevant context was not inspectable.

Check the visible task and likely hidden/automatic context: `CLAUDE.md`, rules, skill descriptions and content, hooks, MCP resources, git status, directory names, tool output, prior turns, and generated output.

## 3. Classifier families

### Cyber

**High likelihood** normally includes prohibited or high-risk dual-use activity such as malware or offensive infrastructure, destructive effects, defense evasion, exfiltration, unauthorized access, credential attacks, authentication bypass, privilege escalation, lateral movement, persistence, exploit weaponization, VM/container escapes, penetration testing, red teaming, bug bounty exploitation, high-uplift vulnerability discovery, and assessments of critical infrastructure.

**Medium likelihood** includes legitimate but classifier-adjacent activity: vulnerability identification with common tools, OSINT and public enumeration, protocol and TLS research, low-level HTTP/networking behavior, operating-system internals, incident artifacts, security logs, dependency advisories, secure-code fixes, and routine DevOps where surrounding context resembles offensive workflows. These may be intended to be allowed but can fall inside Fable's large safety margin.

**Low likelihood** includes ordinary product code, UI work, data transformations, tests, documentation, and general IT work with clearly defensive and non-operational context. Context can still raise the score.

### Biology and chemistry

**High likelihood** includes substantive biological or chemical research, dangerous lab methods, molecular mechanisms, experimental design, pathogen or vector engineering, and work requiring detailed wet-lab procedures. Current Claude Code guidance says substantive biology work should be expected to reroute frequently.

**Medium likelihood** includes biology-adjacent software, biomedical terminology, literature processing, sequence/data pipelines, chemical names, and repositories where the desired coding task is routine but the surrounding artifacts are substantive.

**Low likelihood** includes ordinary software tasks that do not require biological or chemical content. Merely stating a beneficial purpose does not necessarily reduce classifier likelihood.

### Frontier-model development and distillation

**High likelihood** includes work that materially assists extraction, imitation, distillation, or competitive development of a frontier model's capabilities, especially at scale.

**Medium likelihood** includes benign ML infrastructure, training pipelines, evals, synthetic-data systems, model-output harvesting, or optimization work whose scale and intent are ambiguous.

**Low likelihood** includes ordinary application use of model APIs, prompt integration, analytics, and non-frontier ML tasks with no extraction or competitive-training objective.

### Reasoning extraction

**High likelihood** includes requests to reproduce hidden chain-of-thought, private scratchpads, or verbatim internal reasoning. Ask instead for concise conclusions, assumptions, decision criteria, verification steps, or a short rationale. Do not ask the model to expose private internal reasoning.

### Multiple or unknown

Use `multiple` when more than one family is materially implicated. Use `unknown` when the evidence is incomplete or the category does not map cleanly.

## 4. Fallback-likelihood bands

### Low

Use when all are true:

- the task is independently benign;
- its complete local objective is outside protected domains;
- required inputs and likely outputs are low-risk;
- repository/customization baseline is low;
- it does not enable a sensitive downstream objective.

Route: `fable_batch`. Low does not mean guaranteed.

### Medium

Use when the task is independently benign but one or more are true:

- subject matter is adjacent to a protected domain;
- raw logs, protocols, low-level systems code, biomedical terms, ML training infrastructure, or ambiguous artifacts are required;
- the repository baseline is medium;
- independent reports or local history show false positives for similar work;
- output-side triggering is plausible.

Route: `fable_isolated`, one fresh session per batch, automatic switching disabled. On a flag, stop and route the batch to Opus. Do not iterate on wording to search for a bypass.

### High

Use when any are true:

- the task matches a protected or high-risk activity;
- substantive biology/chemistry or offensive-security work is required;
- frontier-model extraction/distillation is the objective;
- hidden reasoning reproduction is requested;
- the task must consume raw high-risk artifacts;
- it enables or completes a protected objective;
- the workspace baseline is high and cannot be separated without omitting relevant context.

Route: `opus` or `human_review`.

### Unknown

Use when relevant intent, authorization, files, dependencies, or context cannot be determined. Do not force a low or medium label.

Route: `opus` assessment or `human_review`.

## 5. Confidence

- **High confidence**: official category mapping and complete task/context information strongly agree.
- **Medium confidence**: task is clear, but classifier behavior is known to be broad or context-sensitive.
- **Low confidence**: missing context, novel task shape, or conflicting evidence.

Likelihood and confidence are different. A task can be `medium` likelihood with `high` confidence.

## 6. Dependency and ordering rules

1. Build a dependency graph before reordering.
2. Run low-likelihood independent work first.
3. Run medium-likelihood independent work next, one fresh Fable session per batch.
4. Route high/unknown/enabling/inseparable work to Opus.
5. Do not execute a downstream Fable task until required Opus handoffs exist.
6. After Opus, provide Fable only reviewed result artifacts needed for its independent task—not the Opus transcript or protected procedures.
7. If a high-risk task is a prerequisite and its output makes downstream work sensitive, route those downstream tasks to Opus too.

## 7. Prompt-generation rules

A Fable prompt must be complete and honest about its local objective. It may minimize unrelated context, but must not omit material intent or authorization. It must not be a disguised version of an Opus task.

Every Fable prompt should include:

- objective;
- scope and non-goals;
- allowed inputs and paths;
- allowed edits;
- acceptance checks;
- stop conditions;
- checkpoint path;
- instruction to execute one batch and stop.

Every Opus prompt should include the complete context required for safe, correct execution and the exact handoff artifacts later batches may consume.
