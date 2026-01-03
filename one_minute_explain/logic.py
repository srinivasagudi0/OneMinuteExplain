# logic.py
from __future__ import annotations
from typing import Tuple, List
import re

# ================== CONFIG ==================
TARGET_WORDS = 140
HARD_MAX_WORDS = 150
MIN_WORDS = 25  # prevent useless outputs
DEFAULT_MODEL = "gpt-3.5-turbo"

OPENAI_API_KEY = ""  # Set your OpenAI API key here
# ============================================


# ---------- UTIL ----------
def count_words(text: str) -> int:
    return len(text.split())


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def is_too_short_or_garbage(text: str) -> bool:
    lowered = text.lower()
    if count_words(text) < MIN_WORDS:
        return True
    if "may refer to" in lowered:
        return True
    return False


# ---------- OPENAI ----------
def generate_with_openai(topic: str, level: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)

    # Handle very short / ambiguous topics explicitly
    if len(topic.split()) <= 2:
        prompt = f"""
Define "{topic}" for a {level.lower()} learner.

Rules:
- Plain English
- Explain what it is, why it matters, and one example
- Stay under {TARGET_WORDS} words
- Do NOT say "may refer to"
"""
    else:
        prompt = f"""
Explain "{topic}" for a {level.lower()} learner.

Rules:
- Plain English
- Max {HARD_MAX_WORDS} words
- No fluff
"""

    res = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return normalize(res.choices[0].message.content)


# ---------- WIKIPEDIA ----------
def adapt_text_for_level(text: str, level: str) -> str:
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    if not sentences:
        return text

    if level == "Beginner":
        return sentences[0] + ". In simple terms, this explains the basic idea."

    if level == "Intermediate":
        return ". ".join(sentences[:3]) + "."

    if level == "Advanced":
        return ". ".join(sentences[:5]) + "."

    return text


def generate_with_wikipedia(topic: str, level: str) -> str:
    import wikipediaapi

    wiki = wikipediaapi.Wikipedia(
        language="en",
        user_agent="OneMinuteExplain/1.0 (educational)",
    )

    candidates = [
        topic,
        f"{topic} (technology)",
        f"{topic} (concept)",
        f"{topic} (greeting)",
    ]

    for cand in candidates:
        page = wiki.page(cand)
        if not page.exists():
            continue

        summary = normalize(page.summary)
        if is_too_short_or_garbage(summary):
            continue

        summary = adapt_text_for_level(summary, level)

        if count_words(summary) > TARGET_WORDS:
            summary = " ".join(summary.split()[:TARGET_WORDS]) + "…"

        return summary

    return ""


# ---------- SMART FALLBACK (NEVER FAILS) ----------
def build_definition_fallback(topic: str, level: str) -> str:
    return normalize(
        f"{topic} is a concept explained for a {level.lower()} learner. "
        f"It focuses on the main idea, why it matters, and how people commonly use it. "
        f"The goal is to understand {topic} quickly without unnecessary details. "
        f"A simple way to recognize {topic} is to look at what problem it solves "
        f"and how it changes the outcome of a task."
    )


# ---------- FINAL GENERATOR ----------
def generate_explanation(topic: str, level: str) -> Tuple[str, bool, str]:
    enforced = False

    # 1️⃣ OpenAI (primary)
    try:
        text = generate_with_openai(topic, level)
        source = "openai"
        if is_too_short_or_garbage(text):
            raise RuntimeError("OpenAI output too weak")
    except Exception:
        # 2️⃣ Wikipedia
        text = generate_with_wikipedia(topic, level)
        source = "wikipedia"

        if not text:
            # 3️⃣ Guaranteed fallback
            text = build_definition_fallback(topic, level)
            source = "fallback"

    if count_words(text) > HARD_MAX_WORDS:
        text = " ".join(text.split()[:HARD_MAX_WORDS])
        enforced = True

    return text, enforced, source


# ---------- INTELLIGENT TAKEAWAYS + EXAMPLE ----------
def build_takeaways_and_example(topic: str, explanation: str, source: str):
    topic_clean = topic.strip()

    takeaways: List[str] = []

    # AI-derived takeaways
    if source == "openai":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)

            prompt = f"""
From the explanation below, extract exactly 3 clear takeaways.
Each must be one sentence, specific, and useful.

Explanation:
{explanation}
"""

            res = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )

            raw = res.choices[0].message.content.split("\n")
            takeaways = [t.lstrip("-• ").strip() for t in raw if t.strip()][:3]
        except Exception:
            takeaways = []

    if len(takeaways) < 3:
        sentences = [s.strip() for s in explanation.split(".") if s.strip()]
        takeaways = [
            sentences[0] + ".",
            f"{topic_clean} is easier when you focus on the core idea.",
            "Short explanations help you act without confusion.",
        ]

    # Real-world example
    if source == "openai":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)

            prompt = f"""
Give ONE realistic real-world example for learning "{topic_clean}".
2–3 sentences. Specific situation. Plain English.
"""

            res = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )

            example = normalize(res.choices[0].message.content)
        except Exception:
            example = ""

    else:
        example = ""

    if not example:
        example = (
            f"Example: You encounter {topic_clean} while starting a task. "
            f"Instead of reading long material, you use a one-minute explanation "
            f"to understand the idea and begin confidently."
        )

    return takeaways, example
