import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.gemini_api_key)

# Use gemini-1.5-pro — best reasoning model, good for long JSON context
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.3,   # low = more consistent predictions
        "max_output_tokens": 2048,
    }
)

def call_llm(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the text response.
    This is the only function the rest of the app calls —
    swap the internals here if you ever change provider.
    """
    response = model.generate_content(prompt)
    return response.text


def call_llm_with_context(system_prompt: str, context: dict) -> str:
    """
    Convenience wrapper that injects a JSON context object
    into the prompt. Used by race_predictor.py and championship_sim.py
    """
    import json
    full_prompt = f"{system_prompt}\n\nContext data:\n{json.dumps(context, indent=2)}"
    return call_llm(full_prompt)