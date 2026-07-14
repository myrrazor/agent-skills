# Fable 5 Guardrail-Aware Workflow Router

This repository contains a small, model-aware workflow router for Claude Code projects that use Claude Fable 5 and Opus.

It assesses a complete workflow first, separates independently eligible Fable work from Opus work, and executes one reviewed Fable batch at a time. The goal is clearer routing and cleaner context boundaries when a legitimate task may trigger a safeguard fallback.

This is not a jailbreak, guardrail bypass, keyword-avoidance system, or prompt-laundering tool. It never recommends disguising intent, splitting a protected objective into benign-looking fragments, or retrying altered wording to hunt for a different classifier result.

## What is included

- `skills/fable-route-plan/` — portable skill core for assessing a full workflow.
- `skills/fable-run-next/` — portable skill core for executing one reviewed Fable batch.
- `claude/` — Claude Code adapters and subagent definitions that add model and agent routing metadata.
- `references/`, `schemas/`, `prompts/`, and `examples/` — supporting material for the router.
- `scripts/summarize_calibration.py` — summarize local fallback observations without third-party packages.
- `calibration/calibration-log.csv` — an empty CSV template for local calibration data.

The `skills/` folders follow the portable Agent Skills layout and contain only standard frontmatter. The `claude/` files add Claude Code-specific model, fork, and subagent settings, so other clients can reuse the skill instructions but may need their own worker configuration.

## Install in a Claude Code project

Clone the repository, then copy the portable skills and Claude companion agents into the project:

```bash
git clone https://github.com/myrrazor/Agent-Skills.git
cd Agent-Skills

mkdir -p /path/to/project/.claude/skills /path/to/project/.claude/agents
cp -R claude/skills/fable-route-plan /path/to/project/.claude/skills/
cp -R claude/skills/fable-run-next /path/to/project/.claude/skills/
cp claude/agents/fable-risk-assessor.md /path/to/project/.claude/agents/
cp claude/agents/fable-safe-worker.md /path/to/project/.claude/agents/
```

Restart Claude Code if `.claude/skills/` did not exist when the session started.

For another Agent Skills-compatible client, install the folders under `skills/` in that client's skill directory. The assessment and worker model settings may need an equivalent client-specific configuration.

## Use the router

### 1. Assess the complete workflow on Opus

Start a dedicated Opus session and assess the objective before implementation:

```bash
claude --model opus --name fable-router
```

Then run:

```text
/fable-route-plan @WORKFLOW.md
```

The assessor writes a run directory under `.claude/fable-routing/<workflow-id>/` containing:

- `assessment.md` — the human-readable task matrix and execution strategy.
- `route-plan.json` — the complete controller-only route plan.
- `fable/queue.json` — only independently eligible Fable batches.
- `fable/prompts/` — complete prompts for those Fable batches.
- `opus/prompts/` — prompts for Opus-routed work.
- `checkpoint.json` — resumable workflow state.

Review the assessment before executing any batch. The likelihood labels are heuristics, not access to Anthropic's private classifier scores.

### 2. Execute one reviewed Fable batch

Start a fresh Fable session:

```bash
claude --model fable --name fable-safe-work
```

Run one pending batch:

```text
/fable-run-next .claude/fable-routing/<workflow-id>/fable/queue.json
```

Repeat the command for the next eligible batch. If the platform flags the request or switches models, stop that batch and route it through the generated Opus prompt. Do not reword the request to search for a bypass.

## Example workflow

```text
1. Update the account settings page to use the new design tokens.
2. Fix a cache TTL regression in an HTTP client and add regression tests.
3. Perform an authorized penetration-test workstream described in the internal engagement brief.
4. Update the ordinary product release notes for tasks 1 and 2.
```

The router should keep task 1 in a normal Fable batch, isolate or conservatively route task 2, send task 3 to Opus, and defer task 4 until its real dependencies complete. The Fable queue must not contain the penetration-test brief or a summary of the Opus-only task.

See [`examples/sample-assessment.md`](examples/sample-assessment.md) for the expected matrix format.

## Safety boundaries

The router evaluates the whole objective rather than trying to exploit wording. It routes work conservatively when it is high-risk, unknown, materially enables a sensitive objective, or requires protected context. It also keeps Opus-only prompts and raw protected material out of the Fable queue.

The rubric is a planning aid. It does not decide whether work is authorized, legal, or safe, and it is not a substitute for human review or the model provider's safeguards.

## Calibration

Record observed outcomes locally using the CSV columns in `calibration/calibration-log.csv`. Keep personal or project-sensitive notes in an ignored `calibration/*.local.csv` file instead of committing them.

Summarize a calibration file with:

```bash
python3 scripts/summarize_calibration.py calibration/calibration-log.csv
```

Small samples should not be treated as reliable probabilities. Recalibrate after meaningful Claude Code or safeguard changes.

## Development checks

This repository intentionally has no runtime dependency. Run the focused test suite with:

```bash
python3 -m unittest discover -s tests -v
```

The test suite covers the calibration summarizer's normal and invalid-input paths. The JSON route-plan schema can be checked with Python's standard library:

```bash
python3 -m json.tool schemas/route-plan.schema.json >/dev/null
```

## Sources and contributions

The research notes in [`SOURCES.md`](SOURCES.md) identify the primary Claude Code and Anthropic sources used for the routing guidance. Contributions should keep the complete objective visible, preserve honest authorization context, and add or update tests for scripts and schemas.

Before opening an issue or pull request, remove local routing runs, credentials, private paths, and sensitive calibration notes from the proposed diff.

## License

MIT. See [`LICENSE`](LICENSE).
