# Mind2Act 新版视频 · 空白 HyperFrames 工程

本目录只准备素材和空白工程，尚未开始新一版剪辑。原版工程保留在 `../mind2act-promo-codex-20261010-022331/`。

## 入口和目录

- `index.html`：1920×1080 空白画布，1 秒占位长度，无场景、文案、视频或音频轨道。开始创作时设置实际时长，并去掉根节点的 `data-no-timeline`。
- `assets/videos/`：45 条主 case 视频，15 个任务各有 Easy / Medium / Hard，按类别和任务整理。
- `assets/reference-videos/mind_p_order_case_16s_204025_1080p.mp4`：MIND / P 配餐的 16 秒布局与动效参考视频，1920×1080、30fps；不计入主素材 45 条。
- `assets/logos/Mind2Act-三个Logo-高清透明版/`：用户指定的三个原始透明 PNG，逐文件 SHA-256 校验一致。
- `assets/audio/The Midnight - The Equaliser (Not Alone).mp3`：原宣传片使用的完整 BGM 源文件，229.042 秒、44.1kHz、双声道；原样复制，未裁剪或调整音量，也未混入口播。
- `assets/lib/gsap.min.js`：本地动画依赖，无需渲染时连接 CDN。
- `compositions/`：留空，供新场景使用。
- `renders/`：留空，供新成片使用。
- `manifest.json`：创建时间、来源及素材哈希。
- `CASE_VIDEOS.md`：完整视频清单和缺项说明。
- `qa/blank-check.json`：空白工程 HyperFrames 检查结果。

旧片的时间线、设计方案、旁白、字幕和成片没有复制进来；BGM 完整源文件已按用户要求补入素材目录，尚未放入时间线。所有素材是独立文件副本，不是指向旧工程的软链接。

## 45 条主视频已补齐

15 个任务 × Easy / Medium / Hard = 45 条主视频，每个组合恰好一条。

原展示库的 35 条明确标注难度的视频保留；从用户指定的 `Mind2Act-15任务-三档演示.zip` 补入 P Easy/Medium、CP04 Medium/Hard、FR1 三档及 FR2 三档，共 10 条。原来的 4 条未分级演示及 `ungraded` 目录已按用户要求删除。

完整压缩包已经解压到 `/home/xzy/xzy_project/robostream++/mind2act_video/video materio/Mind2Act-15任务-三档演示/`，其中有全部 45 条 640×480、30fps、原速头相机训练采集演示及离线观看页。新工程仅补入此前缺少或未分级的组合，已有较高分辨率展示片未被替换。

所有归档视频的哈希、帧数、帧率和分辨率已与随包 manifest 核对；补入视频为训练采集演示，不是模型评测结果。详细来源见 `CASE_VIDEOS.md`、`manifest.json` 及 `assets/source-metadata/training-demos-20261009/`。

## 使用

```bash
cd /home/xzy/xzy_project/robostream++/outputs/mind2act-hyperframes-blank-20261010-111117
npm run dev
npm run check
```

`npm` 脚本通过 `scripts/hyperframes.sh` 使用本机 Node 22、FFmpeg 和已安装的 HyperFrames 0.8.143 插件。封装只设置当前命令的环境，不修改系统配置。

新片制作完成后可执行 `npm run render -- --quality delivery --output renders/new-version.mp4`。本次准备阶段没有渲染视频或启动新的预览服务。
