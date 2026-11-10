# Model Context Protocol (MCP) Specification

OpenClaymation complies with Anthropic's Model Context Protocol (MCP) specification to bridge Claude with local 3D execution environments.

## Connection Config

### Claude Desktop
Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

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

### Claude Code CLI
```bash
claude mcp add openclaymation python -m openclaymation.mcp.server
```

---

## Tool Reference

### `stage_clay_scene`
- **Description**: Spawns miniature cyclorama stage, warm 3-point lighting, and camera.
- **Parameters**:
  - `theme` (*string*, default: `"warm_studio"`): Studio mood preset.
  - `backdrop_color` (*string*, default: `"terracotta"`): Palette color for the clay backdrop.

### `apply_clay_material`
- **Description**: Applies procedural plasticine material with fingerprints and SSS.
- **Parameters**:
  - `object_name` (*string*, required): Name of the target Blender object.
  - `palette` (*string*, default: `"terracotta"`): Clay color preset (`terracotta`, `midnight_blue`, `olive_green`, `mustard_yellow`, `plasticine_red`, `plasticine_cyan`, `sculpting_grey`, `porcelain_white`).
  - `fingerprint_scale` (*float*, default: `28.0`): Scale of procedural whorls.

### `bake_stopmotion_physics`
- **Description**: Steps animation f-curves on twos and injects natural camera micro-bumps.
- **Parameters**:
  - `step_size` (*int*, default: `2`): Keyframe step (2 corresponds to 12 FPS on a 24 FPS timeline).
  - `camera_jitter` (*bool*, default: `true`): Whether to add organic hand-placement camera chatter.

### `render_claymation_frames`
- **Description**: Renders PNG sequence of current scene.
- **Parameters**:
  - `output_dir` (*string*, required): Destination folder path.
  - `start_frame` (*int*, default: `1`): First frame to render.
  - `end_frame` (*int*, default: `48`): Final frame to render.

### `execute_blender_code`
- **Description**: Runs custom procedural Python inside Blender for bespoke modeling and animation.
- **Parameters**:
  - `python_code` (*string*, required): Valid `bpy` Python script.
