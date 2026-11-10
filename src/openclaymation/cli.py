"""
OpenClaymation Command Line Interface (CLI).
Manage Blender stop-motion setups, run MCP servers, and compile claymation videos.
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .blender.bridge import find_blender_binary, run_inline_blender_code
from .blender.clay_shader import CLAY_PALETTES

console = Console()


@click.group()
def main():
    """🎨 OpenClaymation: Autonomous Stop-Motion Clay Studio for Claude & Blender."""
    pass


@main.command()
def info():
    """Inspect local Blender installation and system environment."""
    console.print(Panel.fit("[bold magenta]OpenClaymation Studio Environment[/bold magenta]"))
    try:
        blender_path = find_blender_binary()
        console.print(f"[green]✓[/green] Blender binary found: [cyan]{blender_path}[/cyan]")
    except Exception as e:
        console.print(f"[red]✗[/red] Blender not found: {e}")

    table = Table(title="Available Procedural Clay Palettes")
    table.add_column("Palette Name", style="cyan")
    table.add_column("RGBA Value", style="green")

    for k, v in CLAY_PALETTES.items():
        table.add_row(k, str(v))

    console.print(table)


@main.command()
def mcp():
    """Launch the Model Context Protocol (MCP) server for Claude Desktop / Claude Code."""
    console.print("[bold green]Starting OpenClaymation FastMCP server on stdio...[/bold green]")
    from .mcp.server import run as run_server
    run_server()


@main.command()
@click.option("--output", "-o", default="./demo_clay.blend", help="Output .blend file path")
def demo(output):
    """Generate an instant demo scene: Clay ball morphing with fingerprints and warm lighting."""
    console.print(f"[bold yellow]Generating demo clay scene in Blender...[/bold yellow]")
    code = f"""
import bpy
from openclaymation.blender.studio_stage import build_miniature_stage
from openclaymation.blender.clay_shader import apply_clay_to_object
from openclaymation.blender.stop_motion_rig import setup_stop_motion_environment, add_camera_chatter

# Clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Stage & lighting
build_miniature_stage()
setup_stop_motion_environment()

# Add demo clay character/sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.7, location=(0, 0, 0.7))
clay_ball = bpy.context.active_object
clay_ball.name = "Demo_Clay_Character"

# Add clay material
apply_clay_to_object(clay_ball, palette_name="terracotta", fingerprint_scale=24.0)

# Add camera chatter
if bpy.context.scene.camera:
    add_camera_chatter(bpy.context.scene.camera)

bpy.ops.wm.save_as_mainfile(filepath="{output}")
print("DEMO_CREATED_SUCCESSFULLY")
"""
    res = run_inline_blender_code(code)
    console.print(f"[bold green]✓ Demo scene created at: {output}[/bold green]")


if __name__ == "__main__":
    main()
