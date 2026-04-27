# Research Paper Assistant

A Streamlit app that lets you paste research paper URLs and ask questions about them using LLM-powered Q&A.

## Features
- Load up to 3 research paper URLs
- Splits and embeds content using HuggingFace sentence transformers
- Stores vectors locally using FAISS
- Answers questions using Groq (LLaMA 3.1)

## 🛠️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
Copy `.env.example` to `.env` and add your Groq API key:
```bash
cp .env.example .env
```
Then edit `.env`:
```
GROQ_API_KEY=your_actual_key_here
```
Get a free key at: https://console.groq.com

### 5. Run the app
```bash
streamlit run main.py
```

## 📁 Project Structure
```
├── main.py               # Main Streamlit app
├── requirements.txt      # Python dependencies
├── .env.example          # Template for environment variables
├── .gitignore            # Files excluded from Git
└── README.md             # This file
```

## ⚠️ Important
Never commit your `.env` file. It's already in `.gitignore`.
