# ⏱️ OneMinuteExplain

OneMinuteExplain provides a **clear, on-script explanation of any topic** in a **~60-second read**, adapted to the user’s learning level.  
No fluff. No overload.

---

## 🚀 What It Does

Users:
1. Enter a topic  
2. Choose an audience level (Beginner, Intermediate, Advanced)  
3. Receive a focused explanation that fits within one minute  

The system enforces a strict word limit to keep explanations clear and usable.

---

## 🧠 How It Works

The project separates **knowledge retrieval** from **presentation control**:

- **Primary intelligence:** OpenAI API (when available)
- **Public fallback:** Wikipedia API (no authentication required)
- **Final fallback:** Definition-based explanation (never fails)

Explanations are:
- Adapted to the selected audience level
- Checked for low-quality or ambiguous outputs
- Forced to stay within a ~60-second reading limit

This ensures reliability even when external services are unavailable.

---

## 🛠️ Built With

- **Language:** Python  
- **Framework:** Streamlit  
- **APIs:** OpenAI API (optional), Wikipedia API  
- **Platform:** Web application (Streamlit)

---

## ▶️ How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/one-minute-explain.git
   cd one-minute-explain
   ```
Install dependencies:

pip install -r requirements.txt
Run the app:


streamlit run main.py
(Optional) To enable AI:


export OPENAI_API_KEY="your_api_key_here"
The app works with or without an API key.

⚠️ Edge Case Handling
Very short or ambiguous topics (e.g., “hi”) are handled safely

Wikipedia disambiguation pages are detected and avoided

The app never crashes or returns unusable output

📚 What This Project Demonstrates
The value of hard constraints in design

Responsible and transparent use of AI

Graceful fallbacks for reliability

Clear separation between data retrieval and presentation

