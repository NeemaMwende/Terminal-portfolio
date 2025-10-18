"""
UI - Streamlit frontend for portfolio terminal with typing effects
"""

import streamlit as st
from datetime import datetime
from mcp_server import MCPServer
from config import Config
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="My Terminal", layout="wide")

# --- Initialize MCP server with caching ---
@st.cache_resource
def get_mcp_server():
    """Initialize and cache MCP server - only runs once"""
    try:
        print("🚀 Initializing MCP Server...")
        server = MCPServer(resume_pdf_path=Config.RESUME_PDF_PATH)
        success = server.initialize()
        if success:
            print("✓ MCP Server cached and ready!")
            return server
        return None
    except Exception as e:
        print(f"✗ MCP server initialization error: {e}")
        return None

mcp_server = get_mcp_server()

# --- Session State ---
if "history" not in st.session_state:
    welcome_text = """Hi, I'm Neema Mwende, a Software & AI Engineer.

Welcome to my interactive 'AI powered' portfolio terminal!
Type 'help' to see available commands.

Type any command to continue..."""
    st.session_state.history = [
        {"prompt": Config.TERMINAL_PROMPT, "command": "", "output": welcome_text, "is_ai": False}
    ]

if "current_input" not in st.session_state:
    st.session_state.current_input = ""

if "command_count" not in st.session_state:
    st.session_state.command_count = 0

