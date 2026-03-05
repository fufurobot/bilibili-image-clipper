# Bilibili Image Clipper

A tool to crop images from clipboard to 169x169 pixels and generate creative 4-character names using Ollama's qwen-vl:2b-instruct model.

## Installation

1. Install Ollama and pull the model \[WIP, debugging\]:
```bash
ollama pull qwen-vl:2b-instruct
ollama serve
```

2. Install the package:
```bash
uv pip install -e .
```

## Usage

1. Copy an image to your clipboard (screenshot or copy image file)
2. Run the command:
```bash
bilibili-clip
```

The script will:
- Read image from clipboard
- Crop it to 169x169 (centered square)
- Generate a 4-character name using AI \[WIP, debugging\]
- Save as `[generated_name].png` in current directory
