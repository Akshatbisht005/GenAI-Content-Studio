import os
import base64
import anthropic

def get_client():
    """
    Helper to initialize and retrieve the Anthropic client safely.
    Raises ValueError if ANTHROPIC_API_KEY is not set.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Anthropic API Key is missing. Please provide ANTHROPIC_API_KEY in your .env file.")
    return anthropic.Anthropic(api_key=api_key)

def generate(prompt: str, max_tokens: int = 2000) -> str:
    """
    Generate content using Claude Sonnet.
    """
    try:
        client = get_client()
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        raise RuntimeError(f"Claude generation failed: {str(e)}")

def analyze_image_and_generate(image_bytes: bytes, media_type: str, prompt: str) -> str:
    """
    Analyze image and generate content using Claude Sonnet.
    """
    try:
        client = get_client()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": base64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt,
                        }
                    ],
                }
            ],
        )
        return response.content[0].text
    except Exception as e:
        raise RuntimeError(f"Claude Image Analysis failed: {str(e)}")
