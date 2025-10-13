import streamlit as st
import time
import re
from pathlib import Path
from datetime import datetime
from PIL import Image
import PyPDF2

st.set_page_config(
    page_title="Portfolio Terminal - Neema",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for terminal styling
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        background-color: #000000;
        color: #00ff00;
        font-family: 'Courier New', monospace;
    }
    
    .main {
        background-color: #000000;
        padding: 0;
    }
    
    .stApp {
        background-color: #000000;
    }
    
    .terminal-wrapper {
        display: grid;
        grid-template-columns: 280px 1fr;
        gap: 20px;
        padding: 20px;
        background-color: #000000;
    }
    
    .profile-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 15px;
        background-color: #111111;
        padding: 20px;
        border: 2px solid #00ff00;
        border-radius: 8px;
        height: fit-content;
    }
    
    .profile-image {
        width: 100%;
        max-width: 260px;
        aspect-ratio: 1;
        border: 3px solid #00ff00;
        border-radius: 8px;
        object-fit: cover;
    }
    
    .profile-name {
        color: #00ff00;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
    }
    
    .profile-title {
        color: #888888;
        font-size: 12px;
        text-align: center;
    }
    
    .terminal-container {
        background-color: #000000;
        border: 2px solid #00ff00;
        border-radius: 5px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        color: #00ff00;
        min-height: 700px;
        display: flex;
        flex-direction: column;
    }
    
    .terminal-output {
        flex-grow: 1;
        overflow-y: auto;
        margin-bottom: 20px;
        white-space: pre-wrap;
        word-wrap: break-word;
        line-height: 1.6;
        font-size: 12px;
        font-family: 'Courier New', monospace;
    }
    
    .stTextInput > div > div > input {
        background-color: #000000;
        color: #00ff00;
        border: 1px solid #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 12px;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #000000;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00ff00;
        border-radius: 4px;
    }
    
    .header {
        background-color: #000000;
        padding: 20px;
        border-bottom: 2px solid #00ff00;
        margin-bottom: 20px;
    }
    
    .header h1 {
        color: #00ff00;
        margin: 0;
        font-size: 32px;
    }
    
    .header p {
        color: #00ff00;
        margin: 5px 0;
        font-size: 14px;
    }
    
    .header-sub {
        color: #888888;
        margin: 5px 0;
        font-size: 12px;
    }
    
    .footer {
        text-align: center;
        color: #888888;
        font-size: 12px;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #333333;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.resume_data = {}
    st.session_state.user_name = "Neema"
    st.session_state.typing_complete = True

def extract_pdf_sections(pdf_path):
    """Extract sections from resume PDF"""
    sections = {}
    try:
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            full_text = ""
            for page in pdf_reader.pages:
                full_text += page.extract_text() + "\n"
        
        # Extract common resume sections
        section_patterns = {
            "professional_summary": r"(?:PROFESSIONAL SUMMARY|SUMMARY|OBJECTIVE)(.*?)(?=\n[A-Z\s]+:|$)",
            "contact": r"(?:CONTACT|EMAIL|PHONE)(.*?)(?=\n[A-Z\s]+:|$)",
            "skills": r"(?:SKILLS|TECHNICAL SKILLS)(.*?)(?=\n[A-Z\s]+:|$)",
            "experience": r"(?:EXPERIENCE|WORK EXPERIENCE)(.*?)(?=\n[A-Z\s]+:|$)",
            "education": r"(?:EDUCATION|EDUCATIONAL)(.*?)(?=\n[A-Z\s]+:|$)",
            "certifications": r"(?:CERTIFICATIONS|CERTIFICATES)(.*?)(?=\n[A-Z\s]+:|$)",
            "projects": r"(?:PROJECTS|PORTFOLIO)(.*?)(?=\n[A-Z\s]+:|$)",
        }
        
        for key, pattern in section_patterns.items():
            match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
            if match:
                sections[key] = match.group(1).strip()
            else:
                sections[key] = f"[{key.replace('_', ' ').title()} information not found in resume]"
        
        return sections
    except Exception as e:
        st.warning(f"Error reading PDF: {e}")
        return {}

def generate_placeholder_image():
    """Generate a placeholder profile image"""
    img = Image.new('RGB', (260, 260), color='#1a1a1a')
    return img

def typing_animation(text, placeholder):
    """Display text with typing animation effect"""
    displayed_text = ""
    for char in text:
        displayed_text += char
        placeholder.text_area("", displayed_text, disabled=True, height=400)
        time.sleep(0.01)

def format_response(response_text):
    """Format response into bullet points"""
    lines = response_text.split('\n')
    formatted = []
    for line in lines:
        line = line.strip()
        if line:
            if not line.startswith('•') and not line.startswith('-') and not line.startswith('*'):
                formatted.append(f"  • {line}")
            else:
                formatted.append(f"  {line}")
    return "\n".join(formatted)

# Load resume on startup
resume_path = Path("Neema.pdf")
if resume_path.exists() and not st.session_state.resume_data:
    with st.spinner("Loading resume..."):
        st.session_state.resume_data = extract_pdf_sections(str(resume_path))

# Commands help
commands = {
    "help": "Show available commands",
    "about": "Professional summary",
    "skills": "View technical skills",
    "experience": "Work experience",
    "projects": "View projects",
    "contact": "Contact information",
    "education": "Educational background",
    "certifications": "Certifications and qualifications",
    "clear": "Clear terminal",
}

def process_command(cmd):
    """Process user commands"""
    cmd = cmd.strip().lower()
    
    if cmd == "help":
        help_text = "Available commands:\n"
        for k, v in commands.items():
            help_text += f"  {k:20} - {v}\n"
        return help_text.rstrip()
    
    elif cmd == "about":
        text = st.session_state.resume_data.get("professional_summary", "Professional summary not found")
        return format_response(text)
    
    elif cmd == "skills":
        text = st.session_state.resume_data.get("skills", "Skills not found")
        return format_response(text)
    
    elif cmd == "experience":
        text = st.session_state.resume_data.get("experience", "Experience not found")
        return format_response(text)
    
    elif cmd == "projects":
        text = st.session_state.resume_data.get("projects", "Projects not found")
        return format_response(text)
    
    elif cmd == "contact":
        text = st.session_state.resume_data.get("contact", "Contact not found")
        return format_response(text)
    
    elif cmd == "education":
        text = st.session_state.resume_data.get("education", "Education not found")
        return format_response(text)
    
    elif cmd == "certifications":
        text = st.session_state.resume_data.get("certifications", "Certifications not found")
        return format_response(text)
    
    elif cmd == "clear":
        st.session_state.history = []
        return ""
    
    elif cmd == "":
        return ""
    
    else:
        return f"Command not found: '{cmd}'. Type 'help' for available commands."

# Header
st.markdown("""
<div class="header">
    <h1>Neema</h1>
    <p>Software Engineer & Developer</p>
    <p class="header-sub">Portfolio Terminal v1.0 | Powered by ByLLM & JAC</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col_left, col_right = st.columns([0.22, 0.78], gap="large")

with col_left:
    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
    placeholder_img = generate_placeholder_image()
    st.image(placeholder_img, use_container_width=True)
    st.markdown('<div class="profile-name">Neema</div>', unsafe_allow_html=True)
    st.markdown('<div class="profile-title">Software Engineer</div>', unsafe_allow_html=True)
    
    if st.session_state.resume_data:
        st.markdown("""
        <div style="background-color: #001100; border: 1px solid #00ff00; padding: 10px; border-radius: 5px; text-align: center; color: #00ff00; font-size: 11px; margin-top: 15px;">
            ✓ Resume loaded
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="terminal-container">', unsafe_allow_html=True)
    
    # Terminal output area
    terminal_placeholder = st.empty()
    
    # Generate output text
    output_text = ""
    if not st.session_state.history:
        output_text = """help | about | skills | experience | projects | contact | education | certifications | clear

neema@portfolio:~$ welcome
Hi, I'm Neema, a Software Engineer.

Welcome to my interactive 'AI powered' portfolio terminal!
Type 'help' to see available commands.

neema@portfolio:~$ """
    else:
        for item in st.session_state.history:
            output_text += f"neema@portfolio:~$ {item['command']}\n"
            output_text += f"{item['response']}\n\n"
    
    with terminal_placeholder.container():
        st.markdown(
            f'<div class="terminal-output"><pre>{output_text}</pre></div>',
            unsafe_allow_html=True
        )
    
    # Input area
    input_col1, input_col2 = st.columns([0.88, 0.12], gap="small")
    
    with input_col1:
        user_input = st.text_input(
            "Command",
            placeholder="Type a command or 'help'...",
            label_visibility="collapsed",
            key=f"input_{len(st.session_state.history)}"
        )
    
    with input_col2:
        submit = st.button("⏎", use_container_width=True, key="submit_btn")
    
    # Process input with typing animation
    if submit and user_input:
        response = process_command(user_input)
        st.session_state.history.append({
            "command": user_input,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer inside terminal
st.markdown("""
<div class="footer">
    <p>Last updated: """ + datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p") + """ | © 2025 Neema</p>
</div>
""", unsafe_allow_html=True)