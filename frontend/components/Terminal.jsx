// components/Terminal.jsx
"use client";
import { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function Terminal() {
  const [history, setHistory] = useState([]);
  const [currentInput, setCurrentInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const [currentTime, setCurrentTime] = useState("");
  const terminalRef = useRef(null);

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

    // Get welcome response from backend
    try {
      const response = await axios.post("http://localhost:8000/query", {
        command: "welcome",
      });

      const { response: output, is_ai } = response.data;
      await typeText(output, is_ai, 0);
    } catch (error) {
      // Fallback welcome message if backend is not available
      const fallbackMessage = `Hi, I'm Neema Mwende, a Software & AI Engineer.

Welcome to my interactive 'AI powered' portfolio terminal!
Type 'help' to see available commands.

Type any command to continue..`;
      await typeText(fallbackMessage, false, 0);
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

    try {
      const response = await axios.post("http://localhost:8000/query", {
        command: cmd,
      });

      const { response: output, is_ai } = response.data;

      // Type the output
      await typeText(output, is_ai, history.length);
      setIsTyping(false);
    } catch (error) {
      setHistory((prev) => {
        const newHistory = [...prev];
        newHistory[newHistory.length - 1].output = `Error: ${error.message}`;
        return newHistory;
      });
      setIsTyping(false);
    }
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
    "certifications",
  ];

  return (
    <div className="min-h-screen p-15 w-350 font-mono text-white">
      <div className="max-w-4xl mx-auto">
        <div className="bg-black border-4 border-[#00ff99] rounded-md overflow-hidden shadow-lg shadow-[#00ff99]/20">
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
            className="p-5 min-h-[500px] max-h-[600px] overflow-y-auto whitespace-pre-wrap break-words scrollbar-thin scrollbar-thumb-[#00ff99] scrollbar-track-black"
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
          <div className="text-[#00ff99] text-right text-xs mt-3">
            {currentTime}
          </div>
        )}
      </div>
    </div>
  );
}
