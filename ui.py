# ui.py - Main Streamlit UI with AI integration
import streamlit as st
from datetime import datetime
import os
from ai_engine import AITerminalEngine
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="My Terminal", layout="wide")

# Initialize AI engine with Gemini API key
@st.cache_resource
def get_ai_engine():
    api_key = os.getenv("GEMINI_API_KEY")
  
    if not api_key:
        st.error("GEMINI_API_KEY environment variable not set")
        return None
    return AITerminalEngine(api_key=api_key)

ai_engine = get_ai_engine()

# --- CSS Styles ---
st.markdown("""
<style>
body {
    background-color: black;
    margin: 0;
    padding: 0;
}
.main { background-color: black; padding: 0; }
.stApp { background-color: black; }
.stTextInput { display: none !important; }
.header {
    color: #00ff99;
    border-bottom: 1px solid #00ff99;
    padding: 10px 20px;
    margin-bottom: 10px;
    font-family: monospace;
    font-size: 14px;
    background-color: #000;
}
.terminal {
    background-color: #000;
    color: #fff;
    font-family: monospace;
    padding: 20px;
    border: 1px solid #00ff99;
    border-radius: 5px;
    min-height: 70vh;
    overflow-y: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
    outline: none;
}
.prompt { 
    color: #00aaff; 
    display: inline; 
    font-weight: bold; 
}
.command { 
    color: #00ff99; 
    display: inline; 
}
.output { 
    color: #ffffff; 
    margin-top: 5px; 
    margin-bottom: 15px; 
}
.ai-output {
    color: #00ff99;
    margin-top: 5px;
    margin-bottom: 15px;
    font-style: italic;
}
.suggestion {
    color: #888888;
    display: inline;
    margin-left: 10px;
    font-style: italic;
}
.input-line { 
    display: flex; 
    align-items: center;
    flex-wrap: wrap;
}
.cursor {
    display: inline-block;
    background-color: #00ff99;
    width: 10px;
    height: 18px;
    animation: blink 1s step-start infinite;
    vertical-align: text-bottom;
    margin-left: 2px;
}
@keyframes blink { 
    50% { background-color: transparent; } 
}
.timestamp {
    color: #00ff99;
    text-align: right;
    font-size: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- Commands ---
commands = {
    "welcome": """Hi, I'm Neema Mwende, a Software & AI Engineer.

Welcome to my interactive 'AI powered' portfolio terminal!
Type 'help' to see available commands.""",
    "help": """Available commands:

about           - Learn about me
projects        - View my projects
skills          - See my technical skills
experience      - My work experience
contact         - How to reach me
education       - My educational background
certifications  - View my certifications
leadership      - Leadership and community involvement
clear           - Clear the terminal

Type any command to continue..""",
    "about": "I'm Neema Mwende, passionate about building intelligent systems and modern web apps.",
    "projects": """AI Portfolio Terminal - Interactive terminal-based portfolio
MyTech API Dashboard - Real-time data visualization platform
Trading Bot Platform - Automated trading system
Data Analysis Tool - Python-based analytics suite""",
    "skills": """Programming Languages: Python, JavaScript, Java, C++
Web Development: Streamlit, React, Next.js, FastAPI
AI/Machine Learning: TensorFlow, PyTorch, Scikit-learn
Cloud & DevOps: AWS, GCP, Docker, Kubernetes
Databases: PostgreSQL, MongoDB, Firebase""",
    "experience": """Software Engineer at Tech Corp (2022-Present)
- Led development of ML pipeline systems
- Built scalable microservices

AI Developer at StartupXYZ (2020-2022)
- Developed NLP models
- Deployed production AI systems

Research Assistant at University Lab (2019-2020)
- Computer Vision research""",
    "contact": """Email: markgatere@example.com
GitHub: github.com/markgatere
LinkedIn: linkedin.com/in/markgatere
Twitter: @markgatere""",
    "education": """BSc in Software Engineering - Strathmore University (2020)
Advanced Machine Learning Certificate - Coursera
Full Stack Development Bootcamp - TechAcademy""",
    "certifications": """AWS Certified Developer Associate
TensorFlow Developer Certificate
Azure AI Engineer Associate
Google Cloud Certified Associate Cloud Engineer""",
    "leadership": """Tech Lead at AI Club - Mentoring 50+ students
Mentor at Local Developer Community
Speaker at Tech Meetups
Open Source Contributor""",
}

# --- Session state ---
if "history" not in st.session_state:
    st.session_state.history = [("neema@portfolio:~$ ", "welcome", commands["welcome"], False)]
if "temp_command" not in st.session_state:
    st.session_state.temp_command = ""
if "use_ai" not in st.session_state:
    st.session_state.use_ai = True

# --- Header bar ---
st.markdown(
    '<div class="header">help | about | projects | skills | experience | contact | education | certifications | leadership | clear</div>',
    unsafe_allow_html=True
)

# --- Terminal render function ---
terminal_container = st.container()

def render_terminal():
    html = '<div class="terminal" id="terminal" tabindex="0">'
    for prompt, command, output, is_ai in st.session_state.history:
        html += f'<div><span class="prompt">{prompt}</span><span class="command">{command}</span></div>'
        if output:
            output_class = "ai-output" if is_ai else "output"
            html += f'<div class="{output_class}">{output}</div>'
    html += '<div class="input-line">'
    html += '<span class="prompt">gatere@portfolio:~$ </span>'
    html += '<span id="typed-text" class="command"></span>'
    html += '<span id="suggestion" class="suggestion"></span>'
    html += '<span class="cursor"></span>'
    html += '</div>'
    html += '</div>'
    terminal_container.markdown(html, unsafe_allow_html=True)

render_terminal()

# --- Hidden input field ---
command_input = st.text_input("terminal_input", key="terminal_input", label_visibility="collapsed")

# --- JS Typing System with AI Suggestions ---
st.markdown("""
<script>
(function() {
  window._typed = window._typed || '';
  window._suggestion = '';
  
  function updateDisplay() {
    const typedText = document.querySelector('#typed-text');
    const terminal = document.querySelector('#terminal');
    const suggestion = document.querySelector('#suggestion');
    
    if (typedText) typedText.textContent = window._typed;
    if (suggestion) suggestion.textContent = window._suggestion;
    if (terminal) terminal.scrollTop = terminal.scrollHeight;
  }
  
  function handleKey(e) {
    if (e.key === 'Enter') {
      const hiddenInput = document.querySelector('input[data-testid="stTextInput"]');
      if (hiddenInput && window._typed.trim() !== '') {
        hiddenInput.value = window._typed;
        hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
        hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
      }
      window._typed = '';
      window._suggestion = '';
    } else if (e.key === 'Backspace') {
      e.preventDefault();
      window._typed = window._typed.slice(0, -1);
      window._suggestion = '';
    } else if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
      window._typed += e.key;
    }
    updateDisplay();
  }
  
  if (!window._terminalKeyHandlerAttached) {
    document.addEventListener('keydown', handleKey);
    window._terminalKeyHandlerAttached = true;
  }
  
  const observer = new MutationObserver(updateDisplay);
  observer.observe(document.body, { childList: true, subtree: true });
  
  updateDisplay();
})();
</script>
""", unsafe_allow_html=True)

# --- Process command ---
if command_input and command_input.strip():
    cmd = command_input.strip().lower()
    
    if cmd != st.session_state.temp_command:
        st.session_state.temp_command = cmd

        if cmd == "clear":
            st.session_state.history = []
        elif cmd in commands:
            st.session_state.history.append(("neema@portfolio:~$ ", cmd, commands[cmd], False))
        else:
            # Use AI for strict data extraction from resume
            if ai_engine:
                ai_response = ""
                try:
                    for chunk in ai_engine.validate_and_extract(cmd):
                        ai_response += chunk
                    st.session_state.history.append(("neema@portfolio:~$ ", cmd, ai_response, True))
                except Exception as e:
                    st.session_state.history.append(
                        ("neema@portfolio:~$ ", cmd, f"Error: {str(e)}. Type 'help' for available commands.", False)
                    )
            else:
                st.session_state.history.append(
                    ("neema@portfolio:~$ ", cmd, f"Command not found: '{cmd}'. Type 'help' for available commands.", False)
                )

        st.rerun()

# --- Timestamp ---
now = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
st.markdown(f'<div class="timestamp">{now}</div>', unsafe_allow_html=True)