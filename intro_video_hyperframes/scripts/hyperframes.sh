#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$PROJECT_DIR"
NODE_DIR="${HOME}/.nvm/versions/node/v22.23.3/bin"
FFMPEG_DIR="${HOME}/miniconda3/envs/xvla-stable/bin"
PLUGIN_CLI="${HOME}/.claude/plugins/cache/hyperframes/hyperframes/0.8.143/skills/hyperframes/scripts/plugin-cli.mjs"
BROWSER_PATH="${HOME}/.cache/puppeteer/chrome-headless-shell/linux-148.0.7778.97/chrome-headless-shell-linux64/chrome-headless-shell"
if [ -x "$NODE_DIR/node" ]; then export PATH="$NODE_DIR:$PATH"; fi
if [ -x "$FFMPEG_DIR/ffmpeg" ]; then
  export PATH="$FFMPEG_DIR:$PATH"
  export HYPERFRAMES_FFMPEG_PATH="$FFMPEG_DIR/ffmpeg"
  export HYPERFRAMES_FFPROBE_PATH="$FFMPEG_DIR/ffprobe"
fi
if [ -x "$BROWSER_PATH" ]; then export HYPERFRAMES_BROWSER_PATH="${HYPERFRAMES_BROWSER_PATH:-$BROWSER_PATH}"; fi
if [ -f "$PLUGIN_CLI" ]; then
  exec node "$PLUGIN_CLI" "$@"
fi
exec npx --yes hyperframes@0.8.143 "$@"
