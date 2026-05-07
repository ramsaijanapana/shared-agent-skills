# Agent Routing Orchestrator Usage

This guide shows how to use `agent-routing-orchestrator` and when each routing pattern fits.

## What The Skill Does

The skill helps an agent answer five questions before work begins:

- Where is the process hosted?
- Which agent leads?
- Which agents execute?
- Which reviews or approvals are required?
- How are decisions, reviews, and verification logged in the session?

The output should be a normalized routing contract, recommendations, task packets for executors when needed, a session-visible log, and verification evidence before success is claimed.

## Installation Choices

Use the Claude Code plugin path when Claude Code is the host:

```text
/plugin marketplace add ramsaijanapana/shared-agent-skills
/plugin install agent-routing-orchestrator@shared-agent-skills
/reload-plugins
```

Use standalone install scripts when you want the same skill available to Codex, Claude, `.agents`, or project-local skill folders:

```bash
git clone https://github.com/ramsaijanapana/shared-agent-skills.git
cd shared-agent-skills
sh ./install.sh all
```

On Windows:

```powershell
git clone https://github.com/ramsaijanapana/shared-agent-skills.git
cd shared-agent-skills
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target all
```

## When To Use It

Use it when:

- The work may involve multiple agents, subagents, external coding agents, or human-managed chats.
- You care which model or agent is trusted for decisions versus execution.
- The task has architecture, product, security, data, cost, licensing, or acceptance-risk decisions.
- You want routine execution to use cheaper safe agents while keeping high-quality review gates.
- You need a clear session log for decisions and reviews.

Skip it when the task is a trivial one-shot command or a tiny local edit with no meaningful routing choice.

## Minimal Prompt

```text
Use agent-routing-orchestrator.

Host: Codex.
Goal: implement the next roadmap task.
Autonomy: ask-on-stop-rules.
Session log: decisions and reviews in this session.
Verification: run relevant tests.
```

## Full Routing Contract

```text
Use agent-routing-orchestrator.

Host: Claude Code single session.
Lead: highest-quality configured Claude.
Co-lead: highest-quality configured Codex for architecture, security, product, data, or expensive decisions.
Execution: Claude subagents for bounded parallel work; local lead for integration.
Cost mode: quality-first for decisions, cheapest safe tier for execution.
Autonomy: autonomous unless stop-rules trigger.
Manual review: destructive edits, production data, licensing, major spend, acceptance-criteria changes, co-lead disagreement.
Context: keep worker packets under 300 words; pass artifact paths, not full logs.
Session log: active session plus .planning/AGENT-SESSION-LOG.md for long-running work.
Verification: tests, diff review, and acceptance criteria before success.
Do not touch: secrets, production data, generated migrations unless explicitly assigned.
```

## Hosting Examples

### Codex Single Session

Use when Codex is the only active orchestrator.

```text
Use agent-routing-orchestrator.

Host: Codex single session.
Lead: Codex.
Execution: local unless a subagent can own a disjoint task.
Review: self-check for routine work; peer review for architecture or security.
Session log: summarize routing, reviews, and verification in the active session.
```

Recommendation: Codex should lead and execute locally for narrow tasks. Use subagents only when they save time and have non-overlapping ownership.

### Claude Code With Codex As Co-Lead

Use when Claude Code hosts the process but Codex should challenge major decisions.

```text
Use agent-routing-orchestrator.

Host: Claude Code.
Lead: Claude.
Co-lead: Codex for risky decisions.
Execution: Claude subagents for bounded implementation.
Review: Codex reviews architecture, acceptance gates, and high-risk diffs.
Session log: log proposal, objections, reconciliation, and final decision.
```

Recommendation: Keep one primary host. Use the second agent for independent review before implementation, not as a competing executor.

### Remote Coding Agents

Use when work is delegated to background or cloud-hosted agents.

```text
Use agent-routing-orchestrator.

Host: Codex as orchestrator.
Lead: Codex.
Execution: remote coding agents receive one bounded task packet each.
Review: Codex inspects returned diffs and reruns the smallest sufficient checks.
Session log: routing, task packets, completion packets, and verification.
```

