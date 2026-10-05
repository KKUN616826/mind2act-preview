# Mind2Act

**Mind2Act World** · Benchmark

**Mind2Act Harness** · 配套模型方案

**Evaluating Reasoning–Acting Coordination in Robotic Manipulation**

研究主线：计划如何适应物理约束，前一步的实际结果如何改变后一步。展示名称为 Mind2Act World，配套方法名为 Mind2Act Harness；仓库地址、兼容文件名与任务 ID 保持不变。

打开 `index.html` 即可浏览项目介绍、15 项任务与 39 段演示及预览。请保持 media/、docs/ 和 data/ 的相对位置。

如果浏览器限制本地视频，可在解压目录运行 `python3 -m http.server 8765`，访问 http://127.0.0.1:8765/。

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
