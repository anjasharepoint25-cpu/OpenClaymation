<div align="center">

# 🏺 OpenClaymation

### **Autonomous 3D Stop-Motion & Claymation AI Studio for Claude, MCP & Blender**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Blender: 3.6 | 4.x | 5.x](https://img.shields.io/badge/Blender-3.6%20%7C%204.x%20%7C%205.x-E87D0D.svg)](https://www.blender.org/)
[![Anthropic MCP](https://img.shields.io/badge/MCP-Native%20Compatible-blueviolet.svg)](https://modelcontextprotocol.io/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill%20Ready-black.svg)](https://claude.ai/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/kalimahsaktirinjani/OpenClaymation/pulls)

<p align="center">
  <b>Don't hallucinate pixels. Direct real 3D physical clay.</b><br>
  OpenClaymation gives Claude and AI agents physical hands inside Blender to sculpt procedural plasticine, stage warm miniature sets, bake 12 FPS stop-motion cadence, and assemble complete narrative episodes.
</p>

[Quickstart](#-quickstart-in-60-seconds) •
[Features](#-key-features) •
[MCP Integration](#-claude-mcp-integration) •
[Claude Skill](#-claude-code-agent-skill) •
[Architecture](docs/ARCHITECTURE.md) •
[Anthropic OSS Application](docs/CLAUDE_OSS_APPLICATION_GUIDE.md)

---

</div>

## 💡 Why OpenClaymation?

Most generative AI video models (Sora, Runway, Kling) produce surreal 2D pixel morphs that suffer from temporal jitter, drifting limbs, and zero physical consistency. 

**OpenClaymation takes a fundamentally different path:**
Instead of guessing video frames, **Claude acts as an autonomous Stop-Motion Director** in Blender:
- Directs actual 3D geometry with true volumetric shadows.
- Coats surfaces in **procedural plasticine shaders** with visible human fingerprints and organic Subsurface Scattering (SSS).
- Locks keyframes into authentic **12 FPS stepped cadence (animating on twos)** with organic camera chatter.
- Compiles the final video with **audio-synced dialogue, subtitles, and cliffhanger endings** via FFmpeg.

Inspired by the tactile magic of *Aardman Animations* (*Wallace & Gromit*, *Chicken Run*) and *Laika* (*Coraline*).

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🏺 **Procedural Clay Engine** | Procedural node trees with dynamic thumbprints, fingernail carving marks, and clay translucency (Cycles & EEVEE). No static image textures needed. |
| ⏱️ **12 FPS Stepped Cadence** | Automatically steps F-curves onto "twos" (holding each pose for 2 frames at 24fps) to eliminate computer smoothness and replicate physical armatures. |
| 🎥 **Miniature Macro Stage** | Tabletop cyclorama backdrops, warm 3-point studio lighting (~3200K), and shallow depth-of-field macro camera lenses (50mm–85mm f/2.8). |
| 🤖 **100% Native MCP Protocol** | Anthropic Model Context Protocol compliant. Works out-of-the-box with Claude Desktop, Claude Code, Cursor, and Antigravity. |
| 🎙️ **Automated Audio-Sync** | Automatically detects breath & paragraph pauses via silence detection, adjusting frame timing per act and burning in styled 9:16 subtitles. |
| 🎛️ **Dual-Mode Workflow** | Use it as a headless AI agent pipeline or as an interactive GUI panel inside Blender. |
| 🎬 **Battle-Tested `anim_lib`** | Included lightweight procedural animation library (`pop`, `hop`, `walk`, `armsto`, `headto`, `mood`, `ending`) dynamically keyed to audio duration arrays `DUR=[...]`. |
| 🧪 **Organic Clay Boil (`BoilCtl`)** | Automatic `CONSTANT` keyframing every 3 frames on displacement modifiers replicating authentic hand-sculpted plasticine boiling. |

---

## 📦 Battle-Tested Production Templates (`templates/`)

OpenClaymation includes the complete production pipeline used to produce 24 broadcast-ready myth reels:

1. **`templates/anim_lib.py`**:
   Zero-dependency procedural animation primitives for Blender. Everything links dynamically to `DUR=[...]` (audio seconds per act). If voiceover length changes, re-running `anim_epN` automatically retimes the entire scene.
2. **`templates/runner.py`**:
   The episode orchestrator: verifies 6-act scripts (190–200 words target), generates 25% resolution test frames (11 contact sheet stills), and prepares clean `.blend` scene files.
3. **`templates/rakit_video.py`**:
   Native Blender VSE video compiler that merges 12 FPS PNG frames and 6-act audio tracks into a pristine H.264/AAC MP4 without needing command-line tools.
4. **`templates/CARA_RENDER.txt`**:
   Detailed Windows (PowerShell) and macOS batch rendering instructions for GPU/CPU farms.
5. **`templates/subtitle_template.ass`**:
   Production-ready ASS subtitle styling: Poppins Bold 80, golden yellow `&H005AC6F5`, dark outline 7, `MarginV 340`.

---

## ⚡ Architecture

```
Claude / AI Agent  ──(MCP Protocol)──►  OpenClaymation Server
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         ▼                                    ▼                                    ▼
Procedural Clay Shaders               12 FPS Stop-Motion Rig               Miniature Tabletop Stage
(Fingerprints & SSS)                  (Stepped Keyframes & Chatter)        (Warm 3200K Studio Lighting)
         │                                    │                                    │
         └────────────────────────────────────┼────────────────────────────────────┘
                                              ▼
                                   Blender 3.6 / 4.x / 5.x
                                              │  (12 FPS PNG Frames)
                                              ▼
                                 FFmpeg Video & Subtitle Assembler
                                              │
                                              ▼
                                Finished 9:16 Claymation Episode
```

---

## 🚀 Quickstart in 60 Seconds

### 1. Prerequisites
- **Blender 3.6 LTS, 4.x, or 5.x** ([Download Blender](https://www.blender.org/download/))
- **Python 3.10+**
- **FFmpeg** (`brew install ffmpeg` on macOS or `sudo apt install ffmpeg` on Linux)

### 2. Install OpenClaymation
```bash
git clone https://github.com/kalimahsaktirinjani/OpenClaymation.git
cd OpenClaymation
pip install -e .
```

### 3. Verify Environment
```bash
openclaymation info
```

---

## 🔌 Claude MCP Integration

Connect OpenClaymation directly to **Claude Desktop** or **Claude Code**.

### Option A: Claude Desktop
Add this to your `claude_desktop_config.json`:

*macOS*: `~/Library/Application Support/Claude/claude_desktop_config.json`  
*Windows*: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "openclaymation": {
      "command": "python",
      "args": ["-m", "openclaymation.mcp.server"]
    }
  }
}
```

### Option B: Claude Code CLI
```bash
claude mcp add openclaymation python -m openclaymation.mcp.server
```

---

## 🧠 Claude Code Agent Skill

OpenClaymation includes a ready-to-use Agent Skill. Once connected, you can give high-level directorial prompts directly to Claude:

> **You:**  
> *"Claude, direct an 8-second vertical stop-motion scene of a terracotta clay golem waking up on a miniature tabletop stage. Give him bead eyes, apply the clay shader with visible fingerprints, and bake the animation to 12 FPS on twos with subtle camera shake."*

> **Claude:**  
> *Calls `stage_clay_scene()` ➔ spawns miniature cyclorama and warm lighting.*  
> *Calls `execute_blender_code()` ➔ sculpts golem armature and keyframes wake-up pose.*  
> *Calls `apply_clay_material()` ➔ applies terracotta plasticine with procedural fingerprints.*  
> *Calls `bake_stopmotion_physics()` ➔ steps keyframes on twos and injects camera chatter.*  
> *Calls `render_claymation_frames()` ➔ outputs 96 distinct frames.*

---

## 🎨 Available Procedural Clay Palettes

| Palette | Hex / Tone | Recommended Use |
| :--- | :--- | :--- |
| `terracotta` | `#C2613D` | Earthy characters, clay humanoids, mythic titans |
| `midnight_blue` | `#141F47` | Night skies, celestial cloaks, deep water props |
| `olive_green` | `#526B33` | Vegetation, tunics, vines, forest creatures |
| `mustard_yellow` | `#D9A626` | Crowns, stars, brass accents, dry grass |
| `plasticine_red` | `#CC2E29` | Capes, hearts, dramatic lighting, warning props |
| `plasticine_cyan` | `#268CBD` | Magical spells, crystals, eyes, skies |
| `sculpting_grey` | `#808080` | Armature bases, stones, clay sculpting masters |
| `porcelain_white` | `#EBE6E0` | Clouds, swaddles, sheep wool, teeth |

---

## 🖥️ Blender Add-on (Optional GUI)

Prefer working directly inside the Blender viewport?
1. Open Blender ➔ `Edit` ➔ `Preferences` ➔ `Add-ons`.
2. Click `Install...` and pick `src/openclaymation/blender/addon.py`.
3. Press `N` in the 3D Viewport to open the **ClayStudio** tab:
   - 🔘 **Spawn Miniature Stage**
   - 🔘 **Apply Clay Material** (with palette selector)
   - 🔘 **Bake 12 FPS Stepper**

---

## 🗺️ Roadmap to v1.0

- [x] FastMCP Server compliant with Anthropic specification
- [x] Procedural fingerprint and SSS clay shader generator (Blender 3.6 – 5.x)
- [x] 12 FPS stepped cadence engine (animating on twos)
- [x] Tabletop miniature studio stage & warm lighting generator
- [x] Audio-sync assembler with FFmpeg silence detection
- [ ] 🗣️ Procedural Clay Face Replacement Mouth Library (Aardman style)
- [ ] 🦴 Automated Clay Armature Rigging Generator
- [ ] 🌐 ComfyUI Bridge for clay-style image-to-3D mesh conditioning
- [ ] 📦 Blender Asset Browser preset library (.blend bundle)

---

## 🤝 Contributing

We welcome contributions from animators, developers, and ML creators!
Check out [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## 📜 License

OpenClaymation is open-source software licensed under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Crafted with tactile love by clay animators and AI open-source contributors.</sub>
</div>
