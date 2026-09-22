# MindAccord

**Contract-Guided Coordination of Cognitive and Reactive Agents for Robotic Manipulation**

[模型网站](index.html) · [MindActWorld](../index.html) · [架构说明](docs/PhysCo_Model_Architecture.md)

基于 EvoMemHarness 固定提交的 Cognitive–Reactive 架构说明。当前原生路径使用固定控制器；双角色原生路径中的 VLA checkpoint 接入和跨局候选经验晋升仍待完成。没有新增模型成绩。

## 维护

`python3 scripts/build.py` 生成网站、模型 JSON、架构 Markdown 与素材 provenance。

`python3 scripts/verify.py --static-only` 检查名称、副标题、本地链接与模型数据。安装 Python Playwright 和 Chrome 后可运行完整验证。

名称与副标题由 `scripts/content.py` 中的 MODEL_NAME / MODEL_SUBTITLE 维护；`scripts/model.html` 为模板，`scripts/presentation.py` 为执行状态和能力映射。可编辑架构图为 `media/mindaccord-architecture.svg`。

研究目录是本次发布的来源；后续以当前 Git 仓库内文件维护公开模型页。文件名 PhysCo_Model_Architecture.md 保留以兼容旧链接。
