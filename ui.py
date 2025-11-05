# """
# UI - Standalone Streamlit terminal interface with typing effects
# Author: Neema Mwende
# """

# import streamlit as st
# from datetime import datetime
# import streamlit.components.v1 as components
# import json
# from rag_engine import ResumeRAG
# import os
# from dotenv import load_dotenv
# import time

# load_dotenv()

# RESUME_PATH = "resume.pdf" 
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# st.set_page_config(page_title="AI Terminal", layout="wide")

# # --- Initialize RAG Engine ---
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

# # --- Initialize session state ---
# if "history" not in st.session_state:
#     welcome_text = """Hi, I'm Neema Mwende, a Software & AI Engineer.

# Welcome to my interactive terminal!
# Type 'help' to see available commands.

# Type any command to continue..."""
#     st.session_state.history = [
#         {"prompt": "neema@terminal:~$ ", "command": "welcome", "output": welcome_text, "is_ai": False}
#     ]

# if "current_input" not in st.session_state:
#     st.session_state.current_input = ""

# if "command_count" not in st.session_state:
#     st.session_state.command_count = 0

# if "processing" not in st.session_state:
#     st.session_state.processing = False


# # --- Custom CSS Styling ---
# st.markdown("""
# <style>
# body {
#     background-color: black;
#     margin: 0;
#     padding: 0;
# }
# .main { 
#     background-color: black; 
# }
# .stApp { 
#     background-color: black; 
# }
# .header {
#     color: #00ff99;
#     border-bottom: 1px solid #00ff99;
#     padding: 10px 20px;
#     margin-bottom: 10px;
#     font-family: monospace;
#     font-size: 14px;
#     background-color: #000;
# }
# </style>
# """, unsafe_allow_html=True)


# # --- Terminal Header ---
# st.markdown(
#     '<div class="header">help | about | projects | skills | experience | contact | education | clear</div>',
#     unsafe_allow_html=True
# )


# # --- Generate the HTML for the terminal ---
# def create_terminal_html():
#     history_json = json.dumps(st.session_state.history)
#     command_count = st.session_state.command_count
#     now = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")

#     html = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <style>
#             body {{
#                 background-color: #000;
#                 font-family: 'Courier New', monospace;
#                 color: #fff;
#                 overflow: hidden;
#                 margin: 0;
#                 padding: 0;
#             }}
#             .terminal {{
#                 background-color: #000;
#                 color: #fff;
#                 font-family: 'Courier New', monospace;
#                 padding: 20px;
#                 border: 1px solid #00ff99;
#                 border-radius: 5px;
#                 min-height: 500px;
#                 max-height: 500px;
#                 overflow-y: auto;
#                 white-space: pre-wrap;
#                 word-wrap: break-word;
#             }}
#             .prompt {{ color: #00aaff; font-weight: bold; }}
#             .command {{ color: #00ff99; }}
#             .output {{ color: #fff; margin-top: 5px; margin-bottom: 15px; line-height: 1.5; }}
#             .ai-output {{ color: #fff; margin-top: 5px; margin-bottom: 15px; line-height: 1.5; }}
#             .input-line {{ display: flex; align-items: baseline; }}
#             #typed-text {{ color: #00ff99; }}
#             .cursor {{
#                 display: inline-block;
#                 background-color: #00ff99;
#                 width: 8px;
#                 height: 16px;
#                 animation: blink 1s step-start infinite;
#                 margin-left: 2px;
#                 vertical-align: baseline;
#             }}
#             @keyframes blink {{ 50% {{ background-color: transparent; }} }}
#             .timestamp {{
#                 color: #00ff99;
#                 text-align: right;
#                 font-size: 12px;
#                 margin-top: 10px;
#                 padding-right: 20px;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="terminal" id="terminal" tabindex="0">
#             <div id="history-container"></div>
#             <div class="input-line" id="input-line">
#                 <span class="prompt">neema@terminal:~$ </span>
#                 <span id="typed-text"></span>
#                 <span class="cursor"></span>
#             </div>
#         </div>
#         <div class="timestamp">{now}</div>

#         <script>
#             let currentInput = '';
#             let isTyping = false;
#             let history = {history_json};
#             let displayedCount = 0;
#             let commandCount = {command_count};
#             let lastSentCommand = '';

#             function escapeHtml(text) {{
#                 const div = document.createElement('div');
#                 div.textContent = text;
#                 return div.innerHTML;
#             }}

#             function typeText(element, text, speed, callback) {{
#                 let index = 0;
#                 element.textContent = '';
#                 function typeChar() {{
#                     if (index < text.length) {{
#                         element.textContent += text.charAt(index);
#                         index++;
#                         scrollToBottom();
#                         setTimeout(typeChar, speed);
#                     }} else {{
#                         if (callback) callback();
#                     }}
#                 }}
#                 typeChar();
#             }}

#             function scrollToBottom() {{
#                 const terminal = document.getElementById('terminal');
#                 terminal.scrollTop = terminal.scrollHeight;
#             }}

