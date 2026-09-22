# MindAccord · Astra–Jev Proposal v2

**Contract-Guided Coordination of Cognitive and Reactive Agents for Robotic Manipulation**

[模型网站](index.html) · [Proposal v2](docs/MindAccord_Proposal_v2.md) · [MindActWorld](../index.html)

新版聚焦 GPT-6 Astra 的子目标拆解与感知调度、结构化交接、Jev 候选选择 harness、有界工作记忆与成本路由。当前为设计 proposal，不是已完成的 Astra–Jev 系统；未运行新模型调用或机器人实验。RSI 不在当前范围内。

## 维护入口

- `scripts/proposal.html` / `scripts/proposal.css`：新模型网页。
- `scripts/content.py` / `scripts/presentation.py`：模块、路由示意、来源和三张方法图。
- `docs/MindAccord_Proposal_v2.md`：完整 proposal。
- `data/examples/`：明确标注为合成示例的四类交接 JSON。
- `figures/specs/`：FigureSpec 图源；`figures/`：SVG 和 PDF。

运行 `python3 scripts/build.py` 生成网站、公开结构数据和兼容路径的架构 Markdown；运行 `python3 scripts/verify.py --static-only` 检查链接、状态、示例与图源一致性。两命令都不调用模型或机器人。

图源使用项目 figure-spec 技能的 `figure_renderer.py validate` / `render` 生成；不可把直接手改 SVG 当作可复现图源。PDF 是 SVG 的浏览器打印版本。

原模型网页由 Git 历史保留，本地研究目录另有 `archive/pre-astrajev-v2/`。旧 `media/` 图和原模板保留为历史文件，不由当前构建使用。今后以此 Git 子目录维护公开页面。
