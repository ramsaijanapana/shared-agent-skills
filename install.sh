#!/usr/bin/env sh
set -eu

TARGET="${1:-both}"
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SKILLS_ROOT="$ROOT/skills"
SKILLS="agent-routing-orchestrator"
LEGACY_SKILLS="cost-aware-delegation cross-agent-project-lead"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
AGENTS_HOME="${AGENTS_HOME:-$HOME/.agents}"

install_to() {
  dest="$1"
  mkdir -p "$dest"
  for skill in $LEGACY_SKILLS; do
    if [ -e "$dest/$skill" ]; then
      rm -rf "$dest/$skill"
      printf 'Removed legacy %s -> %s\n' "$skill" "$dest"
    fi
  done
  for skill in $SKILLS; do
    rm -rf "$dest/$skill"
    cp -R "$SKILLS_ROOT/$skill" "$dest/"
    printf 'Installed %s -> %s\n' "$skill" "$dest"
  done
}

case "$TARGET" in
  codex)
    install_to "$CODEX_HOME/skills"
    ;;
  claude)
    install_to "$CLAUDE_HOME/skills"
    ;;
  agents)
    install_to "$AGENTS_HOME/skills"
    ;;
  both)
    install_to "$CODEX_HOME/skills"
    install_to "$CLAUDE_HOME/skills"
    ;;
  all)
    install_to "$CODEX_HOME/skills"
    install_to "$CLAUDE_HOME/skills"
    install_to "$AGENTS_HOME/skills"
    ;;
  *)
    echo "Usage: ./install.sh [codex|claude|agents|both|all]" >&2
    exit 2
    ;;
esac
