# Proposal v2 方法图

三个图说明方法分工与信息访问，不是实测轨迹。Case7 外部原型已接通部分接口；通用覆盖、按需调度和成本收益仍待验证。

1. `figures/architecture.svg`：Cognitive 提供事实与短期意图，harness 编码状态和绑定候选，Jev 选择动作、信息获取或升级，Runtime 与视觉工具完成执行。
2. `figures/packet-memory.svg`：当前认知、最近四次工具交互、按需读取的动作记忆与可见证据进入 DecisionPacket。Jev 主动选择保存／读／删，程序固定编码，容量为 32 条／32 KiB。
3. `figures/routing.svg`：等待事件、选择工具、补观察或升级的路径。语义选择由 Agent 作出；现有巡检、放置后和补计划触发另行标注，不将图示解读成已学到的最优路由。

图源为 `figures/specs/*.json`，使用 FigureSpec renderer 验证并生成 SVG；PDF 与 PNG 检查图通过本地 Chromium 渲染 SVG。修改图源后重新生成，不手改产物。

图风格参考 RoboICL-GPT6-Astra 的模块化说明，结构和文字独立编写。旧 `media/` 图保留为历史材料，不由当前页面使用。