#             function displayHistory() {{
#                 const container = document.getElementById('history-container');
#                 if (displayedCount < history.length) {{
#                     const entry = history[displayedCount];
#                     displayedCount++;
#                     const commandDiv = document.createElement('div');
#                     const promptSpan = document.createElement('span');
#                     promptSpan.className = 'prompt';
#                     promptSpan.textContent = entry.prompt;
#                     const commandSpan = document.createElement('span');
#                     commandSpan.className = 'command';
#                     commandSpan.textContent = entry.command;
#                     commandDiv.appendChild(promptSpan);
#                     commandDiv.appendChild(commandSpan);
#                     container.appendChild(commandDiv);
#                     if (entry.output) {{
#                         const outputDiv = document.createElement('div');
#                         outputDiv.className = entry.is_ai ? 'ai-output' : 'output';
#                         container.appendChild(outputDiv);
#                         isTyping = true;
#                         typeText(outputDiv, entry.output, 10, function() {{
#                             isTyping = false;
#                             displayHistory();
#                         }});
#                     }} else {{
#                         displayHistory();
#                     }}
#                 }}
#             }}

#             function updateDisplay() {{
#                 const typedText = document.getElementById('typed-text');
#                 if (typedText) {{
#                     typedText.textContent = currentInput;
#                 }}
#                 scrollToBottom();
#             }}

#             function sendCommand(cmd) {{
#                 // Prevent sending duplicate commands
#                 if (cmd === lastSentCommand) {{
#                     console.log('Duplicate command prevented:', cmd);
#                     return;
#                 }}
#                 lastSentCommand = cmd;
#                 console.log('Sending command:', cmd);
#                 window.parent.postMessage({{
#                     type: 'streamlit:setComponentValue',
#                     value: cmd
#                 }}, '*');
#             }}

#             document.addEventListener('keydown', function(e) {{
#                 if (isTyping) {{
#                     e.preventDefault();
#                     return;
#                 }}
#                 if (e.key === 'Enter') {{
#                     e.preventDefault();
#                     const cmd = currentInput.trim();
#                     if (cmd !== '') {{
#                         sendCommand(cmd);
#                         currentInput = '';
#                         updateDisplay();
#                     }}
#                 }} else if (e.key === 'Backspace') {{
#                     e.preventDefault();
#                     currentInput = currentInput.slice(0, -1);
#                     updateDisplay();
#                 }} else if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {{
#                     e.preventDefault();
#                     currentInput += e.key;
#                     updateDisplay();
#                 }}
#             }});

#             const terminal = document.getElementById('terminal');
#             terminal.focus();
#             terminal.addEventListener('blur', function() {{
#                 if (!isTyping) {{
#                     setTimeout(() => terminal.focus(), 10);
#                 }}
#             }});
            
#             // Initialize display
#             displayHistory();
#             updateDisplay();
#             console.log('Terminal initialized with', history.length, 'history entries');
#         </script>
#     </body>
#     </html>
#     """
#     return html


# # --- Render the Terminal ---
# terminal_html = create_terminal_html()
# command_received = components.html(terminal_html, height=650, scrolling=False)


# # --- Command Processing with RAG Integration ---
# if command_received and isinstance(command_received, str) and command_received.strip():
#     cmd = command_received.strip()

#     # Avoid reprocessing same command
#     if cmd != st.session_state.current_input and not st.session_state.processing:
#         st.session_state.processing = True
#         st.session_state.current_input = cmd
#         st.session_state.command_count += 1

#         if cmd.lower() == "clear":
#             welcome_text = """Hi, I'm Neema Mwende, a Software & AI Engineer.

# Welcome to my interactive terminal!
# Type 'help' to see available commands.

# Type any command to continue..."""
#             st.session_state.history = [
#                 {"prompt": "neema@terminal:~$ ", "command": "", "output": welcome_text, "is_ai": False}
#             ]
#         else:
#             # Check if RAG engine is available
#             if rag_engine:
#                 try:
#                     # Check for static responses first
#                     static_response = rag_engine.get_static_response(cmd)
                    
#                     if static_response:
#                         response = static_response
#                         is_ai = False
#                     else:
#                         # Use RAG for other queries
#                         response = rag_engine.query(cmd)
#                         is_ai = True
#                 except Exception as e:
#                     response = f"Error processing command: {str(e)}"
#                     is_ai = False
#             else:
#                 # Fallback to simulated responses if RAG fails
#                 responses = {
#                     "help": """Available commands:
# • about - Learn about me
# • skills - View my technical skills
# • projects - See my projects
# • experience - View my work experience
# • education - See my education background
# • contact - Get my contact information
# • clear - Clear terminal
# • Or ask any question about my background!""",
#                     "about": "I'm Neema Mwende, a passionate AI Engineer & Software Developer from Nairobi.",
#                     "skills": """Technical Skills:
# • Languages: Python, JavaScript
# • Frameworks: React, Node.js, Streamlit
# • AI/ML: LangChain, RAG, Google Gemini
# • Tools: Docker, MySQL, Git""",
#                     "projects": """Projects:
# • HR Chatbot (RAG + Streamlit)
# • Portfolio Terminal
# • Expense Tracker App
# • Django E-commerce Site""",
#                     "contact": """Contact Information:
# • Email: neemamwende@gmail.com
# • GitHub: github.com/NeemaMwende
# • LinkedIn: linkedin.com/in/neemamwende""",
#                     "experience": "Please add your experience details to this fallback response.",
#                     "education": "Please add your education details to this fallback response."
#                 }
#                 response = responses.get(cmd.lower(), f"Command '{cmd}' not found. Type 'help' for options.")
#                 is_ai = False

#             st.session_state.history.append({
#                 "prompt": "neema@terminal:~$ ",
#                 "command": cmd,
#                 "output": response,
#                 "is_ai": is_ai
#             })
        
#         st.session_state.processing = False
#         time.sleep(0.1)  # Brief pause to ensure state is saved
#         st.rerun()