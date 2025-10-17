"""
UI - Streamlit frontend for portfolio terminal
Maintains original design, connects to MCP server backend
"""
import streamlit as st
from datetime import datetime
from mcp_server import MCPServer
from config import Config

st.set_page_config(page_title="My Terminal", layout="wide")


def initialize_mcp_server():
    """Initialize MCP server with error handling"""
    # Validate config first
    is_valid, errors = Config.validate()
    if not is_valid:
        st.error("Configuration errors:")
        for error in errors:
            st.error(f"  • {error}")
        return None
    
    # Initialize MCP server
    server = MCPServer(resume_pdf_path=Config.RESUME_PDF_PATH)
    
    with st.spinner("Initializing AI Portfolio Terminal..."):
        if server.initialize():
            st.success("✓ Terminal ready!")
            return server
        else:
            st.error("Failed to initialize terminal. Check console for details.")
            return None


# Initialize MCP server once
if "mcp_server" not in st.session_state:
    st.session_state.mcp_server = initialize_mcp_server()

mcp_server = st.session_state.mcp_server

# --- CSS Styles (UNCHANGED) ---
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

# --- Session state ---
if "history" not in st.session_state:
    welcome_response, _ = mcp_server.process_command("welcome") if mcp_server else ("Terminal not initialized", False)
    st.session_state.history = [
        (Config.TERMINAL_PROMPT, "welcome", welcome_response, False)
    ]

if "temp_command" not in st.session_state:
    st.session_state.temp_command = ""

# --- Header bar (UNCHANGED) ---
st.markdown(
    '<div class="header">help | about | projects | skills | experience | contact | education | certifications | leadership | clear</div>',
    unsafe_allow_html=True
)

# --- Terminal render function (UNCHANGED) ---
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

# --- Hidden input field ---
command_input = st.text_input("", key="terminal_input", label_visibility="collapsed")

# --- JS Typing System (UNCHANGED) ---
st.markdown("""
<script>
(function() {
  window.terminalState = window.terminalState || {
    typed: '',
    attached: false
  };
  
  function updateDisplay() {
    const typedText = document.querySelector('#typed-text');
    const terminal = document.querySelector('#terminal');
    
    if (typedText) {
      typedText.textContent = window.terminalState.typed;
    }
    if (terminal) {
      terminal.scrollTop = terminal.scrollHeight;
    }
  }
  
  function handleKey(e) {
    const hiddenInput = document.querySelector('input[data-testid="stTextInput"]');
    
    if (e.key === 'Enter') {
      if (hiddenInput && window.terminalState.typed.trim() !== '') {
        hiddenInput.value = window.terminalState.typed;
        hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
        hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
      }
      window.terminalState.typed = '';
    } else if (e.key === 'Backspace') {
      e.preventDefault();
      window.terminalState.typed = window.terminalState.typed.slice(0, -1);
    } else if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
      window.terminalState.typed += e.key;
    }
    updateDisplay();
  }
  
  if (!window.terminalState.attached) {
    document.addEventListener('keydown', handleKey, true);
    window.terminalState.attached = true;
  }
  
  updateDisplay();
})();
</script>
""", unsafe_allow_html=True)

# --- Process command (UPDATED to use MCP server) ---
if command_input and command_input.strip():
    cmd = command_input.strip()
    
    if cmd != st.session_state.temp_command:
        st.session_state.temp_command = cmd

        if cmd.lower() == "clear":
            st.session_state.history = []
        else:
            # Process command through MCP server
            if mcp_server:
                try:
                    response, is_ai = mcp_server.process_command(cmd)
                    st.session_state.history.append(
                        (Config.TERMINAL_PROMPT, cmd, response, is_ai)
                    )
                except Exception as e:
                    st.session_state.history.append(
                        (Config.TERMINAL_PROMPT, cmd, f"Error: {str(e)}", False)
                    )
            else:
                st.session_state.history.append(
                    (Config.TERMINAL_PROMPT, cmd, "Terminal not initialized. Please refresh the page.", False)
                )

        st.rerun()

# --- Timestamp (UNCHANGED) ---
now = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
st.markdown(f'<div class="timestamp">{now}</div>', unsafe_allow_html=True)