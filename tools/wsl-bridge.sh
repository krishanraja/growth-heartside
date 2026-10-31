#!/usr/bin/env bash
# Start a Remote Control bridge from Krish's WSL Ubuntu so the cloud Claude session can run
# Codex (ChatGPT images), Buffer uploads and the engine on this machine, and report back in
# the same chat. Run it from anywhere inside WSL:
#
#   bash ~/growth-heartside/tools/wsl-bridge.sh            # uses ~/growth-heartside
#   bash tools/wsl-bridge.sh /path/to/growth-heartside     # or name the folder
#
# It never posts, sends or spends: it only checks the machine and opens the bridge. Every
# post still needs Krish's yes in the chat (AGENTS.md, rule 1 and "Autonomy").
set -euo pipefail

REPO="${1:-$HOME/growth-heartside}"
BRANCH="${HEARTSIDE_BRANCH:-ccr-21e182e5-psq1vi}"
ok() { printf '  ok   %s\n' "$1"; }
bad() { printf '  FIX  %s\n' "$1"; exit 1; }

echo "Heartside bridge: checking this machine"
[ "$(uname -s)" = "Linux" ] || bad "run this inside WSL Ubuntu, not Windows PowerShell"
[ "$REPO" != "$HOME" ] || bad "Remote Control cannot use the home folder itself; use ~/growth-heartside"
case "$REPO" in "$HOME"/.*) bad "Remote Control cannot use a hidden folder under home";; esac

if [ ! -d "$REPO/.git" ]; then
  echo "  cloning growth-heartside into $REPO"
  git clone https://github.com/krishanraja/growth-heartside.git "$REPO"
fi
cd "$REPO"
git fetch --quiet origin "$BRANCH" && git checkout --quiet "$BRANCH" && git pull --quiet --ff-only origin "$BRANCH"
ok "repo on $BRANCH at $(git rev-parse --short HEAD)"

command -v claude >/dev/null || bad "Claude Code is not installed: npm install -g @anthropic-ai/claude-code"
ok "claude $(claude --version 2>/dev/null | head -1)"
command -v codex >/dev/null || bad "Codex CLI is not installed: npm install -g @openai/codex, then run 'codex login' once"
ok "codex $(codex --version 2>/dev/null | head -1)"
command -v python3 >/dev/null || bad "python3 is missing: sudo apt install -y python3 python3-pip"
command -v ffmpeg >/dev/null || bad "ffmpeg is missing: sudo apt install -y ffmpeg"
ok "python3 and ffmpeg present"
mkdir -p local/production local/media

cat <<'NOTE'

Opening the bridge. Leave this terminal open while the cloud session works.
In the Claude chat, say "bridge is up" and the session will ask to use this folder;
approve that request when it appears. Close this terminal to disconnect.
NOTE
exec claude remote-control
