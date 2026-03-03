# Bilibili Image Clipper

A tool to crop images from clipboard to 169x169 pixels and generate creative 4-character names using Ollama's qwen-vl:2b-instruct model.

## Installation

1. Install Ollama and pull the model:
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
- Generate a 4-character name using AI
- Save as `[generated_name].png` in current directory

## Requirements

- Python 3.12+
- Ollama running locally with qwen-vl:2b-instruct model

Also, you might want to update your `src/__init__.py` to expose the main function. Add this at the bottom of your file:

```python
# src/__init__.py

# ... (your existing code from the previous response)

# Export the main function
__all__ = ['main']

# This allows the script to be run as a module
if __name__ == "__main__":
    main()
```

Now you can install your package in development mode with:
```bash
uv pip install -e .
```

And run it with:
```bash
bilibili-clip
```

Or as a module:
```bash
python -m src
```