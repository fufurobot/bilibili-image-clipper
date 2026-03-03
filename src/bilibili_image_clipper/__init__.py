import pyperclip
from PIL import Image
import io
import base64
import requests
import json
import os
import tempfile

def read_image_from_clipboard():
    """Read image from clipboard"""
    try:
        # Try to get image from clipboard
        image = Image.open(io.BytesIO(pyperclip.paste()))
        return image
    except:
        # Alternative method for Windows/Linux
        try:
            from PIL import ImageGrab
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                return image
            elif isinstance(image, list) and len(image) > 0:
                # Handle file list
                image = Image.open(image[0])
                return image
        except:
            pass
    
    raise Exception("No image found in clipboard")

def crop_to_square(image, size=169):
    """Crop image to 169x169 square from center"""
    width, height = image.size
    
    # Calculate crop box to get center square
    if width > height:
        left = (width - height) // 2
        top = 0
        right = left + height
        bottom = height
    else:
        left = 0
        top = (height - width) // 2
        right = width
        bottom = top + width
    
    # Crop and resize
    cropped = image.crop((left, top, right, bottom))
    resized = cropped.resize((size, size), Image.Resampling.LANCZOS)
    
    return resized

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def compress_to_under_16kb(image, max_size=16384):
    """
    Compress image to ensure PNG file size is under max_size (default 16KB).
    Returns a tuple (compressed_image, bytes_buffer) where compressed_image is a PIL Image.
    """
    # Start with original RGB image
    img_rgb = image.convert("RGB")
    
    # First attempt: save with maximum compression, original colors
    buffer = io.BytesIO()
    img_rgb.save(buffer, format="PNG", optimize=True, compress_level=9)
    size = buffer.tell()
    print(f"Original size: {size} bytes")
    
    if size <= max_size:
        print("Already under 16KB, no compression needed.")
        return img_rgb, buffer
    
    # If too large, try reducing colors
    color_levels = [128, 64, 32, 16, 8, 4, 2]
    for colors in color_levels:
        print(f"Trying {colors} colors...")
        # Quantize to palette
        quantized = img_rgb.quantize(colors=colors)
        buffer = io.BytesIO()
        quantized.save(buffer, format="PNG", optimize=True, compress_level=9)
        size = buffer.tell()
        print(f"Size with {colors} colors: {size} bytes")
        if size <= max_size:
            print(f"Success with {colors} colors.")
            # Convert back to RGB? No, palette is fine for PNG.
            return quantized, buffer
    
    # If still too large (unlikely for 169x169), fallback to most aggressive (2 colors)
    print("Warning: Could not get under 16KB even with 2 colors. Using 2-color image.")
    return quantized, buffer

def generate_name_with_ollama(image_base64):
    """Generate 4-character name using Ollama qwen-vl:2b-instruct"""
    
    # Prepare the prompt
    prompt = """Generate a creative 4-character name for this image. 
    The name should be exactly 4 characters long - can be letters, numbers, or symbols.
    Only respond with the 4 characters, nothing else."""
    
    # Prepare the request payload
    payload = {
        "model": "qwen-vl:2b-instruct",
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [image_base64]
            }
        ],
        "stream": False
    }
    
    # Make the request to Ollama
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            # Extract the response content
            name = result.get('message', {}).get('content', '').strip()
            
            # Clean up the response - take first 4 characters if response is longer
            if len(name) > 4:
                # Try to find a 4-char sequence
                words = name.split()
                for word in words:
                    if len(word) == 4:
                        name = word
                        break
                else:
                    name = name[:4]
            elif len(name) < 4:
                # Pad with underscores if too short
                name = name.ljust(4, '_')
            
            return name
        else:
            print(f"Ollama API error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to Ollama. Make sure Ollama is running.")
        return None
    except Exception as e:
        print(f"Error generating name: {e}")
        return None

def main():
    try:
        print("Reading image from clipboard...")
        image = read_image_from_clipboard()
        print(f"Image loaded: {image.size}")
        
        print("Cropping to 162x162...")
        cropped_image = crop_to_square(image, 162)
        
        print("Encoding image for AI analysis...")
        image_base64 = encode_image_to_base64(cropped_image)
        
        print("Generating name with Ollama...")
        name = generate_name_with_ollama(image_base64)
        
        if not name:
            print("Failed to generate name, using fallback...")
            # Generate a fallback name based on timestamp
            import time
            name = hex(int(time.time()))[-4:].upper()
        
        # Ensure name is valid for filename
        safe_name = "".join(c for c in name if c.isalnum() or c in "._-")
        if not safe_name:
            safe_name = "image"
        
        filename = f"{safe_name}.png"
        
        print("Compressing image to stay under 16KB...")
        compressed_image, buffer = compress_to_under_16kb(cropped_image)
        
        print(f"Saving as {filename}...")
        # Save the compressed image from buffer or directly
        with open(filename, "wb") as f:
            f.write(buffer.getvalue())
        
        # Verify final size
        final_size = os.path.getsize(filename)
        print(f"Success! Image saved as: {filename} (Size: {final_size} bytes)")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check if Ollama is available
    try:
        requests.get("http://localhost:11434/api/tags", timeout=2)
    except:
        print("Warning: Ollama doesn't seem to be running at http://localhost:11434")
        print("Make sure Ollama is installed and running with: ollama serve")
        print("And pull the model: ollama pull qwen-vl:2b-instruct")
    
    main()