# Mind2Act 15任务三档采集演示

2026-10-09 导出。每任务每难度一条，共45条，全部来自当前接纳的训练选择。
头相机640×480、30fps、1倍原速，保留全部原生帧和完整流程。

[打开离线观看页](index.html)

|任务|Easy|Medium|Hard|
|---|---|---|---|
|E|[episode_0010 · 60.5s](E/easy.mp4)|[episode_0010 · 120.0s](E/medium.mp4)|[episode_0010 · 170.2s](E/hard.mp4)|
|P|[episode_0031 · 46.4s](P/easy.mp4)|[episode_0047 · 57.3s](P/medium.mp4)|[episode_0030 · 76.3s](P/hard.mp4)|
|S|[episode_0022 · 64.8s](S/easy.mp4)|[episode_0047 · 72.0s](S/medium.mp4)|[episode_0048 · 72.4s](S/hard.mp4)|
|F|[episode_0003 · 16.9s](F/easy.mp4)|[episode_0030 · 27.6s](F/medium.mp4)|[episode_0022 · 33.1s](F/hard.mp4)|
|M|[episode_0008 · 74.5s](M/easy.mp4)|[episode_0037 · 90.0s](M/medium.mp4)|[episode_0049 · 99.6s](M/hard.mp4)|
|FR1|[episode_0011 · 23.0s](FR1/easy.mp4)|[episode_0010 · 27.8s](FR1/medium.mp4)|[episode_0039 · 36.1s](FR1/hard.mp4)|
|FR2|[episode_0031 · 15.3s](FR2/easy.mp4)|[episode_0046 · 16.9s](FR2/medium.mp4)|[episode_0009 · 14.6s](FR2/hard.mp4)|
|PR1|[episode_0022 · 12.0s](PR1/easy.mp4)|[episode_0023 · 10.4s](PR1/medium.mp4)|[episode_0012 · 12.3s](PR1/hard.mp4)|
|PR2|[episode_0043 · 20.5s](PR2/easy.mp4)|[episode_0012 · 20.4s](PR2/medium.mp4)|[episode_0005 · 19.4s](PR2/hard.mp4)|
|PR3|[episode_0015 · 24.5s](PR3/easy.mp4)|[episode_0017 · 24.7s](PR3/medium.mp4)|[episode_0034 · 24.6s](PR3/hard.mp4)|
|CP01|[episode_0050 · 57.4s](CP01/easy.mp4)|[episode_0015 · 107.8s](CP01/medium.mp4)|[episode_0004 · 139.9s](CP01/hard.mp4)|
|CP02|[episode_0040 · 55.4s](CP02/easy.mp4)|[episode_0001 · 92.3s](CP02/medium.mp4)|[episode_0030 · 100.4s](CP02/hard.mp4)|
|CP03|[episode_0024 · 84.6s](CP03/easy.mp4)|[episode_0014 · 154.1s](CP03/medium.mp4)|[episode_0028 · 188.0s](CP03/hard.mp4)|
|CP04|[episode_0043 · 111.6s](CP04/easy.mp4)|[episode_0042 · 123.8s](CP04/medium.mp4)|[episode_0039 · 162.3s](CP04/hard.mp4)|
|CP05|[episode_0010 · 62.1s](CP05/easy.mp4)|[episode_0010 · 72.7s](CP05/medium.mp4)|[episode_0002 · 120.0s](CP05/hard.mp4)|

E 三条直接从当前30Hz训练HDF5导出；CP05复用本对话刚导出的三条已接纳重放演示。
其余39条复用已有视频，已核对与当前训练选择的原始来源路径、episode ID、帧数和帧率一致。
全部视频下载后SHA256一致，并逐条检查完整帧数、帧率、分辨率和时长。未重新执行任务或模型。
这些是训练采集演示，不是本轮模型评测结果；技术导出检查不等于重新人工审查全部任务动作。

总视频大小：248.3 MiB；总时长：50.3分钟。
详细来源与冻结训练/导出快照见 [manifest.json](manifest.json)。
