"""
Blender Bridge: Execution & Headless Pipeline Controller.
Locates the Blender executable across macOS, Linux, and Windows,
and executes procedural claymation generation scripts.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def find_blender_binary() -> str:
    """
    Finds the active Blender binary on the system.
    """
    # 1. Environment variable override
    if "BLENDER_BIN" in os.environ and os.path.exists(os.environ["BLENDER_BIN"]):
        return os.environ["BLENDER_BIN"]

    # 2. Check PATH
    bin_in_path = shutil.which("blender")
    if bin_in_path:
        return bin_in_path

    # 3. macOS standard paths
    macos_paths = [
        "/Applications/Blender.app/Contents/MacOS/Blender",
        os.path.expanduser("~/Applications/Blender.app/Contents/MacOS/Blender"),
    ]
    for p in macos_paths:
        if os.path.exists(p):
            return p

    # 4. Linux standard paths
    linux_paths = [
        "/usr/bin/blender",
        "/usr/local/bin/blender",
        "/snap/bin/blender",
    ]
    for p in linux_paths:
        if os.path.exists(p):
            return p

    # 5. Windows standard paths
    win_paths = [
        r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
    ]
    for p in win_paths:
        if os.path.exists(p):
            return p

    raise FileNotFoundError(
        "Blender binary not found! Please install Blender (https://www.blender.org) "
        "or set the BLENDER_BIN environment variable."
    )


def run_blender_script(script_path: str, blend_file: str = None, background: bool = True, extra_args: list = None) -> subprocess.CompletedProcess:
    """
    Executes a python script inside Blender.
    """
    blender_bin = find_blender_binary()
    cmd = [blender_bin]

    if background:
        cmd.append("-b")

    if blend_file and os.path.exists(blend_file):
        cmd.append(blend_file)

    cmd.extend(["-P", str(script_path)])

    if extra_args:
        cmd.append("--")
        cmd.extend(extra_args)

    return subprocess.run(cmd, capture_output=True, text=True, check=True)


def run_inline_blender_code(code: str, background: bool = True) -> str:
    """
    Writes arbitrary python code to a temporary file and runs it headlessly in Blender.
    Returns stdout.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        temp_script = f.name

    try:
        res = run_blender_script(temp_script, background=background)
        return res.stdout
    finally:
        if os.path.exists(temp_script):
            os.remove(temp_script)
