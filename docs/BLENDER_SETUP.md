# Blender Setup Guide

OpenClaymation requires Blender **3.6 LTS, 4.x, or 5.x**.

## Installation

### macOS
1. Download Blender from [blender.org](https://www.blender.org/download/) or install via Homebrew:
   ```bash
   brew install --cask blender
   ```
2. Verify Blender is in `/Applications/Blender.app`.

### Linux (Ubuntu/Debian)
```bash
sudo snap install blender --classic
# or
sudo apt update && sudo apt install blender
```

### Windows
1. Download the official installer from [blender.org](https://www.blender.org/download/).
2. Add Blender to your system `PATH` or define the `BLENDER_BIN` environment variable:
   ```powershell
   setx BLENDER_BIN "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
   ```

---

## Installing the Blender Add-on (Optional GUI)

If you prefer using the Blender 3D Viewport UI:
1. Open Blender.
2. Go to `Edit` > `Preferences` > `Add-ons`.
3. Click the down arrow in the top right and select `Install from Disk...`.
4. Select `src/openclaymation/blender/addon.py`.
5. Check the box to enable **OpenClaymation Studio**.
6. Press `N` in the 3D Viewport to reveal the **ClayStudio** sidebar tab.
