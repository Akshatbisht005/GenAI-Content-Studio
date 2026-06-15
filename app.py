import os
import time
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
import pyperclip

# Load environment variables
load_dotenv()

# Set Streamlit page config
st.set_page_config(
    page_title="GenAI Content Studio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import local modules
from generators import prompts, claude_gen, gemini_gen
from utils import image_utils

# CSS Injection for Premium Dark & Responsive Styling
st.markdown("""
<style>
    /* Gradient Background & App Styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #f1f5f9;
        font-family: 'Outfit', 'Inter', -apple-system, sans-serif;
    }
    
    /* Sidebar customization */
    [data-testid="stSidebar"] {
        background-color: #090d16 !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Headers & Subtitles */
    h1, h2, h3, h4 {
        color: #f8fafc;
        font-weight: 700;
    }
    
    /* Custom Output Container */
    .content-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin: 20px 0;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }
    
    /* Style for platform pill or other metadata */
    .meta-badge {
        background-color: #1e293b;
        color: #94a3b8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        border: 1px solid #334155;
        display: inline-block;
        margin-right: 8px;
    }
    
    /* Status connection badges */
    .status-badge-connected {
        background-color: rgba(34, 197, 94, 0.1);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.2);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 13px;
        display: inline-block;
        margin-top: 5px;
    }
    .status-badge-missing {
        background-color: rgba(239, 68, 68, 0.1);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.2);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 13px;
        display: inline-block;
        margin-top: 5px;
    }
    
    /* Tab formatting */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid #1e293b;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        color: #94a3b8;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.08);
        color: #f8fafc;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border-color: #3b82f6 !important;
        color: #3b82f6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "generated_content" not in st.session_state:
    st.session_state.generated_content = {
        "blog": "",
        "social": "",
        "email": "",
        "youtube": "",
        "audio": ""
    }

if "history" not in st.session_state:
    st.session_state.history = []

# API Keys Check
anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
google_key = os.environ.get("GOOGLE_API_KEY")

# Sidebar Configuration
st.sidebar.markdown("# GenAI Content Studio")
st.sidebar.markdown("Configure your engine, style, and topic parameters.")
st.sidebar.markdown("---")

# Model Selection styled with CSS hints
st.sidebar.markdown("### Select AI Model")
model_options = []
if anthropic_key:
    model_options.append("Claude (Anthropic)")
if google_key:
    model_options.append("Gemini (Google)")

# Fallbacks if keys are missing
if not model_options:
    st.sidebar.warning("No API keys found. Please set them in your `.env` file.")
    model_options = ["Claude (Anthropic)", "Gemini (Google)"]

selected_model = st.sidebar.radio(
    "Active Model",
    options=model_options,
    help="Select the LLM model used to generate content"
)

st.sidebar.markdown("---")

# Content inputs
st.sidebar.markdown("### Content Settings")
topic = st.sidebar.text_input("Content Topic", placeholder="e.g. AI in Healthcare", help="The primary subject of the generated content")
tone = st.sidebar.selectbox(
    "Tone of Voice",
    options=["Professional", "Casual", "Humorous", "Inspirational", "Educational", "Persuasive"]
)
audience = st.sidebar.text_input("Target Audience", placeholder="e.g. startup founders", help="The primary audience group")

# Optional Platform parameter for Social Caption
platform = None

st.sidebar.markdown("---")

# Image Upload
st.sidebar.markdown("### Multimodal Context (Optional)")
uploaded_file = st.sidebar.file_uploader(
    "Upload context image", 
    type=["png", "jpg", "jpeg", "webp"],
    help="Upload an image to guide content creation contextually"
)

use_image = False
image_data = None

if uploaded_file is not None:
    try:
        # Load and resize using utility
        pil_img, img_bytes, mime_type = image_utils.load_image(uploaded_file)
        
        # Display thumbnail
        st.sidebar.image(pil_img, caption="Context Image", width=200)
        
        # Checkbox
        use_image = st.sidebar.checkbox("Use image as content context", value=True)
        image_data = {
            "bytes": img_bytes,
            "mime_type": mime_type,
            "pil": pil_img
        }
    except Exception as e:
        st.sidebar.error(f"Image load error: {e}")

st.sidebar.markdown("---")

# API Keys Indicators
st.sidebar.markdown("### API Key Status")
if anthropic_key:
    st.sidebar.markdown('<div class="status-badge-connected">Claude Key: Connected</div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div class="status-badge-missing">Claude Key: Missing Key</div>', unsafe_allow_html=True)

if google_key:
    st.sidebar.markdown('<div class="status-badge-connected">Gemini Key: Connected</div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div class="status-badge-missing">Gemini Key: Missing Key</div>', unsafe_allow_html=True)

st.sidebar.markdown("<br><p style='font-size:12px; color:#64748b;'>Akshat Bisht &copy; 2026</p>", unsafe_allow_html=True)

# Main Workspace Area
st.markdown("<h1>GenAI Content Studio</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 18px; color: #94a3b8; margin-top: -10px;'>Powered by Claude & Gemini</p>", unsafe_allow_html=True)

# Define Tab Titles
tabs = st.tabs([
    "Blog Post", 
    "Social Caption", 
    "Email Copy", 
    "YouTube Script", 
    "Audio Script"
])

# Spinners list
spinners = [
    "Feeding the algorithms...",
    "Designing your masterpiece...",
    "Summing up the cosmos...",
    "Launching content rockets...",
    "Crafting engaging copy..."
]

# Helper content generation execution
def run_generation(prompt_fun, content_key, tab_name, extra_args={}):
    if not topic.strip():
        st.warning("Please enter a content topic in the sidebar before generating content.")
        return

    # Check key for selected model
    if selected_model == "Claude (Anthropic)" and not anthropic_key:
        st.error("Anthropic API Key is missing. Check your `.env` configuration or switch models.")
        return
    elif selected_model == "Gemini (Google)" and not google_key:
        st.error("Google API Key is missing. Check your `.env` configuration or switch models.")
        return

    # Custom fun spinner
    spinner_msg = spinners[int(time.time()) % len(spinners)]
    
    with st.spinner(spinner_msg):
        try:
            # Build prompt context
            img_description = ""
            
            # If image uploaded and checkbox checked, analyze image first (or send together)
            if use_image and image_data:
                # Obtain image description first or pass directly
                with st.spinner("Running initial image analysis..."):
                    desc_prompt = "Describe this image in detail, focus on objects, colors, text, mood, and style so we can write content based on it."
                    if selected_model == "Claude (Anthropic)":
                        img_description = claude_gen.analyze_image_and_generate(
                            image_data["bytes"], image_data["mime_type"], desc_prompt
                        )
                    else:
                        img_description = gemini_gen.analyze_image_and_generate(
                            image_data["bytes"], desc_prompt
                        )

            # Generate final prompt
            args = {"topic": topic, "tone": tone, "audience": audience, "extra_context": img_description}
            args.update(extra_args)
            
            if use_image and img_description:
                # Use image analysis specific prompt
                prompt = prompts.image_analysis(img_description, tab_name, topic, tone)
            else:
                prompt = prompt_fun(**args)

            # Run LLM Call
            if selected_model == "Claude (Anthropic)":
                result = claude_gen.generate(prompt)
            else:
                result = gemini_gen.generate(prompt)

            # Save content
            st.session_state.generated_content[content_key] = result
            
            # Save history
            st.session_state.history.append({
                "tab": tab_name,
                "model": selected_model,
                "topic": topic,
                "content": result,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            st.success("Content generated successfully!")
        except Exception as e:
            st.error(f"Generation error: {e}")

# Helper to render output actions (Copy, Download, Stats)
def render_output_actions(content, content_key, tab_filename):
    if content:
        # Display word count
        words = len(content.split())
        st.markdown(f"<p style='font-size:14px; color:#94a3b8;'>Generated {words} words</p>", unsafe_allow_html=True)
        
        # Display styled output
        st.markdown(f'<div class="content-box">{content}</div>', unsafe_allow_html=True)
        
        # Action Buttons Column
        col1, col2 = st.columns(2)
        
        with col1:
            # Copy to clipboard
            if st.button("Copy to Clipboard", key=f"copy_{content_key}"):
                try:
                    pyperclip.copy(content)
                    st.success("Copied to clipboard successfully!")
                except Exception:
                    st.warning("Clipboard copy failed natively. You can select and copy the text below:")
                    st.code(content, language="markdown")
                    
        with col2:
            # Download file
            st.download_button(
                label="Download as .txt",
                data=content,
                file_name=f"{tab_filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key=f"download_{content_key}"
            )

# ----------------- TABS IMPLEMENTATION -----------------

# Tab 1: Blog Post
with tabs[0]:
    st.markdown("### Blog Post Generator")
    st.markdown("Generate comprehensive blog posts with catchy titles, clean headings, and CTA guidelines.")
    
    if st.button("Generate Blog Post", type="primary", key="btn_blog"):
        run_generation(prompts.blog_post, "blog", "Blog Post")
        
    render_output_actions(st.session_state.generated_content["blog"], "blog", "blog_post")

# Tab 2: Social Caption
with tabs[1]:
    st.markdown("### Social Caption Generator")
    st.markdown("Platform-customized posts featuring relevant formatting, styles, and emojis.")
    
    # Specific parameter for platform
    platform = st.selectbox(
        "Platform Style", 
        options=["Instagram", "LinkedIn", "Twitter/X", "Facebook"],
        key="social_platform_selector"
    )
    
    if st.button("Generate Social Caption", type="primary", key="btn_social"):
        run_generation(
            prompts.social_caption, 
            "social", 
            "Social Caption", 
            extra_args={"platform": platform}
        )
        
    render_output_actions(st.session_state.generated_content["social"], "social", f"{platform.lower()}_caption")

# Tab 3: Email Copy
with tabs[2]:
    st.markdown("### Email Copy")
    st.markdown("Professional emails containing clear subject lines, preview text, body content, and a defined call-to-action.")
    
    if st.button("Generate Email Copy", type="primary", key="btn_email"):
        run_generation(prompts.email_copy, "email", "Email Copy")
        
    render_output_actions(st.session_state.generated_content["email"], "email", "email_copy")

# Tab 4: YouTube Script
with tabs[3]:
    st.markdown("### YouTube Video Script")
    st.markdown("Structured scripts with timestamp landmarks, hook strategies, and viewer subscription calls.")
    
    if st.button("Generate YouTube Script", type="primary", key="btn_youtube"):
        run_generation(prompts.youtube_script, "youtube", "YouTube Script")
        
    render_output_actions(st.session_state.generated_content["youtube"], "youtube", "youtube_script")

# Tab 5: Audio Script
with tabs[4]:
    st.markdown("### Audio Script")
    st.markdown("Plain spoken text containing reader voice guides and segment changes in brackets.")
    
    if st.button("Generate Audio Script", type="primary", key="btn_audio"):
        run_generation(prompts.audio_script, "audio", "Audio Script")
        
    render_output_actions(st.session_state.generated_content["audio"], "audio", "audio_script")

# History Section at bottom
st.markdown("---")
with st.expander("Generation History (last 5)", expanded=False):
    if st.session_state.history:
        # Show in reverse order (most recent first)
        recent_history = st.session_state.history[::-1][:5]
        for idx, entry in enumerate(recent_history):
            st.markdown(f"**{idx+1}. {entry['tab']}** | Model: `{entry['model']}` | Topic: *{entry['topic']}* | Time: `{entry['timestamp']}`")
            # Preview first 150 characters
            preview = entry["content"][:150] + "..." if len(entry["content"]) > 150 else entry["content"]
            st.code(preview, language="text")
            st.markdown("---")
    else:
        st.write("No generations in this session yet.")
