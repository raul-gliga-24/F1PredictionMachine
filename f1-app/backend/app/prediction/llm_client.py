from google import genai
from app.config import settings
import json

client = genai.Client(api_key=settings.gemini_api_key)

def call_llm(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the text response.
    This is the only function the rest of the app calls —
    swap the internals here if you ever change provider.
    """
    # Use gemini-2.5-flash as requested, but on the new SDK
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            temperature=0.3,   # low = more consistent predictions
            max_output_tokens=8192,
        )
    )
    return response.text

def call_llm_with_context(context: dict, system_prompt: str) -> str:
    """
    Convenience wrapper that injects a JSON context object
    into the prompt. Used by race_predictor.py and championship_sim.py
    """
    full_prompt = f"{system_prompt}\n\nContext data:\n{json.dumps(context, indent=2)}"
    return call_llm(full_prompt)