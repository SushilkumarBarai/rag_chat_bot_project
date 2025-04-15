## 🧾 Project Description

This application is designed for HR teams, recruiters, and hiring managers to **automate the candidate shortlisting process** by leveraging advanced AI capabilities.

It enables HR professionals to upload a CSV file containing multiple resumes, and then **query natural language questions** such as:

- "Who has more than 5 years of experience in Python and Django?"
- "Find candidates with expertise in data analysis and Power BI."
- "List people who have led teams or worked in project management."

Under the hood, the system uses:

- **RAG (Retrieval-Augmented Generation)**: Retrieves the most relevant parts of resume documents using similarity search, and then generates human-readable answers.
- **Chroma Vector Store**: Stores embeddings of resume data to enable efficient semantic search.
- **LangChain**: Manages document chunking, embedding, and conversation prompt handling.
- **LLaMA 2 Chat** via [Ollama](https://ollama.com/): Performs the final reasoning to summarize and return the top 3 most suitable candidates based on user queries.

The system is built for **speed, flexibility, and ease of use**, allowing HR professionals to rapidly filter and identify top candidates without manually reading every resume. The summaries returned are concise, consistent, and aligned with the search intent.

This tool is especially helpful for:
- Rapid hiring cycles
- Filtering large volumes of resumes
- Internal recruitment or vendor evaluations
- Tech or domain-specific hiring use cases



---

## 🧠 How it Works

- Embeds candidate resumes using `FastEmbed` and stores them in a Chroma vector store.
- Uses **LangChain** to perform similarity search.
- Sends retrieved context and user query to the **LLaMA 2 chat model** running via `ollama`.
- Displays HR-friendly summaries for top matching candidates.

---

## 🛠️ Setup Instructions

### 1. 🔧 Clone this repository
```bash
git clone https://github.com/your-username/hr-resume-bot.git
cd hr-resume-bot
```

### 2. 🐍 Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# OR
.\venv\Scripts\activate         # Windows
```

### 3. 📦 Install Python dependencies
```bash
pip install -r requirements.txt
```

---

## 🤖 Install Ollama & LLaMA 2

### 🧱 Step 1: Install Ollama
Follow instructions from the official site: https://ollama.com/download  
Or directly from terminal:

**macOS (Homebrew):**
```bash
brew install ollama
```

**Windows (via executable):**
- Download and run installer from: https://ollama.com/download

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

### 🧠 Step 2: Pull LLaMA 2 Chat Model
```bash
ollama pull llama2:chat
```

Make sure it’s running on: `http://localhost:11434`

---

## ▶️ Run the App

Once everything is set up:

```bash
streamlit run app.py
```

> Replace `app.py` with your Streamlit file name if different.

---

## 📁 Resume File Format (CSV)

Make sure your CSV has at least the following columns:
- `CandidateID`: A unique ID for each candidate
- `Resume`: The complete resume content (in plain text)

Example:
```csv
CandidateID,Resume
101,"Experienced Python developer with 6 years of experience..."
102,"Data Analyst with 3 years in Power BI and SQL..."
```

---

## 💬 Sample Query

> "Who has experience in Django and React?"
>  
> "List candidates with more than 7 years of experience in project management."

---

## ✅ Output Format

```
CandidateID: 103  
Summary: 5 years of experience in SQL and Power BI. Built dashboards and reports for retail clients.

CandidateID: 109  
Summary: Data analyst with strong SQL skills and experience using Power BI for financial reporting.
```

---

## 🧹 Clear Memory or Reset Chat

- Upload new CSV to reset the memory
- Input field will be cleared after each response
- Use `clear()` method in code if needed programmatically

---

## 📃 License

This project is under the MIT License.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Ollama](https://ollama.com/)
- [LangChain](https://www.langchain.com/)
- [LLaMA 2](https://ai.meta.com/llama/)
