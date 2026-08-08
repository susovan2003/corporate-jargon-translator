import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables
load_dotenv(encoding="utf-8")
nvidia_api_key = os.getenv("NVIDIA_API_KEY")

# 2. Configure Streamlit Page
st.set_page_config(page_title="Corporate Jargon Translator", page_icon="💼")

st.title("💼 Corporate Jargon to Plain English Translator")
st.write("Paste confusing emails, legal disclaimers, or corporate buzzwords to see what they *really* mean!")

# 3. User Inputs
user_text = st.text_area(
    "Paste Corporate Jargon Here:",
    placeholder="e.g., Let's circle back on this offline to leverage our bandwidth...",
    height=150
)

tone = st.selectbox(
    "Select Translation Tone:",
    ["Honest/Direct", "Friendly & Simple", "Sarcastic & Funny"]
)

# 4. Translation Logic
if st.button("Translate to Plain English 🚀"):
    if not nvidia_api_key:
        st.error("NVIDIA_API_KEY not found! Please check your .env file.")
    elif not user_text.strip():
        st.warning("Please paste some text to translate first!")
    else:
        try:
            # Initialize OpenAI client with NVIDIA base URL and explicit timeout
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=nvidia_api_key,
                timeout=20.0  # Prevents hanging indefinitely (20-second timeout)
            )

            prompt = f"""
            You are an expert translator specializing in converting confusing corporate jargon, tech buzzwords, and office speak into plain, clear English.

            Task: Translate the following text into plain English using a {tone} tone.
            Rules:
            1. Keep it clear and concise.
            2. If 'Honest/Direct', cut straight to the point.
            3. If 'Sarcastic & Funny', highlight the ridiculousness of the corporate speak humorously.
            4. Provide the translation clearly without extra meta explanations.

            Corporate Text:
            "{user_text}"
            """

            with st.spinner("Decoding corporate speak via NVIDIA AI..."):
                response = client.chat.completions.create(
                    model="meta/llama-3.1-8b-instruct",  # Faster lightweight model for rapid testing
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=500,
                )

                translation = response.choices[0].message.content

                st.markdown("---")
                st.subheader(f"🗣️ Translation ({tone} Mode):")
                st.info(translation)

        except Exception as e:
            st.error(f"API Error or Timeout: {e}")