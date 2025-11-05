"""
UI - Standalone Streamlit terminal interface with typing effects
Author: Neema Mwende
"""

import streamlit as st
from datetime import datetime
import time

# Uncomment these when RAG is ready
# from rag_engine import ResumeRAG
# import os
# from dotenv import load_dotenv
# load_dotenv()

# RESUME_PATH = "resume.pdf" 
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Neema Mwende - AI Terminal", layout="wide", initial_sidebar_state="collapsed")

# --- Initialize RAG Engine (commented out for now) ---
# @st.cache_resource
# def load_rag_engine():
#     """Load RAG engine (cached to avoid reloading)"""
#     try:
#         if not GEMINI_API_KEY:
#             st.warning("Gemini API key not found. Using fallback responses.")
#             return None
#         if not os.path.exists(RESUME_PATH):
#             st.error(f"Resume file not found at {RESUME_PATH}")
#             return None
#         return ResumeRAG(RESUME_PATH, GEMINI_API_KEY)
#     except Exception as e:
#         st.error(f"Failed to load RAG engine: {str(e)}")
#         return None

# rag_engine = load_rag_engine()
rag_engine = None  # Set to None for standalone mode

def simulate_typing_effect(text: str, delay: float = 0.02):
    """Simulate typing animation for output text"""
    placeholder = st.empty()
    typed_text = ""
    for char in text:
        typed_text += char
        placeholder.markdown(
            f'<div class="terminal-output">{typed_text}</div>',
            unsafe_allow_html=True
        )
        time.sleep(delay)

# --- Initialize session state ---
if "history" not in st.session_state:
    welcome_text = """Hi, I'm Neema Mwende, a Software & AI Engineer.
Welcome to my interactive terminal! Type 'help' to see available commands.

Type any command to continue..."""
    st.session_state.history = [
        {"command": "welcome", "output": welcome_text, "timestamp": datetime.now()}
    ]

if "current_input" not in st.session_state:
    st.session_state.current_input = ""

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

if "typing_complete" not in st.session_state:
    st.session_state.typing_complete = False

