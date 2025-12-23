"use client";

import { useState, useEffect, useRef } from "react";

export default function Terminal() {
  const [history, setHistory] = useState([]);
  const [currentInput, setCurrentInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const [currentTime, setCurrentTime] = useState("");
  const terminalRef = useRef(null);

  // Fallback responses for each command
  const fallbackResponses = {
    welcome: `Hi, I'm Neema Mwende, a Software & AI Engineer.

Welcome to my interactive 'AI powered' portfolio terminal!
Type 'help' to see available commands.

Type any command to continue..`,

    about: `I'm Neema Mwende, a results-driven Software and AI Engineer with a strong background in JavaScript and Python. I specialize in building efficient, scalable, and intelligent systems.

I'm passionate about integrating artificial intelligence and machine learning into software solutions to enhance automation and user experience. My expertise spans backend development, API integration, and data-driven problem-solving.

My vision is to leverage AI to create accessible and impactful technologies for real-world challenges.
`,

    projects: `Here are some of my notable projects:

🔹 AI-Powered Portfolio Terminal
   An interactive terminal-style portfolio with RAG integration
   Tech: Next.js, Python, AI/ML

🔹 CodeGenuis
   an AI-powered tool that analyzes, documents, and visualizes your entire codebase in real time. It provides insights, function summaries, and architecture graphs.
   Tech: Jac, Python, Streamlit, Langchain

🔹 HR-Powered Chatbot
   An AI-powered HR Chatbot built with Streamlit, LangChain, ChromaDB, and OpenAI Embeddings. Uses a RAG pipeline to answer HR-related questions from uploaded HR documents, offering intelligent contexts.
   Tech: Python, Streamlit, Chroma, Langchain

🔹 MCP-Chatbot 
   AI-powered multimodal chatbot that understands documents, images, and videos. Built with Jac Language, featuring Object Spatial Programming, MCP tools, RAG with ChromaDB, and OpenAI vision.
   Tech: Jac, Streamlit 

Visit my GitHub for more projects and code samples!`,

    skills: `Technical Skills:

Frontend Development:
• JavaScript (React.js, Next.js, Node.js, TypeScript)
• HTML5, CSS3
• Responsive Web Design

Backend Development:
• Python (Django)
• Express.js, Node.js
• API Development & Integration

AI & Machine Learning:
• Langchain, RAG (Retrieval-Augmented Generation), HuggingFace
• PyTorch, NumPy, Pandas, Matplotlib
• n8n (Automation)
• Vector Databases (Chroma, Pinecone, FAISS)

DevOps & Tools:
• Git, GitHub
• Docker
• Linux
• CI/CD Pipelines (GitHub Actions)
• MySQL

Other:
• Markdown
• Data-driven problem solving`,

    experience: `Professional Experience:

🏢 CrowdDoing - Software Developer Intern
   June 2025 - December 2025
   • Built and improved web application features using Python
   • Supported content creation and enhanced overall functionality

🏢 Bitter Brains - Software Developer Intern
   January 2025 - April 2025
   • Developed markdown editor for generating Q&A content
   • Enhanced content automation and web app functionality
   • Tech: Next.js, Markdown, Python

🏢 ZapTech - Frontend Developer Intern
   October 2024 - December 2024
   • Developed server-side rendered web apps using Next.js
   • Enhanced performance through efficient routing and dynamic content

🏢 Glitex Solutions Limited - Software Developer Intern
   January 2022 - April 2022
   • Built responsive React-based user interfaces
   • Implemented reusable components and state management`,

    contact: `Let's Connect!

📧 Email: neemamwende009@gmail.com
📱 Phone: 0792366778
💻 GitHub: github.com/neemamwende

I'm always open to discussing new opportunities, collaborations, or interesting projects. Feel free to reach out!`,

    education: `Education:

🎓 Bachelor of Applied Computer Science
   Chuka University
   2019 - 2023

📚 Kenya Certificate of Secondary Education
   St. Anne's Girls High School
   2014 - 2018

📚 Kenya Certificate of Primary Education
   Nguutani Junior Academy
   2004 - 2013`,

    references: `References:

References Available:

👨‍💼 Peter Njenga
   CEO, Glitex Solutions Limited
   📧 peter@glitexsolutions.co.ke
   📱 0707021821

👨‍🏫 Muhia Mureithi Njeru
   Teacher, St. Anne's Girls High School
   📧 matonjeru139@gmail.com
   📱 0714995319`,

    help: `Available Commands:

• about         - Learn more about me
• projects      - View my projects
• skills        - See my technical skills
• experience    - Review my work experience
• contact       - Get my contact information
• education     - View my educational background
• certifications - See certifications and references
• clear         - Clear the terminal screen
• help          - Show this help message

Type any command and press Enter to continue.`,
  };

  // Set current time only on client
  useEffect(() => {
    setCurrentTime(new Date().toLocaleString());
    const interval = setInterval(() => {
      setCurrentTime(new Date().toLocaleString());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Load welcome message on mount
  useEffect(() => {
    if (!isInitialized) {
      loadWelcomeMessage();
      setIsInitialized(true);
    }
  }, [isInitialized]);

  const loadWelcomeMessage = async () => {
    const welcomeEntry = {
      prompt: "neema@portfolio:~$ ",
      command: "",
      output: "",
      isAi: false,
    };

    setHistory([welcomeEntry]);
    setIsTyping(true);

    // Type the welcome command
    await typeCommand("welcome", 0);

    // Try to get welcome response from backend, fallback to local
    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ command: "welcome" }),
      });

      if (response.ok) {
        const data = await response.json();
        const { response: output, is_ai } = data;
        await typeText(output, is_ai, 0);
      } else {
        throw new Error("Backend response not OK");
      }
    } catch (error) {
      // Use fallback welcome message
      await typeText(fallbackResponses.welcome, false, 0);
    }

    setIsTyping(false);
  };

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [history, currentInput]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (isTyping) {
        e.preventDefault();
        return;
      }

      if (e.key === "Enter") {
        e.preventDefault();
        if (currentInput.trim()) {
          handleCommand(currentInput.trim());
          setCurrentInput("");
        }
      } else if (e.key === "Backspace") {
        e.preventDefault();
        setCurrentInput((prev) => prev.slice(0, -1));
      } else if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        setCurrentInput((prev) => prev + e.key);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [currentInput, isTyping]);

  const handleCommand = async (cmd) => {
    if (cmd.toLowerCase() === "clear") {
      setHistory([]);
      return;
    }

    // Add command to history with typing animation
    setIsTyping(true);
    const commandEntry = {
      prompt: "neema@portfolio:~$ ",
      command: "",
      output: "",
      isAi: false,
    };

    setHistory((prev) => [...prev, commandEntry]);

    // Type the command
    await typeCommand(cmd, history.length);

    // Try to get response from backend, fallback to local
    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ command: cmd }),
      });

      if (response.ok) {
        const data = await response.json();
        const { response: output, is_ai } = data;
        await typeText(output, is_ai, history.length);
      } else {
        throw new Error("Backend response not OK");
      }
    } catch (error) {
      // Use fallback response based on command
      const cmdLower = cmd.toLowerCase();
      const fallbackOutput =
        fallbackResponses[cmdLower] ||
        `Command '${cmd}' not recognized. Type 'help' to see available commands.`;

      await typeText(fallbackOutput, false, history.length);
    }

    setIsTyping(false);
  };

  const typeCommand = (cmd, historyIndex) => {
    return new Promise((resolve) => {
      let index = 0;
      const speed = 30;

      const typeChar = () => {
        if (index < cmd.length) {
          setHistory((prev) => {
            const newHistory = [...prev];
            if (newHistory[historyIndex]) {
              newHistory[historyIndex].command = cmd.substring(0, index + 1);
            }
            return newHistory;
          });
          index++;
          setTimeout(typeChar, speed);
        } else {
          resolve();
        }
      };

      typeChar();
    });
  };

  const typeText = (text, isAi, historyIndex) => {
    return new Promise((resolve) => {
      let index = 0;
      const speed = 10;

      const typeChar = () => {
        if (index < text.length) {
          setHistory((prev) => {
            const newHistory = [...prev];
            if (newHistory[historyIndex]) {
              newHistory[historyIndex].output = text.substring(0, index + 1);
              newHistory[historyIndex].isAi = isAi;
            }
            return newHistory;
          });
          index++;
          setTimeout(typeChar, speed);
        } else {
          resolve();
        }
      };

      typeChar();
    });
  };

  const commands = [
    "about",
    "projects",
    "skills",
    "experience",
    "contact",
    "education",
    "references",
  ];

  return (
    <div className="min-h-screen flex items-center justify-center font-mono text-white p-4">
      <div className="w-full max-w-4xl">
        <div className="bg-black border-4 border-[#00ff99] rounded-md overflow-hidden shadow-lg shadow-[#00ff99]/20 h-[500px] w-[900px] flex flex-col">
          {/* Command Header */}
          <div className="bg-[#001a0f] border-b-2 border-[#00ff99] p-3">
            <div className="flex items-center justify-between gap-2 text-[#00ff99] text-sm">
              {commands.map((cmd, idx) => (
                <span key={cmd}>
                  {cmd}
                  {idx < commands.length - 1 && (
                    <span className="mx-2 text-[#00ff99]/50">|</span>
                  )}
                </span>
              ))}
            </div>
          </div>

          {/* Terminal Content */}
          <div
            ref={terminalRef}
            className="pt-5 pb-5 pr-5 pl-7 flex-1 overflow-y-auto whitespace-pre-wrap break-words scrollbar-thin scrollbar-thumb-[#00ff99] scrollbar-track-black"
          >
            {history.map((entry, idx) => (
              <div key={idx}>
                <div className="mb-2">
                  <span className="text-[#00aaff] font-bold">
                    {entry.prompt}
                  </span>
                  <span className="text-[#00ff99]">{entry.command}</span>
                </div>
                {entry.output && (
                  <div className="text-white my-1 mb-4 leading-relaxed">
                    {entry.output}
                  </div>
                )}
              </div>
            ))}

            {!isTyping && (
              <div className="flex items-baseline">
                <span className="text-[#00aaff] font-bold">
                  neema@portfolio:~${" "}
                </span>
                <span className="text-[#00ff99]">{currentInput}</span>
                <span className="inline-block bg-[#00ff99] w-2 h-4 ml-0.5 animate-pulse"></span>
              </div>
            )}
          </div>
        </div>

        {currentTime && (
          <div className="text-[#00aaff] font-bold text-right text-xs mt-3">
            {currentTime}
          </div>
        )}
      </div>
    </div>
  );
}
