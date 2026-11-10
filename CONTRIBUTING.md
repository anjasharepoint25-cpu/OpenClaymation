# Contributing to OpenClaymation

We welcome contributions from animators, 3D artists, machine learning researchers, and open-source developers worldwide!

## How You Can Contribute

1. **Procedural Shaders**: Create new clay, plasticine, armature wire, or miniature prop shaders for Blender.
2. **MCP Tooling**: Expand tools for Claude (e.g., character rigging, facial morphing, multi-camera cuts).
3. **Audio-Video Assembly**: Improve FFmpeg demuxing, TTS integration, and subtitle styling.
4. **Documentation & Showcases**: Share your animated episodes and showcase videos!

## Development Setup

```bash
git clone https://github.com/kalimahsaktirinjani/OpenClaymation.git
cd OpenClaymation
pip install -e ".[dev]"
```

Run test suite:
```bash
pytest
```

## Pull Request Workflow

1. Fork the repo and create a feature branch (`git checkout -b feature/awesome-clay-rig`).
2. Commit your changes with descriptive messages.
3. Push to your branch and open a Pull Request against `main`.
4. Ensure CI tests pass.
