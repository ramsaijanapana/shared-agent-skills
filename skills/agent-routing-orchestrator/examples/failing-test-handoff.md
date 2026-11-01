Use agent-routing-orchestrator to hand this failing test investigation to the cheapest safe executor.

Host: Codex.
Lead: Codex.
Execution: standard worker or subagent for bounded file-owned fixes.
Cost mode: balanced.
Autonomy: ask before broad rewrites or dependency changes.
Session log: routing choice, task packet, completion packet, verification.
Verification: reproduce failure, fix root cause, rerun failing test and nearby suite.

Goal: Fix the failing test in <path or test name> without expanding scope.

Do not touch: unrelated modules, public API shape, or CI configuration.
