# Proposal v2 方法图

三个图均为目标设计，不代表已实现集成或实测结果。

1. `figures/architecture.svg`：Astra 下发子目标契约、调用 perception；harness 编译文本状态；Jev 选择候选，Runtime 执行，事件路由触发局部刷新或升级。
2. `figures/packet-memory.svg`：关键任务事实、近期事件、带证据摘要、有效场景与候选进入 DecisionPacket。
3. `figures/routing.svg`：继续、刷新、候选选择、升级与预算耗尽停止的示意分支。它是决策路径说明，不是完整实现状态机。

源文件为 `figures/specs/*.json`，由本地 FigureSpec renderer 验证并生成 SVG；对应 PDF 可用于汇报。没有复制参考网站的图像或性能数据。

图风格参考 RoboICL-GPT6-Astra 研究页的模块化方法说明；本图的结构和文字独立编写。旧 `media/` 架构与经验生命周期图保留为历史材料，不再出现在当前页面。
