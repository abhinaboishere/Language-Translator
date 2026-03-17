import streamlit as st
import google.generativeai as genai
import os

# 🔑 Set your API key
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Detect available models
models = genai.list_models()
available_model = None
for m in models:
    if "generateContent" in m.supported_generation_methods:
        available_model = m.name
        break

if not available_model:
    st.error("No supported Gemini models found for your API key.")
else:
    model = genai.GenerativeModel(model_name=available_model)

    def language_translate(user_txt, source_lang, target_lang):
        prompt = f"""
        Translate the following text from {source_lang} to {target_lang}:

        {user_txt}

        Please don't add extra text, only translate the text.
        """
        response = model.generate_content(prompt)
        return getattr(response, "text", "Translation failed!")

    # UI
    st.title("🌐 Language Translation with GenAI")
    user_txt = st.text_area("Enter Your Text :")

    selected_lang = [
        "English", "Spanish", "French", "German", "Italian", "Portuguese",
        "Russian", "Chinese (Simplified)", "Chinese (Traditional)", "Japanese",
        "Korean", "Arabic", "Hindi", "Bengali", "Urdu", "Turkish",
        "Persian (Farsi)", "Thai", "Vietnamese", "Indonesian"
    ]
    source_lang = st.selectbox("Choose Source Language", selected_lang)
    target_lang = st.selectbox("Choose Target Language", selected_lang)

    if st.button("Translate"):
        if user_txt.strip():
            translation = language_translate(user_txt, source_lang, target_lang)
            st.subheader("Translated Text :")
            st.write(translation)
        else:
            st.warning("⚠️ Please enter text to translate")
