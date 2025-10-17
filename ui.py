"""
UI - Streamlit frontend for portfolio terminal
Maintains original design, connects to MCP server backend
"""

import streamlit as st
from datetime import datetime
from mcp_server import MCPServer
from config import Config

st.set_page_config(page_title="My Terminal", layout="wide")

# --- Initialize MCP server silently ---
if "mcp_server" not in st.session_state:
    try:
        server = MCPServer(resume_pdf_path=Config.RESUME_PDF_PATH)
        st.session_state.mcp_server = server
    except Exception as e:
        st.session_state.mcp_server = None
        print("MCP server initialization error:", e)

mcp_server = st.session_state.mcp_server

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
.stTextInput > div { display: none !important; }
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

# --- Session State ---
if "history" not in st.session_state:
    
    welcome_text = (
        "<span style='color:#00ff99;'>"
        "Hi, I'm Neema Mwende, a Software & AI Engineer.<br><br>"
        "Welcome to my interactive 'AI powered' portfolio terminal!<br>"
        "Type <b>'help'</b> to see available commands.<br><br>"
        "Type any command to continue..."
        "</span>"
    )
    st.session_state.history = [
        (Config.TERMINAL_PROMPT, "", welcome_text, False)
    ]

if "temp_command" not in st.session_state:
    st.session_state.temp_command = ""

# --- Header bar ---
st.markdown(
    '<div class="header">help | about | projects | skills | experience | contact | education | certifications | clear</div>',
    unsafe_allow_html=True
)

# --- Terminal Container ---
terminal_container = st.container()

def render_terminal():
    html = '<div class="terminal" id="terminal" tabindex="0">'
    for prompt, command, output, is_ai in st.session_state.history:
        html += f'<div><span class="prompt">{prompt}</span><span class="command">{command}</span></div>'
        if output:
            output_class = "ai-output" if is_ai else "output"
            html += f'<div class="{output_class}">{output}</div>'
    html += '<div class="input-line">'
    html += f'<span class="prompt">{Config.TERMINAL_PROMPT}</span>'
    html += '<span id="typed-text" class="command"></span>'
    html += '<span class="cursor"></span>'
    html += '</div>'
    html += '</div>'
    terminal_container.markdown(html, unsafe_allow_html=True)

render_terminal()

# --- Hidden text input ---
command_input = st.text_input("command_input", key="terminal_input", label_visibility="collapsed")

# --- Typing system (JS) ---
st.markdown("""
<script>
(function() {
  if (!window.terminalState) {
    window.terminalState = { typed: '', attached: false };
  }
  
  function updateDisplay() {
    const typedText = document.querySelector('#typed-text');
    const terminal = document.querySelector('#terminal');
    if (typedText) typedText.textContent = window.terminalState.typed;
    if (terminal) terminal.scrollTop = terminal.scrollHeight;
  }
  
  function handleKey(e) {
    const hiddenInput = document.querySelector('input[data-testid="stTextInput"]') || 
                        document.querySelector('input[type="text"]');
    
    if (e.key === 'Enter') {
      e.preventDefault();
      if (hiddenInput && window.terminalState.typed.trim() !== '') {
        hiddenInput.value = window.terminalState.typed;
        const inputEvent = new Event('input', { bubbles: true });
        const changeEvent = new Event('change', { bubbles: true });
        hiddenInput.dispatchEvent(inputEvent);
        hiddenInput.dispatchEvent(changeEvent);
        const enterEvent = new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true });
        hiddenInput.dispatchEvent(enterEvent);
      }
      window.terminalState.typed = '';
      updateDisplay();
      return false;
    } else if (e.key === 'Backspace') {
      e.preventDefault();
      window.terminalState.typed = window.terminalState.typed.slice(0, -1);
      updateDisplay();
      return false;
    } else if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      window.terminalState.typed += e.key;
      updateDisplay();
      return false;
    }
  }
  
  if (!window.terminalState.attached) {
    document.addEventListener('keydown', handleKey, true);
    window.terminalState.attached = true;
  }
  
  setTimeout(() => {
    const terminal = document.querySelector('#terminal');
    if (terminal) terminal.focus();
  }, 100);
  
  updateDisplay();
})();
</script>
""", unsafe_allow_html=True)

# --- Process Commands ---
if command_input and command_input.strip():
    cmd = command_input.strip()
    if cmd != st.session_state.temp_command:
        st.session_state.temp_command = cmd

        if cmd.lower() == "clear":
            st.session_state.history = []
        else:
            if mcp_server:
                try:
                    response, is_ai = mcp_server.process_command(cmd)
                    st.session_state.history.append((Config.TERMINAL_PROMPT, cmd, response, is_ai))
                except Exception as e:
                    st.session_state.history.append((Config.TERMINAL_PROMPT, cmd, f"Error: {str(e)}", False))
            else:
                st.session_state.history.append((Config.TERMINAL_PROMPT, cmd, "Terminal not initialized. Please refresh.", False))

        st.rerun()

# --- Timestamp ---
now = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
st.markdown(f'<div class="timestamp">{now}</div>', unsafe_allow_html=True)
