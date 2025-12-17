// components/Terminal.jsx
"use client";
import { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function Terminal() {
  const [history, setHistory] = useState([
    {
      prompt: "neema@portfolio:~$ ",
      command: "welcome",
      output: `Hi, I'm Neema Mwende, a Software & AI Engineer.

Welcome to my interactive 'AI powered' portfolio terminal!
Type 'help' to see available commands.

Type any command to continue..`,
      isAi: false,
    },
  ]);
  const [currentInput, setCurrentInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const terminalRef = useRef(null);

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
      setHistory([
        {
          prompt: "neema@portfolio:~$ ",
          command: "",
          output: `Hi, I'm Neema Mwende, a Software & AI Engineer.

Welcome to my interactive 'AI powered' portfolio terminal!
Type 'help' to see available commands.

Type any command to continue..`,
          isAi: false,
        },
      ]);
      return;
    }

    setHistory((prev) => [
      ...prev,
      {
        prompt: "neema@portfolio:~$ ",
        command: cmd,
        output: "",
        isAi: false,
      },
    ]);

    try {
      const response = await axios.post("http://localhost:8000/query", {
        command: cmd,
      });

      const { response: output, is_ai } = response.data;

      setIsTyping(true);
      await typeText(output, is_ai);
      setIsTyping(false);
    } catch (error) {
      setHistory((prev) => {
        const newHistory = [...prev];
        newHistory[newHistory.length - 1].output = `Error: ${error.message}`;
        return newHistory;
      });
    }
  };

  const typeText = (text, isAi) => {
    return new Promise((resolve) => {
      let index = 0;
      const speed = 10;

      const typeChar = () => {
        if (index < text.length) {
          setHistory((prev) => {
            const newHistory = [...prev];
            newHistory[newHistory.length - 1].output = text.substring(
              0,
              index + 1
            );
            newHistory[newHistory.length - 1].isAi = isAi;
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

  return (
    <div className="bg-black min-h-screen p-5 font-mono text-white">
      <div
        ref={terminalRef}
        className="bg-black border border-[#00ff99] rounded-md p-5 min-h-[500px] max-h-[600px] overflow-y-auto whitespace-pre-wrap break-words scrollbar-thin scrollbar-thumb-[#00ff99] scrollbar-track-black"
      >
        {history.map((entry, idx) => (
          <div key={idx}>
            <div className="mb-2">
              <span className="text-[#00aaff] font-bold">{entry.prompt}</span>
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
            <span className="inline-block bg-[#00ff99] w-2 h-4 ml-0.5 animate-blink"></span>
          </div>
        )}
      </div>

      <div className="text-[#00ff99] text-right text-xs mt-2">
        {new Date().toLocaleString()}
      </div>
    </div>
  );
}
