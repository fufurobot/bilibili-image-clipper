# Bilibili Image Clipper

A tool to crop images from clipboard to 169x169 pixels and generate creative 4-character names using Ollama's qwen3-vl:2b-instruct model.

## Installation

1. Install Ollama and pull the model:
```bash
ollama pull qwen3-vl:2b-instruct
ollama serve # for Microsoft Windows users keep the ollama tray icon there is enough, this is not required
```

2. Install the package (you might want to create a [venv](https://docs.astral.sh/uv/pip/environments/) first like `uv venv` to not to influence the global environment):
```bash
uv pip install -e .
```

## Usage

1. Copy an image to your clipboard (screenshot or copy image file)
2. Run the command:
```bash
uv run bilibili-clip
```

The script will:
- Read image from clipboard
- Crop it to 169x169 (centered square)
- Generate a 4-character name using AI
- Save as `[generated_name].png` in current directory
