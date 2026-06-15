import os
import io
import google.generativeai as genai
from PIL import Image

def get_model():
    """
    Helper to configure Google Generative AI and retrieve the model.
    Raises ValueError if GOOGLE_API_KEY is not set.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API Key is missing. Please provide GOOGLE_API_KEY in your .env file.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-3.5-flash")

def generate(prompt: str, max_tokens: int = 2000) -> str:
    """
    Generate content using Gemini Flash.
    """
    try:
        model = get_model()
        config = genai.types.GenerationConfig(max_output_tokens=max_tokens)
        response = model.generate_content(prompt, generation_config=config)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini generation failed: {str(e)}")

def analyze_image_and_generate(image_bytes: bytes, prompt: str) -> str:
    """
    Analyze image and generate content using Gemini Flash.
    """
    try:
        model = get_model()
        image = Image.open(io.BytesIO(image_bytes))
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini Image Analysis failed: {str(e)}")
