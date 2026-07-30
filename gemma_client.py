import json
import os
from io import BytesIO
import time
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

DEFAULT_MODEL = "gemma-4-26b-a4b-it"

PROMPT = """You are a disaster response analyst reviewing aerial drone imagery.
Return ONLY a JSON object in exactly this shape:
{"severity_score": <integer 1-10>, "hazard_summary": "<one short sentence>"}
Severity 1 means no visible disaster impact. Severity 10 means extreme danger,
major flooding, blocked access, trapped people, collapsed structures, or similar
life-safety risk."""


def _secret(name: str) -> str | None:
    try:
        return st.secrets.get(name)
    except Exception:
        return None


def _get_client() -> genai.Client:
    api_key = _secret("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing GEMINI_API_KEY. Add it to .streamlit/secrets.toml or your environment."
        )
    return genai.Client(api_key=api_key)


def _model_name() -> str:
    return _secret("GEMMA_MODEL") or os.environ.get("GEMMA_MODEL") or DEFAULT_MODEL


def _image_mime_type(image_bytes: bytes) -> str:
    with Image.open(BytesIO(image_bytes)) as image:
        image.verify()
        fmt = (image.format or "").upper()

    if fmt == "JPEG":
        return "image/jpeg"
    if fmt == "PNG":
        return "image/png"
    raise ValueError(f"Unsupported image format: {fmt or 'unknown'}")

def analyze_image(image_bytes: bytes) -> dict:
    client = _get_client()
    response = client.models.generate_content(
        model=_model_name(),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=_image_mime_type(image_bytes)),
            PROMPT,
        ],
    )
    # Strip potential markdown fences defensive fallback
    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
        if raw_text.startswith("json"):
            raw_text = raw_text[4:].strip()
            
    result = json.loads(raw_text)
    return {
        "severity_score": int(result["severity_score"]),
        "hazard_summary": str(result["hazard_summary"]),
    }

def analyze_image_safe(image_bytes: bytes, retries=2) -> dict:
    for attempt in range(retries + 1):
        try:
            return analyze_image(image_bytes)
        except Exception as e:
            if "429" in str(e) and attempt < retries:
                time.sleep(2 ** attempt)
                continue
            return {
                "severity_score": -1,
                "hazard_summary": "Analysis unavailable",
                "error": str(e),
            }
