---
name: agent-routing-orchestrator
description: Use when choosing which AI agents should lead, co-lead, review, or execute work across hosted sessions, including Claude, Codex, subagents, external coding agents, or parallel assistants. Also use when the user mentions cost-aware delegation, cross-agent leadership, agent routing, hosting the process, autonomy, approvals, model quality, session logs, or verification preferences.
license: MIT
metadata:
  shared-agent-skills.version: "0.5.0"
---

# Agent Routing Orchestrator

Use this skill to choose who leads, who reviews, who executes, and how the work is logged based on where the process is hosted.

The lead owns direction, scope, routing, integration, and verification. Executors own bounded implementation. Reviewers challenge decisions or inspect outputs. A task is complete only when the acceptance gate passes.

## Gaps This Skill Closes

The merged skill replaces separate leadership and cost-delegation skills. The split left five gaps:

- No single routing contract that combined host, lead, reviewer, executor, autonomy, cost, and verification.
- Hosting environment did not directly influence which agents should lead or execute.
- Cost-tier guidance was separate from co-lead and review guidance, so it was easy to choose good leaders but poor implementers.
- Session-visible decision and review logging was not required.
- Installers could leave stale legacy skills active after the merge.

## Start With A Routing Contract

Accept a user-provided contract. If it is incomplete, infer safe defaults, state them briefly, and proceed unless a missing value creates real risk.

Supported fields:

- `Host`: where the process is controlled, such as Codex, Claude Code, a remote coding agent, a CI job, or a human-managed set of chats.
- `Lead`: single lead, co-leads, or highest-quality available host agent.
- `Review`: peer reviewer, co-lead council, human review, or none for low-risk work.
- `Execution`: local lead, host subagents, external coding agents, CI workers, or human-assigned agents.
- `Cost mode`: `quality-first`, `balanced`, or `budget`.
- `Autonomy`: `autonomous`, `ask-on-stop-rules`, or `manual`.
- `Manual review`: destructive edits, data changes, licensing, spend, acceptance-criteria changes, security, production deploys, or co-lead disagreement.
- `Context limit`: default 300 words per worker packet.
- `Session log`: chat log only, durable file path, or both.
- `Verification`: tests, artifact checks, screenshots, command outputs, review gates, or acceptance criteria.
- `Do not touch`: files, systems, credentials, production data, or workflows.

Normalize user labels onto the roles below. User preferences override defaults unless unsafe, impossible in the current tools, or conflicting with higher-priority instructions.

## Readiness Check

Before routing to a named external agent, CLI, plugin, subagent, or background worker, verify that it is actually available in the current host when that can be checked cheaply.

Check only what matters for the requested route:

- Tool or plugin installed and callable.
- CLI present on `PATH` when a CLI is required.
- Authentication or setup complete enough to run the task.
- Repository/workspace visible to the executor.
- Background status/result/cancel/resume mechanism available if async work is requested.

If the preferred route is unavailable, recommend the closest safe fallback and log the limitation. Do not invent slash commands, subagents, or background controls that the host does not provide.

## Recommended Defaults

| Situation | Recommended Lead | Recommended Executors | Review |
|---|---|---|---|
| Small reversible task in one hosted session | Host agent | Host agent | Self-check plus acceptance gate |
| Bounded implementation with clear files | Host agent | `standard` worker or subagent with disjoint ownership | Lead reviews diff and runs checks |
| Several independent edits | Host agent | Parallel `standard` workers with non-overlapping file ownership | Lead integrates and verifies |
| Ambiguous architecture, product, security, or data decision | Highest-quality available agent or co-leads | Wait until decision is stable, then route execution | Independent peer or co-lead council |
| Remote or async coding agents | Host agent as orchestrator | Remote workers get narrow task packets | Lead reviews completion packets and reruns checks |
| Human-managed multi-chat workflow | One explicit lead chat | Other chats execute or review one packet each | Lead maintains session log and final decision |
| Budget-sensitive routine work | Host agent | Cheapest safe tier | Escalate only when ambiguity or failed checks require it |

Prefer a single lead unless the decision is high-risk, expensive, ambiguous, architectural, security-sensitive, or hard to reverse. Use co-leads for decisions, not routine edits.

## Hosting Profiles

### Single Hosted Session

Use when Codex, Claude Code, or another agent controls the whole workflow in one place.

- Lead: host agent.
- Executors: host agent by default; subagents only when they save time and have clear ownership.
- Reviewer: peer agent only for risky decisions or reviews.
- Log: concise decision and review notes in the active session; use a durable file for long tasks.

### Hosted Session With Subagents

Use when the host can spawn workers or explorers.

- Lead: host agent.
- Executors: workers for bounded, parallel, objectively checkable tasks.
- Reviewer: lead, or separate reviewer for high-risk diffs.
- Rule: never give two workers overlapping write ownership.

### Remote Or Async Agent Host

Use when work is delegated to remote coding agents, CI-style workers, or background jobs.

- Lead: the interactive host or designated orchestrator.
- Executors: remote agents receive compact task packets and completion-packet requirements.
- Reviewer: lead must inspect artifacts and rerun the smallest sufficient checks.
- Rule: every long-running task needs a probe or stop gate.

### Human-Managed Multi-Agent Process

Use when the user hosts separate chats or tools manually.

