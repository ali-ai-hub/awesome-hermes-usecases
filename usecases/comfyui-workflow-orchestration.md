# ComfyUI Workflow Orchestration

| **Aspect** | **Detail** |
|---|---|
| **Category** | Creative / Media Generation |
| **Complexity** | Intermediate |
| **Hermes Features Used** | `skill_add`, `browser_navigate`, `execute_code`, file tools, sub-agents |
| **Primary Sources** | Reddit post by u/Jonathan_Rivera on r/hermesagent, verified live. ComfyUI ecosystem docs. |

---

## Overview

Hermes can install, launch, manage, and run ComfyUI workflows on demand. It pulls custom nodes, installs dependencies, and executes sophisticated image/video generation pipelines through ComfyUI's node-based backend.

ComfyUI is the most flexible open-source media generation tool with a massive ecosystem of 4,000+ custom nodes. Hermes acts as an orchestration layer on top — fetching workflows, installing missing nodes, and running them deterministically.

---

## Who's Doing This

A Hermes user (Jonathan_Rivera) building media pipelines who wants programmatic access to ComfyUI's node graph without manually clicking through the web UI.

---

## How It Works

### Step 1: Install ComfyUI via Skill

```
hermes skill add comfyui-workflow-runner --from-github <skill-repo>
```

Or manually set up in a workspace:

```bash
# Hermes terminal
git clone https://github.com/comfyanonymous/ComfyUI.git ~/comfyui
pip install -r ~/comfyui/requirements.txt
```

### Step 2: Install Custom Nodes

Hermes reads the workflow JSON, identifies missing custom nodes, and installs them:

```bash
# Hermes detects node dependencies from the workflow file
# Clones into ComfyUI/custom_nodes/
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
# Or other node repos as needed
```

### Step 3: Launch ComfyUI Server

```bash
cd ~/comfyui && python main.py --listen 0.0.0.0 --port 8188
```

Hermes manages this process, kills stale instances, and restarts when config changes.

### Step 4: Load and Execute Workflow

Hermes POSTs the workflow JSON to ComfyUI's `/prompt` endpoint:

```bash
curl -X POST http://localhost:8188/prompt \
  -H "Content-Type: application/json" \
  -d @workflow.json
```

Or Hermes-native via skill:

```
/comfyui-run ~/workflows/portrait-batch.json --output ~/renders/
```

### Step 5: Manage Outputs

Hermes moves generated images/video to project folders, renames by prompt hash, and syncs to cloud storage or Notion galleries.

---

## Required Setup

- Python 3.10+ with `torch`, `torchvision`, `torchaudio`
- ~8GB disk for base ComfyUI + models
- GPU optional but strongly recommended (works on CPU at ~1/20th speed)
- Hermes file-write permission to ComfyUI directories

---

## Real-World Constraints

- **Model downloads are large.** First setup pulls 2-7GB per checkpoint. Hermes caches them.
- **Custom nodes break.** Updates to ComfyUI core can break third-party nodes. Hermes pins known-good commits in workflow metadata.
- **GPU memory limits batch size.** Hermes adjusts `batch_size` automatically based on available VRAM.
- **Workflow JSON is opaque.** Complex graphs are hard to debug. Hermes generates simplified "summary views" of what each node does.

---

## Primary Sources

- **Reddit post:** u/Jonathan_Rivera, r/hermesagent — "Hermes + Comfy UI" (8 points, 11 comments) — "ComfyUI is the most flexible, composable, and powerful open-source media generation tool... Your Hermes Agent can now install, launch, manage, and run sophisticated ComfyUI workflows on demand."
- **ComfyUI GitHub:** [github.com/comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI) — 69k+ stars
- **ComfyUI Manager:** [github.com/ltdrdata/ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager) — node installation helper

---

## Related Use Cases

- [Creative Screen Recording → Video](creative-screen-recording-video.md) — Another media pipeline use case
- [Autonovel — House of Bells](autonovel-house-of-bells.md) — End-to-end creative production pipeline
- [Self-Evolution](self-evolution.md) — Hermes optimizing its own workflows

---

## Why It Works

ComfyUI's node graph is perfect for agents: every operation is a pure function with explicit inputs/outputs. Hermes reads the graph as a dependency tree and executes it programmatically. The combination gives you access to the entire open-source image/video generation ecosystem (Stable Diffusion, Flux, Wan, LTX Video, etc.) without writing any frontend code.