# --- Page CSS ---
st.markdown("""
<style>
body {
    background-color: black;
    margin: 0;
    padding: 0;
}
.main { 
    background-color: black; 
    padding: 0; 
}
.stApp { 
    background-color: black; 
}
.header {
    color: #00ff99;
    border-bottom: 1px solid #00ff99;
    padding: 10px 20px;
    margin-bottom: 10px;
    font-family: monospace;
    font-size: 14px;
    background-color: #000;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(
    '<div class="header">help | about | projects | skills | experience | contact | education | certifications | clear</div>',
    unsafe_allow_html=True
)

# --- Create Terminal HTML ---
def create_terminal_html():
    # Convert history to JSON for JavaScript
    history_json = json.dumps(st.session_state.history)
    command_count = st.session_state.command_count
    
    now = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                background-color: #000;
                font-family: 'Courier New', monospace;
                color: #fff;
                overflow: hidden;
            }}
            .terminal {{
                background-color: #000;
                color: #fff;
                font-family: 'Courier New', monospace;
                padding: 20px;
                border: 1px solid #00ff99;
                border-radius: 5px;
                min-height: 500px;
                max-height: 500px;
                overflow-y: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
                outline: none;
            }}
            .prompt {{ 
                color: #00aaff; 
                font-weight: bold; 
            }}
            .command {{ 
                color: #00ff99; 
            }}
            .output {{ 
                color: #ffffff; 
                margin-top: 5px; 
                margin-bottom: 15px;
                line-height: 1.5;
            }}
            .ai-output {{
                color: #ffffff;
                margin-top: 5px;
                margin-bottom: 15px;
                line-height: 1.5;
            }}
            .input-line {{ 
                display: flex; 
                align-items: baseline;
            }}
            #typed-text {{
                color: #00ff99;
            }}
            .cursor {{
                display: inline-block;
                background-color: #00ff99;
                width: 8px;
                height: 16px;
                animation: blink 1s step-start infinite;
                margin-left: 2px;
                vertical-align: baseline;
            }}
            @keyframes blink {{ 
                50% {{ background-color: transparent; }} 
            }}
            .timestamp {{
                color: #00ff99;
                text-align: right;
                font-size: 12px;
                margin-top: 10px;
                padding-right: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="terminal" id="terminal" tabindex="0">
            <div id="history-container"></div>
            <div class="input-line" id="input-line">
                <span class="prompt">{Config.TERMINAL_PROMPT}</span>
                <span id="typed-text"></span>
                <span class="cursor"></span>
            </div>
        </div>
        <div class="timestamp">{now}</div>
        
        <script>
            let currentInput = '';
            let isTyping = false;
            let history = {history_json};
            let displayedCount = 0;
            let commandCount = {command_count};
            
            function escapeHtml(text) {{
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }}
            
            function typeText(element, text, speed, callback) {{
                let index = 0;
                element.textContent = '';
                
                function typeChar() {{
                    if (index < text.length) {{
                        element.textContent += text.charAt(index);
                        index++;
                        scrollToBottom();
                        setTimeout(typeChar, speed);
                    }} else {{
                        if (callback) callback();
                    }}
                }}
                
                typeChar();
            }}
            
            function scrollToBottom() {{
                const terminal = document.getElementById('terminal');
                if (terminal) {{
                    terminal.scrollTop = terminal.scrollHeight;
                }}
            }}
            
            function displayHistory() {{
                const container = document.getElementById('history-container');
                
                if (displayedCount < history.length) {{
                    const entry = history[displayedCount];
                    displayedCount++;
                    
                    // Create command line
                    const commandDiv = document.createElement('div');
                    const promptSpan = document.createElement('span');
                    promptSpan.className = 'prompt';
                    promptSpan.textContent = entry.prompt;
                    
                    const commandSpan = document.createElement('span');
                    commandSpan.className = 'command';
                    commandSpan.textContent = entry.command;
                    
                    commandDiv.appendChild(promptSpan);
                    commandDiv.appendChild(commandSpan);
                    container.appendChild(commandDiv);
                    
                    // Create output
                    if (entry.output) {{
                        const outputDiv = document.createElement('div');
                        outputDiv.className = entry.is_ai ? 'ai-output' : 'output';
                        container.appendChild(outputDiv);
                        
                        isTyping = true;
                        typeText(outputDiv, entry.output, 10, function() {{
                            isTyping = false;
                            displayHistory(); // Continue with next entry
                        }});
                    }} else {{
                        displayHistory(); // Continue immediately if no output
                    }}
                }} else {{
                    // All history displayed, enable input
                    isTyping = false;
                    document.getElementById('terminal').focus();
                }}
            }}
            
            function updateDisplay() {{
                const typedText = document.getElementById('typed-text');
                if (typedText) {{
                    typedText.textContent = currentInput;
                }}
                scrollToBottom();
            }}
            
            function sendCommand(cmd) {{
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: cmd
                }}, '*');
            }}
            
            // Keyboard handler
            document.addEventListener('keydown', function(e) {{
                if (isTyping) {{
                    e.preventDefault();
                    return;
                }}
                
                if (e.key === 'Enter') {{
                    e.preventDefault();
                    const cmd = currentInput.trim();
                    if (cmd !== '') {{
                        sendCommand(cmd);
                        currentInput = '';
                        updateDisplay();
                    }}
                }} 
                else if (e.key === 'Backspace') {{
                    e.preventDefault();
                    currentInput = currentInput.slice(0, -1);
                    updateDisplay();
                }} 
                else if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {{
                    e.preventDefault();
                    currentInput += e.key;
                    updateDisplay();
                }}
            }});
            
            // Auto-focus
            const terminal = document.getElementById('terminal');
            terminal.focus();
            
            // Keep focus
            terminal.addEventListener('blur', function() {{
                if (!isTyping) {{
                    setTimeout(() => terminal.focus(), 10);
                }}
            }});
            
            // Start displaying history with typing effect
            displayHistory();
            updateDisplay();
        </script>
    </body>
    </html>
    """
    return html

# --- Render Terminal ---
terminal_html = create_terminal_html()
command_received = components.html(terminal_html, height=650, scrolling=False)

# --- Process Commands ---
if command_received and isinstance(command_received, str) and command_received.strip():
    cmd = command_received.strip()
    
    # Prevent duplicate processing
    if cmd != st.session_state.current_input:
        st.session_state.current_input = cmd
        st.session_state.command_count += 1
        
        if cmd.lower() == "clear":
           
            welcome_text = """Hi, I'm Neema Mwende, a Software & AI Engineer.

Welcome to my interactive 'AI powered' portfolio terminal!
Type 'help' to see available commands.

Type any command to continue..."""
            st.session_state.history = [
                {"prompt": Config.TERMINAL_PROMPT, "command": "", "output": welcome_text, "is_ai": False}
            ]
        else:
            if mcp_server and mcp_server.initialized:
                try:
                    response, is_ai = mcp_server.process_command(cmd)
                    st.session_state.history.append({
                        "prompt": Config.TERMINAL_PROMPT,
                        "command": cmd,
                        "output": response,
                        "is_ai": is_ai
                    })
                except Exception as e:
                    st.session_state.history.append({
                        "prompt": Config.TERMINAL_PROMPT,
                        "command": cmd,
                        "output": f"Error: {{str(e)}}",
                        "is_ai": False
                    })
            else:
                error_msg = "Terminal not initialized. Please check your API keys and resume.pdf file."
                st.session_state.history.append({
                    "prompt": Config.TERMINAL_PROMPT,
                    "command": cmd,
                    "output": error_msg,
                    "is_ai": False
                })
        
        # Rerun to show new output
        st.rerun()