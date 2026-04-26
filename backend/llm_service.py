import os
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

class LLMService:
    def get_fitness_guidance(self, user_profile, activity_logs, chat_history):
        """
        Generates personalized fitness coaching with automatic model failover and fresh API connection.
        """
        # 1. Reload Environment (local .env or Streamlit Cloud secrets)
        load_dotenv(override=True)
        api_key = os.getenv("GEMINI_API_KEY")
        primary_model = os.getenv("LLM_MODEL", "gemini-2.5-flash")

        # Fallback: Read from Streamlit secrets (used in Streamlit Cloud deployment)
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("GEMINI_API_KEY", None)
                primary_model = st.secrets.get("LLM_MODEL", "gemini-2.5-flash")
            except Exception:
                pass
        
        if not api_key:
            return "API Key missing. Please configure GEMINI_API_KEY in your .env file."

        # Initialize fresh client
        try:
            client = genai.Client(api_key=api_key)
        except Exception as e:
            return f"Failed to initialize AI Client: {str(e)}"

        # 2. Format Context & Instructions
        history_summary = activity_logs.tail(10).to_string() if not activity_logs.empty else "No activities logged yet."
        system_instruction = f"""
        ROLE: You are 'Vitality AI', a professional fitness coach.
        USER: Name: {user_profile.get('name', 'User')}, Age: {user_profile.get('age', '25')}, Goal: {user_profile.get('goal', 'Stay Active')}.
        RECENT WORKOUTS: {history_summary}
        
        STRICT SAFETY:
        - NEVER give medical advice.
        - Refuse extreme or dangerous diet/exercise requests.
        - Recommend doctors for pain/injury.
        
        PERSONALITY:
        - Conversational, encouraging, and data-driven.
        - Refer to their recent workouts often.
        """

        # 3. Model Failover Logic
        if not primary_model.startswith("models/"):
            primary_model = f"models/{primary_model}"

        models_to_try = [
            primary_model, 
            "models/gemini-2.5-flash",           # Confirmed working
            "models/gemini-3.1-flash-lite-preview", # Confirmed working
            "models/gemini-2.0-flash",
            "models/gemini-flash-lite-latest"
        ]
        models_to_try = list(dict.fromkeys(models_to_try))

        errors = []
        for model_to_use in models_to_try:
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    contents = []
                    for msg in chat_history:
                        role = "user" if msg["role"] == "user" else "model"
                        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

                    response = client.models.generate_content(
                        model=model_to_use,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7
                        )
                    )
                    return response.text
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg:
                        if attempt < max_retries - 1:
                            time.sleep(2)
                            continue
                    errors.append(f"{model_to_use}: {error_msg}")
                    break 
        
        return f"All models failed. Last errors: \n" + "\n".join(errors[-2:])

# Singleton instance
llm_service = LLMService()
