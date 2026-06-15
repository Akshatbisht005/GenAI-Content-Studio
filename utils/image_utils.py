import io
import base64
from PIL import Image

def load_image(uploaded_file) -> tuple:
    """
    Loads an uploaded file as PIL Image, resizes it if the longest side > 1024px
    (maintaining aspect ratio), and returns the (PIL.Image, resized_bytes, media_type).
    """
    original_bytes = uploaded_file.getvalue()
    pil_image = Image.open(io.BytesIO(original_bytes))
    
    # Detect media type
    fmt = pil_image.format
    if fmt:
        media_type = f"image/{fmt.lower()}"
    else:
        # Fallback mapping
        name = getattr(uploaded_file, "name", "").lower()
        if name.endswith(".png"):
            media_type = "image/png"
            fmt = "PNG"
        elif name.endswith(".webp"):
            media_type = "image/webp"
            fmt = "WEBP"
        else:
            media_type = "image/jpeg"
            fmt = "JPEG"

    width, height = pil_image.size
    max_side = max(width, height)
    
    if max_side > 1024:
        if width > height:
            new_width = 1024
            new_height = int(height * (1024.0 / width))
        else:
            new_height = 1024
            new_width = int(width * (1024.0 / height))
            
        pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save resized image back to bytes
        buffer = io.BytesIO()
        pil_image.save(buffer, format=fmt)
        image_bytes = buffer.getvalue()
    else:
        image_bytes = original_bytes
        
    return pil_image, image_bytes, media_type

def image_to_base64(image_bytes: bytes) -> str:
    """
    Encodes image bytes to base64 string.
    """
    return base64.b64encode(image_bytes).decode("utf-8")
