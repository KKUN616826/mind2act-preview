# Mind2Act Harness · Astra–Jev Proposal v2

**Contract-Guided Coordination of Cognitive and Reactive Agents for Robotic Manipulation**

[模型网站](index.html) · [Proposal v2](docs/MindAccord_Proposal_v2.md) · [Mind2Act World](../index.html)

Mind2Act Harness 面向目标可在一段操作中复用、执行反馈会改变后续决策的多步机器人任务，研究如何在局部行动与视觉重规划之间分配推理开销。GPT-6 Astra 形成可见事实与短期意图；Jev 根据新回执选择工具、补观察、读取信息或请求重规划；视觉执行工具负责动作期间的连续控制。RSI 设计为在局间分析执行记录，提出并验证经验与策略改进，使后续任务使用经过检验的新版本。

核心 insight 是：**任务目标与执行证据可能以不同速度变化。已有理解足以支持行动时复用它；新证据表明局部信息不足或计划需要修订时，再获取相应层级的认知支持。** 局内反馈决定下一步行动，跨局反馈改进协作方式；目标是在保持任务完成能力的条件下，改善总成本与完成时间。

外部 Case7 清框原型已完成端到端运行，现有结果来自同一开发场景，尚未证明优于单 Agent、节省 Cognitive 调用或降低总成本。当前实现仍有巡检、放置后更新等固定触发，完全按需的认知更新属于待验证方案。本目录维护方法提案、开发证据与展示页面；Mind2Act World 正式评测结果仍为空，合成接口示例不代表运行轨迹。**RSI 是下一阶段立即推进的实现重点**：开发记录 → Critic → 改进候选 → 独立验证 → 版本发布／回滚。首版接入认知与工具使用双经验库，再扩展受限的交接和调度补丁；当前尚未接入 Jev 闭环，也不涉及模型权重训练。

## 维护入口

- `scripts/proposal.html` / `scripts/proposal.css`：模型网页源文件。
- `scripts/content.py` / `scripts/presentation.py`：模块、调用路径、来源和方法图说明。
- `docs/MindAccord_Proposal_v2.md`：研究问题、方法接口、开发证据与评测设计。
- `docs/Proposal_v2_Changes.md`：提案更新记录。
- `data/examples/`：明确标注为合成示例的交接 JSON。
- `data/research/case7_development_evidence_20260924.json`：历史开发计数、离线评分摘要、来源路径及 SHA-256；不包含私有物体记录。
- `figures/specs/`：FigureSpec 图源；`figures/`：SVG 和 PDF。

运行 `python3 scripts/build.py` 生成网站、公开结构数据和兼容路径的架构 Markdown；运行 `python3 scripts/verify.py --static-only` 检查链接、状态、示例与图源一致性。两命令都不调用模型或机器人。

图源使用项目 figure-spec 技能的 `figure_renderer.py validate` / `render` 生成；不可把直接手改 SVG 当作可复现图源。

原模型网页由 Git 历史保留，本地研究目录另有 `archive/pre-astrajev-v2/`。旧 `media/` 图和原模板保留为历史文件，不由当前构建使用。今后以此 Git 子目录维护公开页面。
