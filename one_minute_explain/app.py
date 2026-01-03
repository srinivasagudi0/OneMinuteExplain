# main.py
import streamlit as st
from logic import (
    generate_explanation,
    build_takeaways_and_example,
    TARGET_WORDS,
)

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="OneMinuteExplain",
    page_icon="⏱️",
    layout="centered",
)

st.title("⏱️ OneMinuteExplain")
st.write(
    "Get a **clear, on-script explanation** of any topic in a "
    "**~60-second read**. No fluff. No overload."
)

st.divider()

# ---------- INPUTS ----------
topic = st.text_input(
    "Topic",
    placeholder="e.g. APIs, Recursion, Photosynthesis, GitHub",
)

level = st.selectbox(
    "Audience level",
    ["Beginner", "Intermediate", "Advanced"],
)

st.caption(f"Target length: ~{TARGET_WORDS} words")

# ---------- ACTION ----------
if st.button("Explain in 1 Minute"):
    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("Generating explanation..."):
        text, enforced, source = generate_explanation(topic.strip(), level)

    word_count = len(text.split())
    progress = min(word_count / TARGET_WORDS, 1.0)

    # ---------- TRUST SIGNALS ----------
    if enforced:
        st.success("✅ Constraint enforced — kept it on-script.")
    else:
        st.info("✅ Within the 1-minute constraint.")

    st.progress(progress)
    st.caption(
        f"🕒 ~60-second read • **{word_count} words** • "
        f"Source: **{source}**"
    )

    st.divider()

    # ---------- EXPLANATION ----------
    st.subheader("📖 Explanation")
    st.write(text)

    # ---------- INTELLIGENT TAKEAWAYS ----------
    takeaways, example = build_takeaways_and_example(
        topic=topic,
        explanation=text,
        source=source,
    )

    st.subheader("✅ Key Takeaways (What You Should Remember)")
    for t in takeaways:
        st.markdown(f"- {t}")

    st.divider()

    # ---------- REAL-WORLD EXAMPLE ----------
    st.subheader("🌍 Real-World Example")
    st.write(example)

# ---------- FOOTER ----------
st.divider()
st.caption(
    "OneMinuteExplain enforces clarity through time constraints. "
    "AI is optional; public sources are used automatically when needed."
)
