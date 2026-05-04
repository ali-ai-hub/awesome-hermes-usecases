# AI Video Generation: HTML-to-MP4 Pipeline

| **Aspect** | **Detail** |
|---|---|
| **Category** | Content & Creative Pipelines |
| **Complexity** | Intermediate |
| **Hermes Features Used** | `terminal`, `execute_code`, `skill_add`, file tools, cron |
| **Primary Sources** | [HyperFrames by HeyGen](https://github.com/HeyGenAI/hyperframes), [Open Design by Nexu](https://github.com/nexu-io/open-design), installed HyperFrames skill in Hermes |

---

## Overview

Hermes writes, designs, and renders MP4 videos entirely through code — no timeline editor, no manual export. The agent generates HTML compositions with GSAP animations, then renders them to MP4 via Chrome headless + FFmpeg.

Two tools combine under Hermes orchestration:

- **Open Design** — Open-source alternative to Claude Design. 72 brand-grade design systems + 31 composable skills. Hermes is one of 13 auto-detected coding-agent CLIs. Generates the visual design as HTML.
- **HyperFrames** — Renders HTML → MP4. GSAP timeline animations, shader transitions, social overlays, TTS narration (Kokoro, local). CLI-based: `npx hyperframes render`.

The pipeline: Idea → Hermes + Open Design (write HTML composition) → HyperFrames (render) → MP4 → publish.

---

## Who's Doing This

Content creators who want programmatic video generation without opening Premiere or After Effects. Faceless video channels, AI explainers, product demos, social media content. The user already has cloned voice via Coqui TTS and music via HeartMuLa — this pipeline completes the visual layer.

---

## How It Works

### Step 1: Install Both Tools

```bash
# HyperFrames — scaffold a project
npx hyperframes init my-video
cd my-video

# Open Design — available via Hermes skill or direct clone
git clone https://github.com/nexu-io/open-design.git
```

### Step 2: Hermes Generates the HTML Composition

Hermes uses Open Design to produce a designed HTML file following HyperFrames composition rules:

- Root element with `data-composition-id`, `data-duration`, `data-width`, `data-height`
- Every timed element needs `data-start`, `data-duration`, `data-track-index`, `class="clip"`
- GSAP timeline registered on `window.__timelines["main"]` with `{ paused: true }`
- Video elements must be `muted`; audio goes in separate `<audio>` elements

Hermes writes this to `index.html` in the HyperFrames project.

### Step 3: Add Narration and Music

```bash
# TTS narration via HyperFrames (Kokoro, local, no API key)
npx hyperframes tts --text "Your script here" --voice af_heart --output narration.wav

# Or use Coqui TTS with cloned voice if preferred
# Background music via HeartMuLa skill
```

### Step 4: Lint and Preview

```bash
npx hyperframes lint
npx hyperframes preview   # opens in browser for quick check
```

### Step 5: Render to MP4

```bash
# Standard render (1920×1080, 30fps)
npx hyperframes render

# Or specific output
npx hyperframes render --fps 30 --output final.mp4
```

Output lands in `renders/<project>_<timestamp>.mp4`.

### Step 6: Automate with Cron

Once the pipeline is working, Hermes can automate the full loop:

```yaml
# Hermes cron job: daily AI news video
schedule: "0 8 * * *"
prompt: |
  Research top AI news from last 24 hours.
  Write a 60-second script.
  Generate HTML composition with Open Design.
  Render MP4 via HyperFrames.
  Save to ~/videos/today.mp4.
```

---

## Required Setup

- **Node.js** — for HyperFrames CLI (`npx hyperframes`)
- **FFmpeg** — in PATH or at `/tmp/ffmpeg/`
- **Chrome/Chromium** — headless for rendering
- **Open Design** — cloned repo or Hermes skill
- **Python 3.10+** — for Coqui TTS (optional, if using cloned voice)
- **~2GB disk** — for HyperFrames + FFmpeg + output files

---

## What Makes It Work

**Design + Render are both code.** There's no GUI bottleneck. Hermes writes HTML → HyperFrames renders it. Every element in the timeline is a DOM element with `data-start`/`data-duration` attributes — the agent can reason about timing as code, not as a visual timeline.

**GSAP is deterministic.** Animations defined as `tl.from("#el", {...}, offset)` are frame-precise and reproducible. No `Math.random()`, no async — the same HTML always produces the same MP4.

**Open Design provides visual vocabulary.** Instead of Hermes inventing design from scratch, Open Design gives it 72 battle-tested design patterns to remix. The agent picks a design system, then generates content within those constraints.

---

## Real-World Constraints

- **HyperFrames linting is strict.** Overlapping clips on the same track, missing `class="clip"`, or root without dimensions all fail. Hermes iterates: generate → lint → fix → repeat.
- **Video elements need wrapper divs.** Animating `<video>` width/height directly breaks frame rendering. Hermes learns this anti-pattern after first failure.
- **Render time scales with duration.** 60s video at 30fps ≈ 3-5 minutes on CPU. Draft mode (15fps) cuts this to ~1 minute for iteration.
- **TTS quality varies.** Kokoro voices are solid for product demos but less expressive than cloned Coqui voice for storytelling.

---

## Primary Sources

- **HyperFrames:** [github.com/HeyGenAI/hyperframes](https://github.com/HeyGenAI/hyperframes) — AI-native video composition framework
- **Open Design:** [github.com/nexu-io/open-design](https://github.com/nexu-io/open-design) — 72 design systems, 31 skills, Hermes auto-detected as coding-agent CLI
- **HyperFrames skill:** Installed in Hermes at `~/.hermes/skills/hyperframes/` — complete reference with block catalog, lint rules, anti-patterns

---

## Related Use Cases

- [Creative Screen Recording → Video](creative-screen-recording-video.md) — Capturing screen content to video
- [Autonovel — House of Bells](autonovel-house-of-bells.md) — End-to-end creative production
- [ComfyUI Workflow Orchestration](comfyui-workflow-orchestration.md) — Image/video gen via ComfyUI node graphs

---

## Why It's Novel

Unlike ComfyUI (diffusion-based generation) or screen recording (capturing existing output), this pipeline generates video *from designed HTML compositions*. Every frame is DOM-rendered — text, layouts, colors, motion — not pixel-sampled from a diffusion model. This gives pixel-perfect typography, brand-consistent color, and fully scriptable motion that diffusion models can't match. The output looks like a designed video, not an AI-generated one.
