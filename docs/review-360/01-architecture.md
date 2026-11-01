# Architecture & Packaging — shared-agent-skills



**Dimension:** 1/5 · **Grade:** A++ (9.6/10)



## Strengths



- **Source-of-truth pattern** — `skills/agent-routing-orchestrator/SKILL.md` is canonical; plugin copy is a distribution artifact.

- **Skill-only plugin bundle** — validation forbids runtime dirs (`agents/`, `commands/`, `hooks/`, etc.) under the plugin root.

- **Dual channel distribution** — standalone install scripts and Claude Code marketplace without duplicating skill semantics.

- **No vendored runtime** — package stays project-agnostic; external agents remain host-managed.

- **Extension path documented** — [docs/ADD-PLUGIN.md](../ADD-PLUGIN.md) describes multi-plugin growth without relaxing drift checks.



## Gaps to A++



None automatable. Single-plugin validation remains intentional until a second skill ships with validator updates.



## Key paths



- Source skill: `skills/agent-routing-orchestrator/SKILL.md`

- Plugin mirror: `plugins/agent-routing-orchestrator/skills/.../SKILL.md`

- Marketplace: `.claude-plugin/marketplace.json`

- Add-plugin guide: `docs/ADD-PLUGIN.md`



See [CODEGRAPH.md](../../CODEGRAPH.md) for topology diagrams.

