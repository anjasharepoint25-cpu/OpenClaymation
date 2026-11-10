"""
MCP (Model Context Protocol) Server for OpenClaymation.
Allows Claude to direct 3D Blender stop-motion scenes autonomously.
"""
from .server import mcp, run

__all__ = ["mcp", "run"]
