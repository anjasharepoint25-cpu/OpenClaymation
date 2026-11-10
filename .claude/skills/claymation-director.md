# Claymation Director: Claude Code Skill

This skill empowers Claude Code to autonomously control Blender through the OpenClaymation MCP server to produce stop-motion claymation films.

## When to Activate
- The user requests claymation, stop-motion animation, or plasticine 3D aesthetics.
- The user wants to animate scripts or mythological episodes into 3D clay characters.
- The user wants to render frame-by-frame stylized animations in Blender.

## Available MCP Tools
- `openclaymation.stage_clay_scene`: Sets up tabletop cyclorama stage and warm 3-point lighting.
- `openclaymation.apply_clay_material`: Applies procedural fingerprint and SSS clay shader.
- `openclaymation.bake_stopmotion_physics`: Steps keyframes on twos (12 FPS) and bakes camera chatter.
- `openclaymation.render_claymation_frames`: Renders sequence of PNG frames.
- `openclaymation.execute_blender_code`: Executes custom Blender Python for complex mesh generation.

## Example Command
```bash
# Start MCP server in Claude Code
claude mcp add openclaymation python -m openclaymation.mcp.server
```