- Lead: choose one chat as the decision owner.
- Executors: other chats receive one bounded packet each.
- Reviewer: use a different agent than the implementer for meaningful review.
- Rule: the lead session keeps the canonical log and final decisions.

## Cost And Quality Tiers

Pick the cheapest safe tier, not the cheapest possible tier. Savings are invalid if they increase failure, rework, or supervision burden.

| Tier | Use For | Avoid For |
|---|---|---|
| `cheap-fast` | status checks, narrow doc edits, formatting, small tests, grep/read-only summaries | ambiguity, hidden coupling, irreversible edits |
| `standard` | bounded implementation, normal bugfixes, targeted test repair, small feature slices | architecture, security, product direction |
| `frontier` | architecture, hard debugging, code review, acceptance gates, data integrity, irreversible decisions | routine edits and monitoring |

Default to `standard` when risk is unclear. Use `cheap-fast` only for narrow, reversible, objectively checkable work. Use `frontier` immediately for ambiguous reasoning, architecture, security, data integrity, acceptance gates, hidden coupling, or expensive rework risk.

If a cheap tier fails because context was missing, improve the packet once. If it fails because reasoning or ambiguity exceeded the tier, escalate.

## Decision Modes

### Single Lead

Use when requirements are explicit, edits are reversible, and checks are objective. The lead decides, executes or delegates, verifies, and logs the result.

### Lead And Implementer

Use when direction is clear and execution can be bounded. The lead sends a context packet, the implementer returns a completion packet, and the lead verifies.

### Co-Lead Council

Use for architecture, product direction, ambiguous debugging, expensive work, security, data integrity, or high-risk implementation.

1. Lead A writes a compact proposal: goal, options, recommendation, risks, acceptance gate.
2. Lead B reviews independently: strongest objections, missing evidence, cheaper or safer alternative.
3. Lead A reconciles: accept, reject, or modify each objection.
4. Final decision packet: chosen path, rejected paths, why, owner, stop/probe gate.

Do not hand work to executors until co-leads agree or the unresolved disagreement is surfaced to the user.

## Review And Rescue Playbooks

Use these playbooks when the user asks for a common cross-agent workflow.

| User Intent | Recommended Mode | Output |
|---|---|---|
| "Review this before shipping" | Normal review by a reviewer different from the implementer when possible | Findings, severity, changed files inspected, verification gap |
| "Challenge this approach" | Co-lead council or adversarial review | Assumptions, strongest objections, safer alternatives, final decision |
| "Hand this problem to another agent" | Lead-and-implementer | Context packet, ownership, completion packet, lead verification |
| "Start this in the background" | Async execution only if host supports status/result/cancel | Job handle, probe/stop gate, status check plan |
| "Continue the previous run" | Resume only when a previous run can be identified | Prior context pointer, resumed goal, updated log entry |

Review-only work must not silently become implementation. Rescue or fix work must return through lead verification before it is treated as integrated.

## Session Log

Do not keep decisions and reviews only implicit. Provide them as a concise log in the active session. For long-running work, also keep a durable log file if the repo or user provides a place for it.

Default log entry format:

```text
[time] decision|review|routing|escalation|verification
Context: one sentence.
Recommendation: chosen path or verdict.
Reason: key evidence or tradeoff.
Owner: lead/reviewer/executor.
Next: immediate action or stop gate.
```

Log these events:

- Routing contract and inferred defaults.
- Lead, co-lead, reviewer, and executor choices.
- Co-lead proposals, objections, reconciliations, and final decision packets.
- Review verdicts and required changes.
- Escalations, blocked states, and manual-review triggers.
- Verification commands, outcomes, and acceptance decisions.

Keep the log useful, not noisy. For routine execution, summarize batches. For high-risk decisions or reviews, log each decision.

## Context Packet

Every delegated task gets a packet under 300 words by default:

- Goal and non-goals.
- Files or areas to read or edit.
- Do-not-touch list.
- Constraints and invariants.
- Acceptance checks.
- Expected output format.
- Escalation triggers.

Pass exact file, commit, artifact, or log pointers instead of whole histories. If more context is approved, summarize first.

## Completion Packet

Require every executor or reviewer to return:

- Result: `complete`, `partial`, or `blocked`.
- Files changed or inspected.
- Tests or checks run, with outcomes.
- Risks, assumptions, and unresolved questions.
- Commit hash or patch summary if applicable.
- Exact next action if blocked.

Worker-reported checks are evidence, not proof. The lead independently inspects the smallest relevant diff or artifact and reruns or directly validates the smallest sufficient acceptance checks.

## Stop Rules

Pause, ask, or escalate when:

- Requirements conflict.
- The requested agent, tool, or host is unavailable.
- An executor touches out-of-scope files.
- A result changes the architecture or product decision.
- A long-running task lacks a probe or stop gate.
- The context packet would exceed 300 words without good reason.
- Co-leads disagree and the disagreement affects implementation safety or direction.
- A check cannot be run but the user expects complete verification.

## Final Integration

Before reporting success:

- Verify acceptance checks directly.
- Confirm dirty worktree changes are expected.
- Update the session log with the final review and verification result.
- Report outcome, evidence, risks, and exact next step.

If acceptance checks cannot be run, report `partial` or `blocked`; do not call the task complete.
