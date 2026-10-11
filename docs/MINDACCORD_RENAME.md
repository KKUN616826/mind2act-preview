# MindAccord 名称与模型页

配套方法名称正式采用 **MindAccord**。

**Contract-Guided Coordination of Cognitive and Reactive Agents for Robotic Manipulation**

MindActWorld 为 benchmark 名称，MindAccord 为配套方法名称。网站首屏、导航、模型简介、结构数据和架构说明采用新名称；原始实现来源仍为 EvoMemHarness，固定源码提交保持不变。

## 模型网站

独立模型页位于 `mindaccord/index.html`，从主站模型介绍可进入；返回 benchmark 使用相对路径。模型子目录包含自有样式、数据、文档、脚本和两张图，无须依赖研究目录即可构建。

架构图重绘为 `mindaccord/media/mindaccord-architecture.svg`，显示新标题并保留当前原生控制器与待接入 VLA 的实线/虚线区别。经验生命周期图保持原样。旧版 AI 生成架构图保留在本地研究目录中，不作为当前网站展示素材。

## 状态与验证

原生 Cognitive–Reactive 与固定控制器路径、版本化授权、取消确认和单一执行入口按既有源码快照说明。VLA checkpoint 接入与原生经验候选晋升仍待完成，未新增模型成绩。

模型页检查覆盖八个模块、三种执行状态、两张图的放大与关闭、源码跳转、benchmark 往返链接，以及 1440/768/390/320px 下的布局。主站任务与视频回归检查通过。逐任务 JSON 和排行榜占位数据保持不变。