# --- Fallback responses (will be replaced by RAG) ---
FALLBACK_RESPONSES = {
    "help": """Available commands:
• about - Learn about me
• skills - View my technical skills
• projects - See my projects
• experience - View my work experience
• education - See my education background
• contact - Get my contact information
• clear - Clear terminal
• Or ask any question about my background!""",
    
    "about": """• I'm Neema Mwende, a passionate Software & AI Engineer based in Nairobi, Kenya
• I specialize in building intelligent systems using cutting-edge AI technologies
• My work spans machine learning, NLP, RAG systems, and full-stack development
• I'm passionate about creating solutions that make real-world impact
• Skills: Python, AI/ML, LangChain, Streamlit, React, Cloud Computing
• Interests: AI Research, Open Source, Tech Community Building""",
    
    "skills": """Technical Skills:

Programming Languages:
• Python, JavaScript, SQL

AI/Machine Learning:
• LangChain, RAG (Retrieval Augmented Generation)
• Google Gemini, OpenAI APIs
• Natural Language Processing
• Vector Databases (ChromaDB)

Web Development:
• Streamlit, React, Node.js
• Flask, FastAPI
• HTML/CSS, Tailwind

Databases & Tools:
• ChromaDB, MySQL, PostgreSQL
• Docker, Git, GitHub
• Cloud Platforms (AWS, GCP)""",
    
    "projects": """Featured Projects:

1. AI-Powered Terminal Portfolio (Current)
   • Interactive terminal-style portfolio with RAG integration
   • Technologies: Streamlit, Python, ChromaDB, LangChain
   • Features: Real-time AI responses, resume querying
   
2. HR Chatbot with RAG
   • Intelligent chatbot for HR queries using retrieval-augmented generation
   • Technologies: LangChain, Streamlit, OpenAI
   • Handles employee queries with context-aware responses
   
3. Expense Tracker Application
   • Full-stack expense management system
   • Technologies: React, Node.js, MySQL
   • Features: Budget tracking, analytics, reporting
   
4. Django E-commerce Site
   • Complete e-commerce platform
   • Technologies: Django, PostgreSQL, Stripe
   • Features: Product management, payment processing, user authentication""",
    
    "experience": """Work Experience:

AI Engineer & Software Developer
Freelance/Contract | 2023 - Present
• Developing AI-powered applications using LangChain and RAG
• Building scalable backend systems with Python and FastAPI
• Implementing machine learning solutions for clients
• Creating intelligent chatbots and automation tools

Software Developer
[Previous Company] | 2021 - 2023
• Developed full-stack web applications using React and Node.js
• Implemented RESTful APIs and database design
• Collaborated with cross-functional teams on product development
• Optimized application performance and user experience

Junior Developer
[Entry Role] | 2020 - 2021
• Built responsive web interfaces using modern frameworks
• Participated in code reviews and agile development
• Maintained and debugged existing applications
• Learned best practices in software engineering""",
    
    "education": """Education:

Bachelor of Science in Computer Science
[University Name] | 2016 - 2020
• Focus: Software Engineering, AI, Data Structures

Relevant Coursework:
• Artificial Intelligence & Machine Learning
• Data Structures & Algorithms
• Database Management Systems
• Software Engineering Principles
• Web Development
• Cloud Computing

Certifications & Training:
• AI Engineering Bootcamp
• LangChain & RAG Development
• Cloud Architecture (AWS/GCP)
• Full-Stack Web Development

Continuous Learning:
• Currently exploring: Advanced RAG techniques, LLM fine-tuning
• Active in AI/ML communities and hackathons
• Regular contributor to open-source projects""",
    
    "contact": """Let's Connect!

• Email: neemamwende@gmail.com
• GitHub: github.com/NeemaMwende
• LinkedIn: linkedin.com/in/neemamwende
• Twitter: @neemamwende
• Location: Nairobi, Kenya

Availability:
• Open to: Full-time, Contract, Collaboration opportunities
• Interested in: AI/ML projects, innovative startups, impactful tech

Feel free to reach out for collaborations, opportunities, or just to chat about AI and technology!""",
}

