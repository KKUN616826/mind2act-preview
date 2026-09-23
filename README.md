# Mind2Act

**Mind2Act World** · Benchmark

**Mind2Act Harness** · 配套模型方案

**Evaluating Reasoning–Acting Coordination in Robotic Manipulation**

研究主线：计划如何适应物理约束，前一步的实际结果如何改变后一步。展示名称为 Mind2Act World，配套方法名为 Mind2Act Harness；仓库地址、兼容文件名与任务 ID 保持不变。

打开 `index.html` 即可浏览项目介绍、15 项任务与 37 段演示及预览、2 张场景图。请保持 media/、docs/ 和 data/ 的相对位置。

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

当前任务与素材同步自 MEMbench 文档 revision 830（2026-09-20）。CP05 已更新为三档完整流程视频，Easy 无琴盖，Medium/Hard 包含开合盖。CP03 仍为局部预览、CP04 为场景图；演示素材不构成模型性能验证。

## 配套模型网站

[Mind2Act Harness 模型架构](mindaccord/index.html)：Contract-Guided Coordination of Cognitive and Reactive Agents for Robotic Manipulation。构建与状态边界见 [模型 README](mindaccord/README.md)。
