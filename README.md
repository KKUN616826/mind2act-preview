# Mind2Act

**Mind2Act World** · Benchmark

**Mind2Act Harness** · 配套模型方案

**Evaluating Reasoning–Acting Coordination in Robotic Manipulation**

研究主线：计划如何适应物理约束，前一步的实际结果如何改变后一步。展示名称为 Mind2Act World，配套方法名为 Mind2Act Harness；仓库地址、兼容文件名与任务 ID 保持不变。

打开 `index.html` 即可浏览项目介绍、15 项任务与 39 段演示及预览。请保持 media/、docs/ 和 data/ 的相对位置。

本地预览运行 `python3 scripts/preview.py`，访问 http://127.0.0.1:8765/。该服务支持视频 byte-range 请求，进度条无需等待整段视频下载完成即可跳转。

- docs/PhysCo_Cases.md：完整任务说明。
- docs/PhysCo_Technical_Report_v0.1.pdf：研究框架与评测设计。
- docs/PhysCo_Media.md：全部演示素材索引。
- data/showcase-cases.json：展示用任务数据，媒体路径相对网站根目录。

本展示包含任务定义与演示，不包含模型评测成绩。暂定参数和待补素材在具体任务中标注。

## 修改与构建

- 修改任务定义、媒体路径、难度和证据说明：`data/showcase-cases.json`。
- 修改核心观点与任务设计介绍：`scripts/research_intro.html`。
- 修改介绍样式：`scripts/research.css`；目录与交互：`scripts/showcase.html`。
- 修改完整研究介绍：`docs/PhysCo_Showcase.md`。
- 修改排行榜候选：`data/leaderboard.json`；表格与交互：`scripts/leaderboard.py`、`scripts/leaderboard.html`、`scripts/leaderboard.js`。当前只接受待评测占位，不能以零值代替缺失成绩；发布实测结果前须完善协议与校验，详见 `docs/Leaderboard.md`。
- 新媒体放在 `media/videos/` 或 `media/images/`，视频封面放在 `media/posters/`。

运行 `python3 scripts/build.py` 重新生成 HTML、逐任务文档及媒体索引，再用 `python3 scripts/validate.py` 检查资源一致性。不要只改生成后的 HTML，否则下次构建会覆盖。

当前任务与素材同步自 MEMbench 文档 revision 903（2026-09-25）。CP03 为动态槽架装盘，CP04 为双臂配料与温控烹饪，CP05 更新为揭防尘布与 Hard 音量调节流程。CP03 是使用仿真状态的专家运控；CP04 仅有 Easy 预览；所有演示均不代表模型测评成绩。

## 配套模型网站

[Mind2Act Harness 模型架构](mindaccord/index.html)：Contract-Guided Coordination of Cognitive and Reactive Agents for Robotic Manipulation。构建与状态边界见 [模型 README](mindaccord/README.md)。


## Current website previews

- Dark hero (current homepage): [index.html](index.html)
- Ivory hero: [hero-ivory-preview.html](hero-ivory-preview.html)
- Dark hero comparison: [hero-dark-preview.html](hero-dark-preview.html)

Both versions use the updated research introduction. Scores remain unpublished placeholders.

## CP05 首屏：记忆、动作与确认

当前首页使用同一次 CP05 高清仿真录制的截图、工具位姿与触键日志。12 次示范各有独立截图；K01–K29 表示从左到右的白键编号，不是音高。记忆卡片属于解释性叠加层，不是模型内部记忆记录。

- `scripts/hero-demo.html`、`scripts/hero-demo.css`、`scripts/hero-demo.js`：首屏结构、布局和播放器；`scripts/hero-demo-data.js` 提供纯时间状态计算。
- `data/hero-demo.json`：公开的事件表、时钟映射、录制来源摘要及左右棒尖高度；构建时内嵌到 HTML，无需 API 或运行时 JSON 请求。
- `media/images/hero-memory/`：12 张真实亮键截图，重复键占独立序列位置。
- `scripts/showcase.html` 与 `scripts/research_intro.html` 已同步当前首页；修改源模板后运行构建，不直接维护生成的 `index.html`。

高度使用同次运行记录的实际工具位姿计算出的棒尖世界坐标 Z，单位 cm。工具位姿记录为 30 Hz，触键时钟为 120 Hz，释放依据 12 Hz 键深日志中触发后首次小于 2 mm 的采样。事件点的高度在线性插值后的曲线上定位；确认时间始终取真实触键事件，不取曲线最低点。所有原始高度采样均保留，未用目标位置替代实测位置。

首页视频的 0–8 秒对应源视频 36.5–60.5 秒（3×），8–19.233333 秒对应 60.5–105.433332 秒（4×）。播放器默认 0.75×，所以观众看到的有效倍速分别为 2.25× 和 3×，单轮约 26 秒。只在 12 次有效触键及释放后显示 `Sequence complete`，不宣称整项任务或专家轨迹验收完成。

重新导出需要原始录制目录及 ffmpeg；普通网页构建不需要访问原始日志。导出依赖可装入独立虚拟环境：

```sh
python3 -m venv /tmp/mind2act-export
/tmp/mind2act-export/bin/pip install -r scripts/hero-export-requirements.txt
/tmp/mind2act-export/bin/python scripts/export_hero_demo.py --run /path/to/CP05-hard-hd-replay-20261009
python3 scripts/build.py
python3 scripts/validate.py
node --test scripts/test_hero_demo.cjs
```

导出器只读取原始运行，使用 `trajectory.json`、`control_trace.json`、`integrated_result.json`、`collection/control.npz` 和原生 RGB 时钟核对视频时间，并记录源文件 SHA-256。可加 `--output /tmp/hero-export-check` 导出到独立目录核对复现结果。

浏览器回归使用独立安装的 Playwright，不作为网站依赖。启动预览后运行 `node scripts/test_hero_browser.cjs`；可通过 `NODE_PATH` 指定 QA 依赖目录、`CHROMIUM_EXECUTABLE` 指定浏览器、`HERO_PREVIEW_URL` 指定地址、`HERO_SCREENSHOTS` 指定截图目录。测试覆盖四种屏宽、72 个事件边界、键盘操作、循环、逐帧同步、暂停恢复、减少动态效果与媒体错误回退。
