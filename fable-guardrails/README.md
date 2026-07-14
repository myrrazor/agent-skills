# Fable guardrails

Two Claude Code skills for routing a complete workflow between Fable 5 and Opus.

- `fable-route-plan` — assess the whole workflow and create separate queues.
- `fable-run-next` — execute exactly one reviewed Fable batch, then stop.
- `agents/` — the Opus assessor and Fable worker used by the skills.

This is a routing aid, not a jailbreak or guardrail bypass. It never hides intent, splits a sensitive objective into benign-looking prompts, or retries altered wording to search for a different result.

## Install

From the repository root, copy the skills and agents into a Claude Code project:

```bash
mkdir -p /path/to/project/.claude/skills /path/to/project/.claude/agents
cp -R fable-guardrails/fable-route-plan /path/to/project/.claude/skills/
cp -R fable-guardrails/fable-run-next /path/to/project/.claude/skills/
cp fable-guardrails/agents/*.md /path/to/project/.claude/agents/
```

Restart Claude Code if the project did not already have `.claude/skills/`.

## Use

Assess the complete objective in a dedicated Opus session:

```bash
claude --model opus --name fable-router
```

```text
/fable-route-plan @WORKFLOW.md
```

Review the matrix. Then start a fresh Fable session and run one batch:

```bash
claude --model fable --name fable-safe-work
```

```text
/fable-run-next .claude/fable-routing/<workflow-id>/fable/queue.json
```

Run the command again for the next pending batch. If Fable flags the work or the platform switches models, stop and use the generated Opus prompt. Do not reword the task to hunt for a bypass.

## Routing rubric

The route planner scores the complete workflow before splitting it into tasks.

- **Low** — independently benign, low-context work. Route to a normal Fable batch.
- **Medium** — benign work with ambiguous or security-adjacent context. Route to one fresh, isolated Fable session.
- **High** — protected or high-risk work, raw protected context, hidden-reasoning extraction, substantive biology/chemistry, offensive security, or frontier-model extraction. Route to Opus or human review.
- **Unknown** — missing intent, authorization, dependencies, or context. Route conservatively to Opus or human review.

Any task that enables, operationalizes, validates, deploys, or completes a sensitive objective inherits that objective's lane. Do not split a protected workflow into superficially harmless pieces.

Classify both likelihood and relation to the whole objective. A low likelihood label does not make an enabling task safe to send to Fable. When uncertain, preserve the complete intent and route conservatively.

The labels are heuristics, not access to a provider's private classifier scores. Human authorization and provider safeguards remain authoritative.
