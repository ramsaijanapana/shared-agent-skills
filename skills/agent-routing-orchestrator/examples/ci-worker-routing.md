Use agent-routing-orchestrator for CI-hosted validation work.

Host: GitHub Actions / CI worker.
Lead: CI orchestrator agent or human on-call.
Execution: CI job steps and artifact-producing workers only.
Review: required for schema, security, or release-gating changes.
Cost mode: budget for routine checks, quality-first for release gates.
Autonomy: autonomous within the CI job; escalate on flaky tests or missing secrets.
Session log: job summary with routing choice, commands run, and verification output.
Verification: validate scripts, tests, and plugin sync checks must pass before green.

Goal: Run package validation and report actionable failures.

Do not touch: secrets, production deploy hooks, or out-of-scope repositories.
