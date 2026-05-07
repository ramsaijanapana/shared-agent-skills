# Design Principles

This package is built around one idea: agent workflows need routing discipline before they need more automation.

## Core Principles

| Principle | How This Package Applies It |
|---|---|
| Choose the lead first | One agent owns direction, scope, integration, and verification. |
| Separate decisions from execution | High-quality agents handle high-risk decisions; cheaper safe agents can handle routine bounded work. |
| Make reviews explicit | Review-only, challenge review, co-lead council, and rescue work each have different expectations. |
| Check readiness before routing | A named tool, CLI, plugin, worker, or background mechanism must exist before the lead routes work to it. |
| Keep handoffs small | Executors get compact task packets with ownership, non-goals, checks, and stop rules. |
| Verify before completion | Worker output is evidence, not proof; the lead verifies before reporting success. |
| Log important choices | Decisions, reviews, routing choices, escalations, and verification results stay visible in the session. |

## What Better Means

Better means:

- Fewer ambiguous handoffs.
- Clear ownership between lead, reviewer, and executor.
- High-quality agents on important decisions.
- Cheaper safe agents on routine execution.
- Decisions and reviews visible in the active session.
- Portable workflows that do not depend on one vendor, one CLI, or one chat host.
