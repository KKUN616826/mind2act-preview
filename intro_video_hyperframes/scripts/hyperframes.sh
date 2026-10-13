#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$PROJECT_DIR"
FFMPEG_DIR="${FFMPEG_DIR:-/opt/homebrew/bin}"
# 已安装的 HyperFrames 插件 CLI：优先取缓存中版本号最高的，回退到 marketplace 克隆
PLUGIN_CLI=""
for candidate in \
  $(ls -1d "${HOME}/.claude/plugins/cache/hyperframes/hyperframes"/*/skills/hyperframes/scripts/plugin-cli.mjs 2>/dev/null | sort -V -r) \
  "${HOME}/.claude/plugins/marketplaces/hyperframes/skills/hyperframes/scripts/plugin-cli.mjs"; do
  if [ -f "$candidate" ]; then
    PLUGIN_CLI="$candidate"
    break
  fi
done
if [ -x "$FFMPEG_DIR/ffmpeg" ]; then
  export PATH="$FFMPEG_DIR:$PATH"
  export HYPERFRAMES_FFMPEG_PATH="$FFMPEG_DIR/ffmpeg"
  export HYPERFRAMES_FFPROBE_PATH="$FFMPEG_DIR/ffprobe"
fi
if [ -n "$PLUGIN_CLI" ]; then
  exec node "$PLUGIN_CLI" "$@"
fi
# 回退版本与已安装插件保持一致
exec npx --yes hyperframes@0.8.149 "$@"
