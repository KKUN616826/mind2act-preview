"""Model-only execution states and compact Bench alignment."""
ALIGNMENT = [
    ("Task-Level Reasoning · 任务级推理", "Cognitive + Notes", "任务理解、状态维护与重规划", "检查目标、依赖和剩余需求是否正确。"),
    ("Constraint-Aware Execution · 约束感知执行", "Reactive + 执行后端", "精度、响应与持续接触", "记录实际物理误差、执行时延与有效交互频率。"),
    ("Reasoning–Acting Coordination · 推理—执行协同", "Contract + 执行反馈", "效果驱动的进度推进", "检查是否根据实际执行反馈修订后续决策。"),
    ("迁移（附加协议）", "Cognitive / Motor Experience", "冻结经验的跨局复用", "在独立实例上比较首次表现、恢复成本与负迁移。"),
]
STATES = {
    "ongoing": dict(label="执行进行中", title="当前执行继续，任务层可规划后续", cognitive="保持当前子目标的授权，利用已有反馈维护未来依赖。无关计划变更不打断当前动作。", reactive="等待动作回执，或在显式检查点接收新观测，再决定下一步。", runtime="独占动作入口，逐步派发并记录实际执行量；推理期间环境仍可继续推进。", evidence="动作已派发、正在执行与子目标已完成是不同状态。"),
    "unknown": dict(label="效果不确定", title="补充证据，再决定是否推进", cognitive="保留未确认状态，避免把后继子目标建立在未经确认的前提上。", reactive="主动观察，必要时调用感知或读取笔记，提交带来源的效果判断。", runtime="检查动作 ID、帧来源、授权和判断版本；记录 agent_judgment，不替模型判断图像中的物理真值。", evidence="在线 achieved 是由模型判断支持的状态；最终成功由独立环境评分器确认。"),
    "revoked": dict(label="授权改变", title="先停止旧执行，再接受新任务", cognitive="根据关键反馈修订当前子目标，发布新版本授权。", reactive="取消旧动作或批次；收到确认后，在新授权下重新决策。", runtime="停止后续派发，等待取消确认；拒绝迟到的旧版本请求，避免两个意图同时控制机器人。", evidence="计划更新不等于物理动作立即停止；取消确认属于层间交接协议。"),
}
FIGURES = [
    dict(id="architecture", path="media/mindaccord-architecture.svg", title="双层 Agent 与执行后端", description="认知授权流向 Reactive，Reactive 经 Runtime 派发动作；观察与回执返回双方。虚线为待接入的 VLA 路径。"),
    dict(id="experience", path="media/experience-lifecycle-v2.png", title="从执行记录到跨局经验", description="开发记录经 Critic 形成候选，验证通过后才能进入冻结快照。当前原生候选保留，晋升环节待验证。"),
]
