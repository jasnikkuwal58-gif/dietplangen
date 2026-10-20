
# 🥗 AI Diet Plan Generator

A simple AI-powered web app that generates personalized diet plans based on user physical and lifestyle data.

🚀 **Live Demo**: [Hugging Face Space](https://dietplangenjaspreet.streamlit.app/)

---

## 📌 Features

* Generates diet plans tailored to individual physical and lifestyle stats
* Uses **Gemma 4 26B** via OpenRouter for natural language generation
* Lightweight and intuitive frontend with **Gradio**
* Seamlessly integrated with **LangChain** for API calls

---

## 🧠 Tech Stack

| Layer     | Technology                                                |
| --------- | --------------------------------------------------------- |
| Frontend  | [Streamlit](https://dietplangenjaspreet.streamlit.app/) (using `app` for layout) |
| Backend   | [LangChain](https://www.langchain.com/) for calling LLM   |
| LLM Model | Gemma 4 26B (`google/gemma-4-26b-a4b-it:free`) via OpenRouter |
| Hosting   | [Hugging Face Spaces](https://huggingface.co/spaces)      |

---

## 📁 Project Structure

```bash
diet_plan/
├── app.py           # Basic implementation to test functionality
├── README.md        # You're here!
```

---

## 🔧 Setup Instructions


1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenRouter API key**

   Create a `.env` (or `.ENV`) file in the project root:

   ```bash
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

3. **Run the app**

   ```bash
   python streamlit run app.py
   ```

---

## 📋 Notes

* `app.py` is a minimal version to ensure the pipeline works end-to-end

---

## 🤖 Model Info

* **Model**: `google/gemma-4-26b-a4b-it:free` (Gemma 4 26B)
* **Accessed via**: OpenRouter (`https://openrouter.ai/api/v1`) through LangChain `ChatOpenAI`
* **Purpose**: Generate coherent and customized diet plans

---


## 📬 Contact

Feel free to reach out for suggestions or collaborations!

---
