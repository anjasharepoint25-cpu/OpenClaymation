# OpenClaymation Architecture

OpenClaymation is an open-source autonomous stop-motion and claymation production framework connecting Large Language Models (Claude via Model Context Protocol) with Blender's procedural rendering engine and FFmpeg.

```
┌────────────────────────────────────────────────────────┐
│                   Claude AI Agent                      │
│     (Claude Desktop / Claude Code / Antigravity)       │
└───────────────────────────┬────────────────────────────┘
                            │
               Model Context Protocol (MCP)
                            │
┌───────────────────────────▼────────────────────────────┐
│              OpenClaymation MCP Server                 │
│                 (FastMCP on Stdio)                     │
└─────┬─────────────────────┬──────────────────────┬─────┘
      │                     │                      │
┌─────▼──────────────┐┌─────▼──────────────┐┌──────▼─────────────┐
│ Procedural Clay    ││ Stop-Motion Rig    ││ Tabletop Studio    │
│ Shader Generator   ││ Stepper (12 FPS)   ││ Lighting & Camera  │
│ - Fingerprint Bump ││ - Animate on Twos  ││ - Warm 3200K key   │
│ - Subsurface (SSS) ││ - Camera Chatter   ││ - Macro 65mm f/2.8 │
│ - Clay Knead Marks ││ - Stepped F-curves ││ - Cyclorama set    │
└────────────────────┘└────────────────────┘└────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                 Blender 3.6 / 4.x / 5.x                │
│             (Headless or Interactive Mode)             │
└───────────────────────────┬────────────────────────────┘
                            │ PNG Frames (12 FPS)
┌───────────────────────────▼────────────────────────────┐
│             Video Assembler & Narration Sync           │
│         - Paragraph silence detection via FFmpeg       │
│         - 12 FPS hold -> 24 FPS social format          │
│         - Subtitle burn-in (Libass / SRT)              │
│         - Cliffhanger end-card generator               │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
              Finished 9:16 / 16:9 MP4 Video
```

## Core Modules

### 1. `openclaymation.blender.clay_shader`
Constructs procedural Blender material node trees mimicking real-world oil-based plasticine:
- **Procedural Fingerprints**: Blended Wave and Voronoi texture algorithms mapped to object coordinates with normal bump mapping.
- **Subsurface Scattering (SSS)**: Simulates the organic translucency of kneaded clay when illuminated by studio lights.
- **Micro-Roughness**: Simulates dust, tiny sculpting tool marks, and non-uniform oil absorption.

### 2. `openclaymation.blender.stop_motion_rig`
Replicates traditional physical stop-motion animation physics:
- **12 FPS Stepped Interpolation**: Converts smooth computer interpolation curves into stepped holds (holding each pose for 2 frames at a 24 FPS baseline, identical to classic stop-motion studios like Aardman).
- **Camera Chatter**: Introduces organic micro-vibrations across the camera's location and rotation channels, replicating physical table nudges caused by animators moving puppets.
- **Macro Miniature Lens**: Employs shallow depth of field (DoF) to accentuate small tabletop scale.

### 3. `openclaymation.mcp.server`
Exposes high-level tools to Claude and other MCP clients:
- `stage_clay_scene`: Sets up a complete tabletop cyclorama and warm lighting.
- `apply_clay_material`: Applies plasticine shaders to scene geometry.
- `bake_stopmotion_physics`: Steps animations on twos and bakes camera chatter.
- `render_claymation_frames`: Renders sequences to high-resolution PNGs.
- `execute_blender_code`: Executes arbitrary Blender Python commands for full creative freedom.

### 4. `openclaymation.assembler`
Automates post-production:
- Detects breath/paragraph pauses in voiceover audio via FFmpeg `silencedetect`.
- Dynamically allocates frame timing per scene.
- Renders final vertical 1080x1920 MP4 with synchronized subtitles and teaser cliffhanger cards.
