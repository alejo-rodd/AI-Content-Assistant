import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv('GEMINI_API_KEY')

client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# --- Streamlit Interface ---
st.title("🚀 Social Media Content Generator")
st.markdown("Instantly create posts, tweets, and slogans with AI.")

with st.sidebar:
    st.header("Settings")
    topic = st.text_input("Topic / Product:", placeholder="E.g. New smartphone launch")
    
    content_type = st.selectbox(
        "Content Type:",
        ["Tweet", "Instagram/Facebook Post", "Slogan", "Product Description", "Short Video Script Idea"]
    )
    
    tone = st.selectbox(
        "Tone:",
        ["Enthusiastic", "Informative", "Funny", "Persuasive", "Formal", "Inspirational"]
    )
    
    audience = st.text_input("Target Audience (optional):", placeholder="E.g. Young students, first-time mothers")
    
    keywords = st.text_area("Keywords to Include (comma separated, optional):", placeholder="E.g. innovation, long-lasting battery, camera")
    
    cta = st.text_input("Call to Action (CTA, optional):", placeholder="E.g. Visit our website, Buy now, Follow us")

if st.button("Generate Content"):
    if not topic:
        st.warning("Please enter a topic or product to generate content.")
    else:
        st.info("Generating content, this may take a moment...")
        
        # Build the prompt dynamically
        messages = [
            {"role": "system", "content": f"You are an expert in digital marketing and content creation. Generate high-quality and engaging content. The tone should be {tone}."}
        ]
        
        user_prompt = f"Generate {content_type} about '{topic}'."
        if audience:
            user_prompt += f" The target audience is '{audience}'."
        if keywords:
            user_prompt += f" Make sure to include the following keywords: {keywords}."
        if cta:
            user_prompt += f" The call to action is '{cta}'."
        
        # Instruction to use tools
        if "hashtag" in content_type.lower() or "instagram" in content_type.lower() or "tweet" in content_type.lower():
            user_prompt += " Use the tool to get relevant hashtags if applicable."

        messages.append({"role": "user", "content": user_prompt})

        try:
            # Call to OpenAI API with tools
            response = client.chat.completions.create(
                model="gemini-2.0-flash-lite", # Or your preferred model
                messages=messages,
                reasoning_effort="none",
            )
            
            response_message = response.choices[0].message
            st.subheader("Generated Content:")
            st.write(response_message.content)

        except Exception as e:
            st.error(f"An error occurred while generating the content: {e}")
            st.warning("Make sure your OpenAI API Key is valid and you have credits.")