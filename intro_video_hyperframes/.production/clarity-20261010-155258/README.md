# Source clarity restoration

Created at: 2026-10-10T15:52:58+08:00.

The replacement sources are 640x480. Large case views use conservative Real-ESRGAN restoration, including the three featured cases, six-tile opening and rapid case montage. Small 45-case mosaic tiles already downscale their source and are unchanged. Order, target-line and piano-memory stills retain their original pixels.

Official model: https://github.com/xinntao/Real-ESRGAN
Model weights: realesr-general-x4v3 (35%) and its weak-denoise variant (65%). Restored output is mixed with 20% Lanczos-resized source. The supplied source files are untouched. Model source and license are in models/.

This is perceptual restoration for promotional media, not recovered ground-truth detail. Geometric aliasing in the low-resolution render cannot be fully eliminated. No benchmark observations or evaluation data are changed.

Rebuild derivatives using the CUDA Python environment with enhance.py --build. activate.py switches compositions to available restored MP4s. before/ retains the preceding compositions. provenance.json records source hashes, timestamps, crop, speed and output paths. qa/comparison.png compares the same source frame before and after restoration.
