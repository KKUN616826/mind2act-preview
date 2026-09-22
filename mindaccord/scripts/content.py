"""Reviewed architecture content, pinned to the supplied evomemharness branch."""

COMMIT = "6d3c53eab6adcdfc7b7c4fdda7c9dba5d4fcce41"
REPO = "https://github.com/MuQY1818/mem-planner-harness"
PREFIX = "cognitive-reactive-harness/"
SRC = PREFIX + "src/cr_harness/"

SOURCES = [
    ("protocol", "当前原生协议 · coordination-v3", PREFIX + "docs/runtime-tools-notes-v3.md", 1, "职责、RGB 推断感知、notes、动作批次与效果判断的当前定义。"),
    ("roles", "Cognitive / Reactive 结构化接口", SRC + "robodojo/rgb_protocol.py", 25, "RGBPlan、RGBAction、两角色工具请求与提示词。"),
    ("runner", "双会话异步运行", SRC + "robodojo/runner.py", 294, "观测、认知、反应与环境事件的独立循环。"),
    ("effects", "效果判断的证据与版本", SRC + "robodojo/coordination.py", 392, "当前 RGB 路径记录 agent_judgment，verified=False。"),
    ("notes", "局内私有 / 共享笔记", SRC + "notes.py", 8, "按 Episode 隔离；主动读写、版本冲突检查、容量约束。"),
    ("perception", "按需 RGB 感知", SRC + "robodojo/agent_tools.py", 153, "Depth Pro / SAM3 与同帧测量；预测相机空间结果。"),
    ("boundary", "观察和经验输入边界", SRC + "robodojo/observation_policy.py", 1, "rgb_proprio_inferred_tools_v2；禁止环境深度与标定；当前原生路径要求空经验快照。"),
    ("vla", "VLA 动作块接口", SRC + "vla.py", 11, "VLAInput → ActionChunk；动作空间、维度、时长和取消检查。"),
    ("campaign", "原生运行配置", SRC + "robodojo/campaign.py", 85, "25 Hz 动作行、持续物理时钟、vla_mode=unavailable。"),
    ("memory", "跨局双经验库", SRC + "memory.py", 11, "每三条开发 Record 分组；候选验证、关联卡原子发布与版本快照。"),
    ("critic", "原生 Critic 的晋升边界", SRC + "robodojo/critic.py", 11, "原生候选缺少 paired replay / regression validator，当前 admitted=False。"),
    ("legacy", "EvoMemHarness · Planner–Runner–RSI", "docs/EVOMEMHARNESS.md", 1, "program-v1 的逐调用账本、经验目录、Critic 与独立 DEV 验证。"),
    ("xvla", "仓库已有 RMBench X-VLA 适配", "robots/rmbench/xvla_backend.py", 101, "三路 RGB、本体状态及 20D 动作转换；不同于双 Agent 原生路径的接入状态。"),
    ("motor", "独立 Motor RSI 试点", "robots/rmbench/motor/README.md", 1, "Swap T 的受限程序修复试点，不能当作已整合的 VLA 或双层自进化结果。"),
]

