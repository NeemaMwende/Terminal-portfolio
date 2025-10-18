# 🖥️ AI-Powered Terminal Portfolio

An interactive, terminal-style portfolio website built with Streamlit, featuring AI-powered responses using RAG (Retrieval-Augmented Generation) and Google's Gemini AI.

## ✨ Features

- 🎨 **Retro Terminal UI** - Authentic terminal experience with typing animations
- 🤖 **AI-Powered Responses** - Intelligent answers using RAG + Gemini 2.5
- ⚡ **Fast Loading** - Optimized with persistent ChromaDB storage
- 📄 **PDF Resume Integration** - Automatically extracts info from your resume
- 💾 **Smart Caching** - Embeddings cached for instant subsequent loads
- 🎯 **Interactive Commands** - Navigate through skills, projects, experience, and more

## 🎥 Demo

```bash
neema@portfolio:~$ welcome
Hi, I'm Neema Mwende, a Software & AI Engineer.

Welcome to my interactive 'AI powered' portfolio terminal!
Type 'help' to see available commands.

neema@portfolio:~$ help
Available commands:
  about           - Learn about me
  projects        - View my projects
  skills          - See my technical skills
  experience      - My work experience
  contact         - How to reach me
  education       - My educational background
  certifications  - View my certifications
  leadership      - Leadership and community involvement
  clear           - Clear the terminal
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+** (or Python 3.8+)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### API Keys Required

You'll need the following API keys:

1. **OpenAI API Key** - For embeddings ([Get it here](https://platform.openai.com/api-keys))
2. **Google Gemini API Key** - For AI responses ([Get it here](https://makersuite.google.com/app/apikey))

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/terminal-portfolio.git
cd terminal-portfolio
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**

```txt
streamlit>=1.28.0
python-dotenv>=1.0.0
google-generativeai>=0.3.0
chromadb>=0.4.0
langchain>=0.1.0
langchain-community>=0.0.10
langchain-openai>=0.0.5
openai>=1.0.0
pypdf>=3.17.0
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add your API keys:

```env
# OpenAI API Key (for embeddings)
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini API Key (for AI responses)
GEMINI_API_KEY=your_gemini_api_key_here

# Resume PDF path (optional, defaults to resume.pdf)
RESUME_PDF_PATH=resume.pdf

# Terminal customization (optional)
TERMINAL_PROMPT=neema@portfolio:~$
TERMINAL_COLOR=#00ff99
PROMPT_COLOR=#00aaff
```

### 5. Add Your Resume

Place your resume PDF in the project root:

```bash
# Make sure your resume is named resume.pdf
# Or update RESUME_PDF_PATH in .env
cp /path/to/your/resume.pdf ./resume.pdf
```

## 🎮 Usage

### Run the Application

```bash
streamlit run ui.py
```

The terminal will open in your browser at `http://localhost:8501`

### First Run (Slower - Embedding)

On the first run, the application will:

1. Load your resume PDF
2. Split it into chunks
3. Generate embeddings using OpenAI
4. Store them in ChromaDB

**Expected time:** 15-30 seconds

```
🚀 Initializing MCP Server...
📄 Loading and embedding resume (first time or updated)...
🔄 Generating embeddings...
💾 Storing in database...
✓ Resume embedded and stored (5 chunks)
✓ MCP Server cached and ready!
```

### Subsequent Runs (Fast - Cached)

After the first run, embeddings are cached:

**Expected time:** 1-2 seconds ⚡

```
✓ Resume already loaded (5 chunks) - skipping embedding
✓ MCP Server cached and ready!
```

## 📁 Project Structure

```
terminal-portfolio/
├── ui.py                   # Main Streamlit UI with terminal interface
├── mcp_server.py           # MCP server handling commands
├── rag_engine.py           # RAG engine with ChromaDB
├── tools.py                # Command handlers and AI tools
├── ai_engine.py            # AI-powered command suggestions
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── resume.pdf              # Your resume PDF (add this)
├── chroma_db/              # ChromaDB persistent storage (auto-created)
│   └── ...
├── README.md               # This file
└── .gitignore              # Git ignore file
```

## 🎨 Available Commands

| Command          | Description                          |
| ---------------- | ------------------------------------ |
| `welcome`        | Display welcome message              |
| `help`           | Show all available commands          |
| `about`          | Learn about your background          |
| `skills`         | View technical skills                |
| `experience`     | Display work experience              |
| `projects`       | Show your projects                   |
| `education`      | Educational background               |
| `certifications` | List certifications                  |
| `leadership`     | Leadership and community involvement |
| `contact`        | Contact information                  |
| `clear`          | Clear the terminal screen            |

You can also ask **custom questions** like:

- "What programming languages do you know?"
- "Tell me about your AI projects"
- "What's your most recent job?"

## 🔧 Troubleshooting

### Issue: "OPENAI_API_KEY not found"

**Solution:** Make sure `.env` file exists and contains valid API keys:

```bash
cat .env  # Check if file exists and has keys
```

## 👨‍💻 Author

**Neema Mwende**

- Email: neemamwende009@gmail.com
- GitHub: [@neemamwende](https://github.com/neemamwende)
- LinkedIn: [Neema Mwende](https://linkedin.com/in/neemamwende)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [Google Gemini](https://ai.google.dev/)
- Embeddings by [OpenAI](https://openai.com/)
- Vector storage by [ChromaDB](https://www.trychroma.com/)
- RAG framework by [LangChain](https://langchain.com/)

## 📊 Performance

- **First Load:** 15-30 seconds (embedding generation)
- **Subsequent Loads:** 1-2 seconds (cached)
- **Response Time:** < 1 second (cached queries)
- **Memory Usage:** ~200-300 MB
- **Storage:** ~50 MB (ChromaDB cache)