# --- Custom CSS Styling ---
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Reset padding */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Body styling */
    .stApp {
        background-color: #000000;
    }
    
    /* Header navigation */
    .header {
        color: #00ff99;
        border-bottom: 1px solid #00ff99;
        padding: 15px 30px;
        margin: 0;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        background-color: #000;
    }
    
    /* Prompt styling - ALWAYS BLUE */
    .terminal-prompt {
        color: blue !important;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        display: inline;
    }
    
    /* Command styling */
    .terminal-command {
        color: #00ff99;
        font-family: 'Courier New', monospace;
        display: inline;
    }
    
    /* Output styling */
    .terminal-output {
        color: #ffffff;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        margin: 5px 0 15px 0;
        line-height: 1.5;
    }
    
    /* Input wrapper - keep inside terminal */
    .input-wrapper {
        display: flex;
        align-items: flex-start;
        margin-top: 10px;
    }
    
    .input-prompt {
        color: blue !important;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        margin-right: 5px;
        flex-shrink: 0;
    }
    
    /* Blinking cursor */
    .blinking-cursor {
        color: #00ff99;
        font-weight: bold;
        animation: blink 1s infinite;
        font-family: 'Courier New', monospace;
        display: inline-block;
        margin-left: 2px;
    }
    
    @keyframes blink {
        0%, 49% { opacity: 1; }
        50%, 100% { opacity: 0; }
    }
    
    /* Input field styling */
    .stTextInput {
        flex-grow: 1;
        display: inline-block;
    }
    
    .stTextInput > div > div > input {
        background-color: #000000 !important;
        color: #00ff99 !important;
        border: none !important;
        font-family: 'Courier New', monospace !important;
        font-size: 14px !important;
        padding: 0 !important;
        box-shadow: none !important;
        height: auto !important;
        line-height: 1.5 !important;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: none !important;
        border: none !important;
    }
    
    .stTextInput > label {
        display: none !important;
    }
    
    /* Hide input container borders */
    .stTextInput > div {
        border: none !important;
        padding: 0 !important;
    }
    
    /* Hide submit button but keep it functional */
    .stButton button {
        display: none !important;
    }
    
    /* Form styling */
    .stForm {
        border: none !important;
        padding: 0 !important;
    }
    
    /* Timestamp */
    .timestamp {
        color: #00ff99;
        text-align: right;
        font-size: 12px;
        font-family: 'Courier New', monospace;
        padding-right: 30px;
        margin-top: 10px;
    }
    
    /* Fix for Streamlit columns inside terminal */
    [data-testid="column"] {
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Process Command ---
def process_command(cmd):
    """Process user command and return response"""
    cmd = cmd.strip().lower()
    
    if cmd == "clear":
        # Clear history except welcome
        welcome_text = """Hi, I'm Neema Mwende, a Software & AI Engineer.
Welcome to my interactive terminal! /nType 'help' to see available commands./n/n

Type any command to continue..."""
        st.session_state.history = [
            {"command": "welcome", "output": welcome_text, "timestamp": datetime.now()}
        ]
        st.session_state.typing_complete = False
        return None
    
    if cmd == "":
        return ""
    
    # If RAG engine is available, use it
    if rag_engine:
        try:
            # Check for static responses first
            static_response = rag_engine.get_static_response(cmd)
            
            if static_response:
                return static_response
            else:
                # Use RAG for other queries
                return rag_engine.query(cmd)
        except Exception as e:
            return f"Error processing command: {str(e)}"
    else:
        # Use fallback responses
        if cmd in FALLBACK_RESPONSES:
            return FALLBACK_RESPONSES[cmd]
        else:
            # Try to answer as an AI question
            return f"Command '{cmd}' not recognized. Type 'help' to see available commands.\n\n(Note: RAG engine not loaded. This terminal is running in standalone mode with fallback responses.)"

# --- Header Navigation ---
st.markdown(
    '<div class="header">help | about | projects | skills | experience | contact | education | clear</div>',
    unsafe_allow_html=True
)

# --- Display command history ---
for i, entry in enumerate(st.session_state.history):
    # Always show the prompt with command
    st.markdown(
        f'<div><span class="terminal-prompt">neema@terminal:~$ </span>'
        f'<span class="terminal-command">{entry["command"]}</span></div>',
        unsafe_allow_html=True
    )

    if entry["output"]:
        output_escaped = (
            entry["output"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        # Animate typing only for the last (most recent) output and only once
        if i == len(st.session_state.history) - 1 and not st.session_state.typing_complete:
            simulate_typing_effect(output_escaped)
            st.session_state.typing_complete = True
        else:
            # Instantly render previous outputs (no animation)
            st.markdown(f'<div class="terminal-output">{output_escaped}</div>', unsafe_allow_html=True)

# --- Input Section ---
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
st.markdown('<span class="input-prompt">neema@terminal:~$ </span><span class="blinking-cursor">█</span>', unsafe_allow_html=True)

with st.form(key=f"input_form_{st.session_state.input_key}", clear_on_submit=True):
    user_input = st.text_input(
        "command",
        key=f"user_input_{st.session_state.input_key}",
        label_visibility="collapsed",
        placeholder=""
    )
    submitted = st.form_submit_button("Submit")

    if submitted and user_input:
        response = process_command(user_input)
        if response is not None:
            st.session_state.history.append({
                "command": user_input,
                "output": response,
                "timestamp": datetime.now()
            })
        st.session_state.input_key += 1
        st.session_state.typing_complete = False  # Reset for next command
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # close input-wrapper

# --- Timestamp ---
current_time = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
st.markdown(f'<div class="timestamp">{current_time}</div>', unsafe_allow_html=True)