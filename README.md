# Shared Agent Skills

Portable `SKILL.md` skill and Claude Code plugin for choosing which AI agents should lead, review, execute, and log work across hosted workflows.

This package is project-agnostic. It does not assume a specific model, provider, repository, operating system, or that Claude/Codex is always the lead.

## What You Get

- A portable `agent-routing-orchestrator` skill.
- Claude Code plugin metadata for plugin-style installation.
- Standalone install scripts for Codex, Claude, and `.agents` skill folders.
- Host-aware recommendations for Codex, Claude Code, subagents, remote coding agents, CI workers, and human-managed chats.
- Session-log rules for decisions, reviews, routing choices, escalations, and verification.
- Validation that prevents the standalone skill and plugin skill copy from drifting.

## Why This Exists

Most Codex/Claude integrations answer "how do I call the other agent?" This skill answers the earlier question: "who should lead, who should review, who should execute, and how do we prove the decision was safe?"

It is designed to be better than a single-agent wrapper by adding:

- Host-aware routing for Codex, Claude Code, subagents, remote coding agents, CI workers, and human-managed chats.
- Cost-aware model/agent selection that keeps high-quality agents on decisions and cheaper safe agents on routine execution.
- Normal review, adversarial review, co-lead council, and rescue/delegation playbooks.
- Required session-visible logs for decisions, reviews, routing choices, escalations, and verification.
- Both Claude Code plugin installation and standalone skill installation.

This package does not vendor another agent runtime. It contains only the routing skill, plugin metadata, install scripts, docs, and validation.

## When To Use It

Use this skill when an AI workflow needs a clear operating model:

- You want Claude, Codex, another agent, or a human-managed session to lead the process.
- You need to decide whether work should be done locally, by subagents, by remote coding agents, or by another chat.
- You want quality-first decisions but cheaper execution for routine implementation.
- You need co-lead review for architecture, product, security, data, expensive, or hard-to-reverse decisions.
- You want decisions, reviews, routing choices, and verification results visible in the session log.

Do not use it for tiny single-step tasks where no delegation, review, routing, or durable decision is involved.

## Requirements

- An agent host that supports skills or Claude Code plugins.
- Git for cloning the repository.
- Python 3 only if you want to run `scripts/validate.py`.
- The external agents or CLIs you route to must already be installed and authenticated; this skill chooses routes and guardrails, it does not vendor another agent runtime.

## Quick Start

After installation, mention the skill in your first prompt:

```text
Use agent-routing-orchestrator.

Host: Codex single session.
Lead: Codex.
Execution: local unless parallel subagents clearly save time.
Cost mode: balanced.
Autonomy: ask-on-stop-rules.
Session log: decisions and reviews in the active session.
Verification: run tests or explain why they cannot run.
```

The agent should normalize the routing contract, recommend who leads and executes, log decisions and reviews in the session, and verify before reporting success.

## First Useful Runs

```text
Use agent-routing-orchestrator to review this branch before shipping.
Host: Claude Code.
Review: independent reviewer if available.
Execution: review-only unless I approve fixes.
Session log: include verdict, risks, and verification gaps.
```

```text
Use agent-routing-orchestrator to hand this failing test investigation to the cheapest safe executor.
Host: Codex.
Cost mode: balanced.
Autonomy: ask before broad rewrites.
Session log: routing choice, task packet, completion packet, verification.
```

```text
Use agent-routing-orchestrator to challenge this architecture.
Host: human-managed multi-chat.
Lead: this chat.
Co-lead: another high-quality agent if available.
Session log: proposal, objections, reconciliation, final decision.
```

## Install

Clone or download this repository, then install into your agent skill directory.

```bash
git clone https://github.com/ramsaijanapana/shared-agent-skills.git
cd shared-agent-skills
```

### Claude Code Plugin

Use this when Claude Code is the host and you want plugin-style installation:

```text
/plugin marketplace add ramsaijanapana/shared-agent-skills
/plugin install agent-routing-orchestrator@shared-agent-skills
/reload-plugins
```

After reload, ask Claude Code to use `agent-routing-orchestrator`.

### Windows / PowerShell

```powershell
# Install for both Codex and Claude user skill directories
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target both

# Or install one target
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target codex
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target claude
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target agents
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target all
```

Inspect install scripts before using `ExecutionPolicy Bypass`.

### macOS / Linux

```bash
# Install for both Codex and Claude user skill directories
sh ./install.sh both

# Or install one target
sh ./install.sh codex
sh ./install.sh claude
sh ./install.sh agents
sh ./install.sh all
```

### Standalone Manual Install

Copy the skill folder into any supported skill directory:

```text
skills/
  agent-routing-orchestrator/
    SKILL.md
```

Common user-level locations:

```text
~/.codex/skills/
~/.claude/skills/
~/.agents/skills/
```

Common project-level locations include `.claude/skills/`, `.agents/skills/`, and `.github/skills/`.

Restart or reload your agent if it does not discover newly installed skills during an active session.

## Usage

The skill triggers from its `description` frontmatter.

Use `agent-routing-orchestrator` when Claude, Codex, another coding agent, subagents, or external assistants need to be chosen as lead, co-lead, reviewer, or executor.

For detailed examples, see [docs/USAGE.md](docs/USAGE.md). For the design principles behind the package, see [docs/DESIGN-PRINCIPLES.md](docs/DESIGN-PRINCIPLES.md).

### Routing Contract Template

You can include a compact contract in your first prompt and omit fields you do not care about:

```text
Use agent-routing-orchestrator.

Host: Claude Code single session.
Co-leads: highest-quality configured Claude + highest-quality configured Codex.
Execution: Claude subagents.
Autonomy: autonomous unless stop-rules trigger.
Cost mode: quality-first for decisions, cheapest safe tier for execution.
Manual review: destructive data edits, licensing, acceptance-criteria changes, major spend, co-lead disagreement.
Context: keep working state under 300 words; pass artifact paths, not full logs.
Session log: provide decisions and reviews in the active session; use .planning/AGENT-SESSION-LOG.md for long-running work.
```

### Common Recommendations

| Workflow | Recommendation |
|---|---|
| Small reversible task | One host agent leads and executes locally. |
| Bounded implementation | Host leads; standard worker or subagent executes a narrow file-owned task. |
| Architecture, security, data, or product decision | Use highest-quality lead or co-leads before implementation. |
| Several independent edits | Host leads; parallel workers execute non-overlapping tasks. |
| Remote coding agents | Host leads; remote agents receive compact packets and return completion packets. |
| Human-managed multi-chat process | Pick one lead chat; all other chats execute or review bounded packets. |

### Session Log Expectations

The skill requires important choices to be visible in the active session. For long-running work, also use a durable log file when the project has a place for one.

```text
[time] decision|review|routing|escalation|verification
Context: one sentence.
Recommendation: chosen path or verdict.
Reason: key evidence or tradeoff.
Owner: lead/reviewer/executor.
Next: immediate action or stop gate.
```

## Validate

```bash
python scripts/validate.py
```

## Package Layout

```text
.claude-plugin/marketplace.json
plugins/agent-routing-orchestrator/
  .claude-plugin/plugin.json
  skills/agent-routing-orchestrator/SKILL.md
skills/agent-routing-orchestrator/SKILL.md
docs/
scripts/validate.py
```

The standalone skill is the source of truth. Validation fails if the plugin copy drifts.

## License

MIT. See `LICENSE`.
