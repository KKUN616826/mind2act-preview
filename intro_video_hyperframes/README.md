# Mind2Act World · 宣传片

已在此工程完成 47.4 秒、1920×1080、30fps 的 HyperFrames 宣传片，包含英文旁白、用户提供的背景音乐和真实来源的任务演示素材。

成片、网页版本、海报与英文字幕见 `renders/`；准确的文件名、技术参数、来源记录与校验值见 `renders/delivery.json`。所有原始素材保留在 `assets/videos`、`assets/logos`、`assets/audio`。

## 继续编辑

```bash
npm run check
bash scripts/hyperframes.sh preview --background --port 3052
```

`index.html` 组装七段可编辑场景；`compositions/` 为各段的 HTML/CSS/GSAP。`BRIEF.md`、`DESIGN.md`、`STORYBOARD.md` 记录结构与设计。`.production/build_film.py` 可以重新生成时间线，直接修改 HTML 后请勿运行生成器覆盖手工改动。

时间结构：Logo 0–5.185s；动机 5.185–11.852s；Mind 11.852–17.778s；Act 17.778–23.704s；Mind2Act 23.704–29.630s；案例/规模/难度 29.630–42.222s；结尾 42.222–47.407s。

## 来源与验证

网站事实保存在 `.production/website-facts.json`。45 条视频形成全部案例拼贴；重点使用 P 配餐、PR3 画线、CP05 弹琴。2026-10-10 已更新到用户替换的 45 条新版源视频，当前生成素材位于 `assets/generated/source-refresh-20261010-142512/`。新版源时间、裁切、速度与哈希记录在 `.production/source-refresh-20261010-142512/case-media-provenance.json` 和 `montage-provenance.json`；旧版来源记录保留供历史核对。

音频采用 81 BPM 网格；旁白、音乐和音效独立保留在 `assets/generated/audio`。`qa/` 保存 HyperFrames 检查、动画映射、从最终 MP4 抽取的画面和解码检查。原空白工程说明保存在 `.production/blank-project-readme.md`；原始 `manifest.json` 未改动。