Recommendation: Remote agents should get narrow tasks with exact file ownership, acceptance checks, and stop rules. The host still owns integration.

### Human-Managed Multi-Chat Process

Use when the user manually opens multiple AI chats or tools.

```text
Use agent-routing-orchestrator.

Host: human-managed multi-chat.
Lead: this chat owns decisions and the session log.
Execution: other chats get bounded packets.
Review: a different chat reviews any high-risk implementation.
Session log: this chat records routing, reviews, decisions, and verification.
```

Recommendation: Pick one canonical lead chat. Other chats should act as executors or reviewers, not independent project leads.

## Review And Rescue Playbooks

### Review Before Shipping

```text
Use agent-routing-orchestrator.

Host: Claude Code.
Goal: review this branch before shipping.
Lead: Claude.
Review: Codex or another independent reviewer if available.
Execution: no implementation unless I ask after the review.
Session log: include review verdict, findings, files inspected, and verification gaps.
```

Recommendation: keep this review-only. If the reviewer finds issues, route fixes as a separate lead-and-implementer task.

### Challenge The Approach

```text
Use agent-routing-orchestrator.

Host: Codex.
Goal: pressure-test whether this architecture is the right approach.
Lead: Codex.
Co-lead: Claude if available.
Review: adversarial/challenge review focused on assumptions, tradeoffs, and failure modes.
Session log: proposal, objections, reconciliation, and final decision.
```

Recommendation: use co-lead council for architecture, security, data integrity, or expensive decisions.

### Delegate A Rescue Task

```text
Use agent-routing-orchestrator.

Host: Claude Code.
Goal: investigate why CI started failing and propose the smallest safe fix.
Lead: Claude.
Execution: Codex or a remote coding agent may investigate; implementation requires lead verification.
Autonomy: ask before broad rewrites.
Session log: routing choice, task packet, completion packet, and verification result.
```

Recommendation: give the executor exact ownership and stop rules. The lead still inspects the diff and runs checks.

### Start Background Work

```text
Use agent-routing-orchestrator.

Host: Claude Code.
Goal: run a long review in the background.
Execution: background only if status/result/cancel controls are available.
Session log: job handle, probe gate, and when to check results.
```

Recommendation: do not start async work unless the host can show status, return results, and cancel or resume safely.

## Cost Mode Examples

| Cost Mode | Best For | Recommendation |
|---|---|---|
| `quality-first` | Architecture, security, data integrity, acceptance gates, expensive work | Use frontier agents for decisions and review; delegate routine edits only after the decision is stable. |
| `balanced` | Normal feature work and bugfixes | Lead with the host agent, use standard workers for bounded tasks, escalate when ambiguity appears. |
| `budget` | Mechanical or repetitive work | Use cheap-fast agents only for reversible, objective, easy-to-check work. |

## Worker Task Packet

Use this shape when sending work to an executor:

```text
Goal: one bounded outcome.
Non-goals: what not to change.
Ownership: exact files or directories.
Context: artifact paths and key constraints.
Acceptance checks: commands or manual checks.
Stop rules: when to return blocked instead of guessing.
Return: result, files changed, checks run, risks, next action.
```

## Session Log Example

```text
[2026-05-06 21:10] routing
Context: package docs need public release prep and GitHub publication.
Recommendation: host agent leads locally; no subagents because edits are small and coupled.
Reason: documentation and install scripts are in one repo and require one final verification gate.
Owner: Codex.
Next: update README/usage guide, validate, commit, create public repo, push.

[2026-05-06 21:18] verification
Context: release docs and merged skill package are ready for validation.
Recommendation: package is ready to publish if validation passes.
Reason: scripts/validate.py passed and install script smoke test passed where available.
Owner: Codex.
Next: commit and push to public GitHub repo.
```

## Verification Checklist

Before calling work complete, the lead should verify:

- The routing contract was stated or safely inferred.
- Important decisions and reviews were logged in the active session.
- Executors had bounded ownership and returned completion packets.
- The lead inspected diffs or artifacts directly.
- Required tests or checks ran, or limitations were clearly reported.