MODULES = [
    dict(id="cognitive", name="Cognitive Agent", label="任务层", state="已实现 · 原生协议", inputs="任务文本、当前 RGB / 本体状态、执行事件、局内笔记", outputs="任务依赖图、当前子目标、版本化授权与计划修订", body="维护长程目标和有效进度，决定当前应完成哪个子目标。可以在 Reactive 执行期间推理后续计划；普通笔记和无关未来计划更新不应撤销正在执行的授权。", boundary="不直接提交物理动作；完成声明属于模型判断。", cases=["E","P","S","F","M","CP01","CP04"], sources=["roles","runner"]),
    dict(id="reactive", name="Reactive Agent", label="动作决策层", state="已实现 · 原生协议", inputs="当前授权、RGB / 本体状态、动作回执、局内笔记", outputs="原子动作、最多八步的有限批次、检查点、恢复或升级请求", body="在 Cognitive 的授权下选择工具与参数，依据新观测判断动作效果。当前它仍是模型会话，不等于高频控制器，也不等于 VLA；高频关节跟踪交给执行后端。", boundary="不能自行更换授权目标；批次完成只表示动作执行结束。", cases=["FR1","FR2","PR1","PR2","PR3","CP02","CP05"], sources=["roles","protocol"]),
    dict(id="contract", name="Subgoal Contract", label="层间接口", state="已实现 · 原生协议", inputs="Cognitive 的当前子目标、工具许可、预算与任务依赖", outputs="Reactive 可使用的稳定授权及其版本", body="将任务意图绑定到有限执行范围。动作携带子目标与授权版本；撤销授权时先停止派发并等待取消确认。过期结果不能恢复旧授权。", boundary="合同管理执行权限，不为任务生成坐标或预设成功答案。", cases=["P","CP01","CP02","CP03","CP04","CP05"], sources=["roles","runner","protocol"]),
    dict(id="runtime", name="Execution Runtime", label="唯一动作入口", state="已实现 · 原生协议", inputs="动作请求、当前授权、批次游标、来源帧与预算", outputs="控制指令、动作回执、拒绝 / 取消事件与执行记录", body="管理单一动作归属、请求去重、来源时效、逐步派发和取消确认。Agent 显式设定检查点；失败、预算耗尽和授权失效也会停止下一步。", boundary="不自动试抬、重抓或计算任务完成；工作空间范围不是通用避碰证明。", cases=["FR1","FR2","PR1","PR2","PR3","CP01","CP02","CP03","CP04","CP05"], sources=["protocol","runner"]),
    dict(id="tools", name="Notes + Perceive", label="双角色共享工具", state="已实现 · 按需调用", inputs="当前 RGB、显式像素 / 框提示，私有或共享笔记的键与版本", outputs="分割 / 预测深度 / 相机空间测量，主动读取的笔记正文", body="两角色都可主动调用感知与笔记。感知只处理实际提供的 RGB，Depth Pro 的深度属于预测；notes 保存局内自由文本，另一角色须显式读取共享正文。", boundary="无环境 GT 深度或相机标定；笔记不等于跨 Episode 经验。", cases=["E","P","S","F","M","PR1","PR2","CP03"], sources=["notes","perception","boundary"]),
    dict(id="controller", name="Native Controller", label="当前执行后端", state="已实现 · 原生接口", inputs="observe / move_to / set_gripper / wait_steps", outputs="IK / 轨迹转换后的实际关节动作及本体回执", body="当前原生接口使用确定性运控。25 Hz 指执行动作行，底层物理子步与 Agent 推理频率另行记录；模型推理时物理继续推进，wall time scale 仍需披露。", boundary="工具执行成功不能单独证明抓住、放稳或任务达标。", cases=["FR1","FR2","PR1","PR2","PR3","CP01","CP02","CP03","CP04","CP05"], sources=["campaign","protocol"]),
    dict(id="vla", name="Execution VLA", label="学习式执行扩展", state="已有接口 · 双 Agent 接入待完成", inputs="局部指令、相机图像、本体状态、动作长度与时长预算", outputs="带 policy_id、动作空间和控制周期的 ActionChunk", body="目标架构中，Reactive 可将适合学习式执行的局部动作交给 VLA。仓库已定义 checkpoint 无关接口，并有独立 RMBench / RoboTwin VLA 后端；当前双 Agent 原生 campaign 仍设置 unavailable。", boundary="尚不能将这条双 Agent 原生路径称为已运行的 checkpoint VLA 系统。", cases=["FR1","FR2","PR1","PR2","PR3","CP02","CP05"], sources=["vla","campaign","xvla"]),
    dict(id="experience", name="Experience Engine", label="离线跨局更新", state="已有机制 · 原生晋升待验证", inputs="已结束的开发 EpisodeRecord、调用事件与最终结果", outputs="认知 / 运动候选卡、验证记录、冻结经验版本", body="三条新开发记录触发离线 Critic；候选区分认知、运动与系统原因。通用存储支持验证后原子发布。原生 Critic 当前保留候选，新的 RGB 原生运行只接受空经验快照。", boundary="轻量环境验证不替代原生回放；SEM-Memory 效果后验和自动回滚仍属后续设计。", cases=["F","PR1","PR2","CP01","CP03","CP04"], sources=["memory","critic","boundary","motor"]),
]

