from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_engine import SimpleRAG
import time

app = Flask(__name__)
CORS(app)

# Initialize RAG engine
rag = SimpleRAG()

COMMANDS = {
    "help": "Display available commands",
    "about": "Learn about me",
    "projects": "View my projects",
    "skills": "See my technical skills",
    "experience": "My work experience",
    "contact": "How to reach me",
    "education": "My educational background",
    "certifications": "View my certifications",
    "leadership": "Leadership and community involvement",
    "clear": "Clear the terminal"
}

@app.route('/api/command', methods=['POST'])
def process_command():
    data = request.json
    command = data.get('command', '').strip().lower()
    
    if not command:
        return jsonify({"response": "Please enter a command. Type 'help' for available commands."})
    
    # Handle special commands
    if command == "help":
        response = "Available commands:\n\n"
        for cmd, desc in COMMANDS.items():
            response += f"{cmd:15} - {desc}\n"
        response += "\nType any command to continue.."
        return jsonify({"response": response})
    
    if command == "clear":
        return jsonify({"response": "", "clear": True})
    
    if command == "welcome":
        response = "Hi, I'm Mark Gatere, a Software & AI Engineer.\n\n"
        response += "Welcome to my interactive 'AI powered' portfolio terminal!\n"
        response += "Type 'help' to see available commands."
        return jsonify({"response": response})
    
    # Check if valid command
    if command not in COMMANDS:
        return jsonify({"response": f"Command '{command}' not found. Type 'help' for available commands."})
    
    # Process with RAG
    try:
        response = rag.query(command)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"Error processing command: {str(e)}"})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)