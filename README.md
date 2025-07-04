# 📚 Research Automation

**AI-powered research assistant that fetches and analyzes ArXiv papers using workflow automation and Retrieval-Augmented Generation (RAG) techniques.**

---

## ✨ Features

* 🔍 **Search ArXiv**: Enter a query and research question to fetch relevant papers from ArXiv.
* 🤖 **AI-Powered Answers**: Uses Groq LLMs (LLaMA/Mixtral) to answer your research question based on the downloaded papers.
* 📄 **PDF Download & Processing**: Automatically downloads, validates, and processes PDFs.
* 🧠 **Vector Database**: Embeds and stores paper content for efficient retrieval.
* ⚡ **Modern Stack**: React frontend, Flask backend, LangChain, LangGraph, and ChromaDB.
* 🔑 **Customizable**: Choose number of papers, LLM model, and provide your own Groq API key.

---

## 📁 Project Structure

```
research-search-automation/
├── backend/
│   └── app.py
    └── Services.py
    └── requirements.txt             # Flask app
├── frontend/
│   ├── src/
        └── App.jsx
        └── Components
            └── ResearchSec.jsx
│   └── vite.config.js        # Vite configuration
├── public/
│   └── vite.svg              # Stack banner
├── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/research-search-automation.git
cd research-search-automation
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Install Backend Dependencies

```bash
cd ../backend
pip install flask flask-cors langchain langgraph langchain_groq chromadb feedparser requests
```

### 4. Run the Backend

```bash
python app.py
```

> The backend will start at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 5. Run the Frontend

```bash
cd ../frontend
npm run dev
```

> The frontend will start at: [http://localhost:5173](http://localhost:5173)

---

## 🧪 Usage

1. Open the frontend in your browser.
2. Enter your search query, research question, and Groq API key (get one from [console.groq.com](https://console.groq.com)).
3. Optionally adjust advanced settings (number of papers, model).
4. Click **Start Research**.
5. View the AI-generated answer and stats once the process completes.

---

## 🧰 Requirements

* Node.js (v18+ recommended)
* Python 3.8+
* Groq API Key

---

## 🛠️ Technologies Used

* **Frontend**: React, Vite, TailwindCSS, Lucide Icons
* **Backend**: Flask, Flask-CORS, LangChain, LangGraph, ChromaDB, HuggingFace Embeddings, Groq LLM
* **Other**: feedparser, requests

---

## 🧯 Troubleshooting

* **CORS errors**: Ensure the backend is running before starting the frontend.
* **Groq API errors**: Make sure your API key is valid and has sufficient quota.
* **PDF download issues**: Some ArXiv papers may not have accessible PDFs or may fail to download.


---

## 🙏 Acknowledgements

* [ArXiv](https://arxiv.org)
* [LangChain](https://www.langchain.com)
* [LangGraph](https://www.langchain.com)
* [Groq](https://www.groq.com)
* [ChromaDB](https://www.trychroma.com)
