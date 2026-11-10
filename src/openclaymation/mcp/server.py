"""
OpenClaymation FastMCP Server.
Compatible with Claude Desktop, Claude Code, Cursor, Windsurf, and Antigravity.
"""

import sys
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    # Minimal fallback mock for local environments before pip install mcp
    class FastMCP:
        def __init__(self, name: str):
            self.name = name
            self._tools = {}

        def tool(self):
            def decorator(fn):
                self._tools[fn.__name__] = fn
                return fn
            return decorator

        def run(self):
            print(f"[{self.name}] Running FastMCP server (Stdio)...", file=sys.stderr)
            import json
            for line in sys.stdin:
                if not line.strip():
                    continue
                try:
                    req = json.loads(line)
                    # Simple echo response
                    print(json.dumps({"jsonrpc": "2.0", "id": req.get("id"), "result": {}}))
                    sys.stdout.flush()
                except Exception as e:
                    print(json.dumps({"jsonrpc": "2.0", "error": str(e)}))
                    sys.stdout.flush()

from .tools import (
    mcp_stage_clay_scene,
    mcp_apply_clay_material,
    mcp_bake_stopmotion_physics,
    mcp_render_frames,
    mcp_execute_blender_code,
)

mcp = FastMCP("openclaymation")


@mcp.tool()
def stage_clay_scene(theme: str = "warm_studio", backdrop_color: str = "terracotta") -> str:
    """
    Sets up a miniature claymation stage in Blender with cyclorama backdrop,
    warm 3-point studio lighting, and macro lens camera.
    """
    res = mcp_stage_clay_scene(theme, backdrop_color)
    return str(res)


@mcp.tool()
def apply_clay_material(object_name: str, palette: str = "terracotta", fingerprint_scale: float = 28.0) -> str:
    """
    Applies authentic procedural plasticine/clay material with subtle fingerprints
    and subsurface scattering to a named 3D object in Blender.
    Available palettes: terracotta, midnight_blue, olive_green, mustard_yellow,
    plasticine_red, plasticine_cyan, sculpting_grey, porcelain_white.
    """
    res = mcp_apply_clay_material(object_name, palette, fingerprint_scale)
    return str(res)


@mcp.tool()
def bake_stopmotion_physics(step_size: int = 2, camera_jitter: bool = True) -> str:
    """
    Converts smooth 3D animation into authentic 12 FPS stop-motion stepping (on twos)
    and introduces organic camera bumps and animator chatter.
    """
    res = mcp_bake_stopmotion_physics(step_size, camera_jitter)
    return str(res)


@mcp.tool()
def render_claymation_frames(output_dir: str, start_frame: int = 1, end_frame: int = 48) -> str:
    """
    Renders claymation frame sequence to PNG images at 1080x1920 (vertical) or configured resolution.
    """
    res = mcp_render_frames(output_dir, start_frame, end_frame)
    return str(res)


@mcp.tool()
def execute_blender_code(python_code: str) -> str:
    """
    Executes raw Blender Python (bpy) code inside Blender. Use this to model clay characters,
    shape plasticine props, animate transforms, and setup scene blocking.
    """
    res = mcp_execute_blender_code(python_code)
    return str(res)


def run():
    """Runs the MCP server on stdio transport."""
    mcp.run()


if __name__ == "__main__":
    run()
