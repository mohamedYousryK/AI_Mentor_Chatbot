# 🤖 AI Mentor Chatbot (Module-Enforced Learning Assistant)

An interactive **AI-powered mentor chatbot** built with **Streamlit, LangChain, and Hugging Face LLMs** that provides **strict, domain-specific mentorship**.  
The system enforces **hard module boundaries** to ensure focused, distraction-free learning with a mentor persona configurable by industry experience.

---

## ✨ Features

- 🎯 **Strict Module Enforcement**  
  Answers are generated **only** for the selected module. Out-of-scope questions are explicitly refused.

- 🧑‍🏫 **Experience-Based Mentorship**  
  Responses adapt dynamically based on selected **years of industry experience**.

- 🔁 **Dynamic LLM Routing**  
  Automatically selects the best Hugging Face model for each domain:
  - Python, EDA → DeepSeek
  - SQL, Power BI → LLaMA
  - Machine Learning, Deep Learning → Qwen
  - Generative AI, Agentic AI → MiMo

- 💬 **Persistent Chat Memory**  
  Maintains conversation context per module and resets automatically when the module changes.

- 🎨 **Modern Chat UI**  
  Clean, ChatGPT-style interface built using custom **HTML + CSS** inside Streamlit.

- 📥 **Chat History Export**  
  Download complete conversations as a `.txt` file.

---

## 📚 Supported Modules

- Python  
- SQL  
- Power BI  
- Exploratory Data Analysis (EDA)  
- Machine Learning  
- Deep Learning  
- Generative AI  
- Agentic AI  

---

## 🛠 Tech Stack

- **Frontend**: Streamlit, HTML, CSS  
- **LLM Orchestration**: LangChain  
- **Models**: Hugging Face Inference API  
- **State Management**: Streamlit Session State  
- **Environment Management**: python-dotenv  

---

## 📂 Project Structure
├── app.py                 # Module & experience selection UI
├── pages/
│   └── mentor.py         # Mentor chatbot interface
├── .env                   # Hugging Face API token
├── requirements.txt
└── README.md

## 🚀 Use Cases

- Focused technical learning without topic drift
- Interview preparation with strict domain boundaries
- Mentor-style Q&A for beginners and intermediates
- Portfolio-ready AI application demonstrating LLM control

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ShubhamMohanty680/AI_Mentor_Chatbot.git
cd AI_Mentor_Chatbot
```
### 2️⃣ Create Virtual Environment
```bash
python -m venv mentor
mentor\Scripts\activate  # On MAC: source venv/bin/activate 
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Set Environment Variables (Create a .env file and add)
```bash
GOOGLE_API_KEY=your_gemini_api_key
```
### 5️⃣ Run the Application
```bash
streamlit run app.py
```