# These are architecture-to-task evaluation mappings, not measured model results.
MAPPING = {
    "E": ("维护跨批物品身份，检索本批重复件。", "托盘停稳后抓取并放入正确提交盘。", "视觉判断实际提交后更新批次进度；独立评分核实身份与落位。", "cognitive tools contract runtime", "历史身份与新观测对应错误；调用成功后误记已提交。"),
    "P": ("累计新订单，分别保存各容器需求与已完成量。", "选择食材、投放、观察实际结果。", "用投放证据更新进度；新订单改变需求，不重置已完成记录。", "cognitive tools contract reactive", "新增需求覆盖旧需求；未成功投放却扣减剩余量。"),
    "S": ("保存颜色布局与旋转后的空间对应。", "按新布局逐件复位并保持稳定。", "依据当前视图重新绑定位置，避免直接重用旧坐标。", "cognitive tools reactive runtime", "记住颜色却混淆旋转后的格位；物理落位偏差未纠正。"),
    "F": ("维护按钮到滑台变化的假设，并据反馈修订。", "按压与释放，观察滑台实际位移。", "每次试验的观测变化更新映射；未知关系继续保留不确定性。", "cognitive tools reactive experience", "把无效按压当作一次映射试验；重复无信息探测。"),
    "M": ("追踪罩内目标，记住有序路线及重复到访。", "揭罩取件，按路线逐站放置。", "只有实际释放并放稳后才推进路线索引。", "cognitive tools contract reactive", "无关交换污染路线；跳过重复工位；索引提前推进。"),
    "FR1": ("保存批次目标和剩余件数。", "在移动窗口内完成取件、运输与入盘。", "观察到动作生效的端到端时延与实际入盘数共同衡量表现。", "reactive runtime controller vla", "模型等待造成窗口错失；以控制器 Hz 代替有效吞吐。"),
    "FR2": ("维护提示顺序及每次独立响应。", "时限内按下、触发后释放，再响应下一次。", "同一按钮连续亮起也需要新的按压—释放周期。", "reactive runtime controller vla", "未释放就计入下一次；动作回执与按钮触发混淆。"),
    "PR1": ("绑定目标阻值与读数容差。", "移动操作柄，双向微调，松手撤离。", "松手后仍在误差范围并保持一秒，才满足 Bench 完成条件。", "tools reactive controller vla", "夹持时达标、松手后回弹；读数误差与控制误差混淆。"),
    "PR2": ("理解目标读数与旋钮调节方向。", "抓握、旋转、重抓或微调，再验证读数。", "用实际读数确认效果，动作角度只是执行量。", "tools reactive controller vla", "转了指定角度却未达目标；接触滑动导致有效转角不足。"),
    "PR3": ("维护目标线条与段落进度。", "持笔连续接触、沿线运动并控制起落。", "以实际笔迹与接触轨迹评测，不以命令轨迹替代。", "reactive runtime controller vla", "跟踪路径正确但笔尖未接触；断线与越界未进入反馈。"),
    "CP01": ("记住参考款式，维护仍待收取的目标集合。", "跟踪移动目标、抓取并稳定放入收集区。", "抓空保留待收目标；疑似入盘需观察，允许预算内处理回流。", "cognitive contract reactive runtime experience", "把一次抓取调用计为收集完成，造成漏件或重复收取。"),
    "CP02": ("维护装饰顺序、目标位置与已完成部分。", "在旋转目标上抓取、接近和准确放置。", "放置后的实际效果影响下一次目标选择与时机。", "cognitive contract reactive runtime vla", "计划使用过期位姿；放置失败后仍推进下一装饰。"),
    "CP03": ("维护阶段配方、累计剂量和搅拌依赖。", "计量、倾倒、观察读数并执行搅拌。", "依据实际液量确认阶段；配方保持显示，重点是进度与动作耦合。", "cognitive tools contract reactive experience", "把指令剂量当成实际剂量；过量后盲目重试。"),
    "CP04": ("组织装箱顺序、占用关系和布局调整。", "搬放不同物体，处理实际占用与放置偏差。", "当前物体落位改变后续可用空间，需要更新剩余计划。", "cognitive contract reactive runtime experience", "预设布局与真实占用脱节；恢复破坏此前稳定结果。"),
    "CP05": ("记住乐句，维护音符索引和双臂分工。", "准确触键、完整释放并衔接下一音符。", "以真实触发与释放确认节奏和进度；演示与执行周期为 2 秒/次。", "cognitive contract reactive runtime vla", "错误触键仍推进索引；双击、漏击和双臂交接延迟。"),
}

WALKTHROUGH = {
    "miss": dict(title="抓空：目标仍待收取", cognitive="保留当前款式的未完成状态；根据剩余窗口决定继续尝试或等待回流。", reactive="检查新 RGB 与夹爪状态，重新接近目标，必要时向 Cognitive 升级。", runtime="记录已执行动作与失败判断；新请求继续检查授权、时效和剩余预算。", evidence="抓取命令的成功回执不能证明持物。此处是 CP01 的架构行为示意，不是模型 rollout。"),
    "unknown": dict(title="效果不确定：先补充观察", cognitive="保持完成状态未确认，避免将后继计划建立在不可靠的持物假设上。", reactive="主动 observe；将基于新帧的判断及证据引用反馈给 Cognitive。", runtime="核对引用来源、已执行动作和版本；保存 agent_judgment，不判定图像中的物理真值。", evidence="当前实现中，Agent 判断与环境评分相互独立；unknown 需要后续观测或任务层决定。"),
    "deposited": dict(title="观察判断入盘：更新待收集合", cognitive="依据带证据的入盘判断关闭当前待收目标，继续处理其他参考款式。", reactive="释放并撤离后观察落位，将前后帧和动作 ID 绑定到效果报告。", runtime="保存判断作者、解释与版本；在线状态可以推进，最终正确性仍由环境评分核验。", evidence="Bench 判据要求实际稳定入盘。在线的 achieved 是由 Agent 证据支持的状态，并非独立认证。"),
}

MODEL_NAME = "MindAccord"
MODEL_SUBTITLE = "Contract-Guided Coordination of Cognitive and Reactive Agents for Robotic Manipulation"
