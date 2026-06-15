def blog_post(topic: str, tone: str, audience: str, extra_context: str = "") -> str:
    """
    Generate a blog post prompt.
    """
    prompt = f"Write a detailed, engaging blog post about {topic}.\nTone: {tone}.\nTarget audience: {audience}.\nInclude: catchy title, introduction, 3-5 main sections with subheadings, conclusion with CTA. Format in Markdown."
    if extra_context:
        prompt += f"\n\nAdditional visual context/details from uploaded image:\n{extra_context}"
    return prompt

def social_caption(topic: str, tone: str, platform: str, audience: str, extra_context: str = "") -> str:
    """
    Generate a social media caption prompt.
    """
    prompt = f"Write a {platform} caption about {topic}.\nTone: {tone}.\nAudience: {audience}.\nInclude relevant hashtags. Keep it platform-appropriate (Instagram: visual+emojis, LinkedIn: professional, Twitter: concise)."
    if extra_context:
        prompt += f"\n\nAdditional visual context/details from uploaded image:\n{extra_context}"
    return prompt

def email_copy(topic: str, tone: str, audience: str, extra_context: str = "") -> str:
    """
    Generate a marketing email prompt.
    """
    prompt = f"Write a marketing email about {topic}.\nTone: {tone}.\nAudience: {audience}.\nInclude: subject line, preview text, body with clear CTA, sign-off. Format clearly labeled."
    if extra_context:
        prompt += f"\n\nAdditional visual context/details from uploaded image:\n{extra_context}"
    return prompt

def youtube_script(topic: str, tone: str, audience: str, extra_context: str = "") -> str:
    """
    Generate a YouTube video script prompt.
    """
    prompt = f"Write a YouTube video script about {topic}.\nTone: {tone}.\nAudience: {audience}.\nInclude: hook (first 15 seconds), main content with timestamps, outro with subscribe CTA. Label all sections."
    if extra_context:
        prompt += f"\n\nAdditional visual context/details from uploaded image:\n{extra_context}"
    return prompt

def audio_script(topic: str, tone: str, audience: str, extra_context: str = "") -> str:
    """
    Generate a podcast/voiceover script prompt.
    """
    prompt = f"Write a podcast/voiceover audio script about {topic}.\nTone: {tone}.\nAudience: {audience}.\nInclude: intro, main segments, outro. Add speaker notes in [brackets]. No markdown — plain spoken language only."
    if extra_context:
        prompt += f"\n\nAdditional visual context/details from uploaded image:\n{extra_context}"
    return prompt

def image_analysis(image_description: str, content_type: str, topic: str, tone: str) -> str:
    """
    Generate content based on image analysis.
    """
    return f"You have been given an image. Description/context: {image_description}. Based on this image, generate {content_type} content about {topic}. Tone: {tone}. Use visual details from the image to make content more specific and engaging."
