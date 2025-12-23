/* eslint-disable */
/* prettier-ignore */

"use client";

export default function TerminalLoader({ text = "NEEMA" }) {
  //prettier-ignore
  const letters = {
    N: [
      "██   ██",
      "███  ██",
      "██ █ ██",
      "██  ███",
      "██   ██",
    ],
    E: [
      "██████",
      "██",
      "████",
      "██",
      "██████",
      ],
    E: [
      "██████",
      "██",
      "████",
      "██",
      "██████",
    ],
    M: [
      "██   ██",
      "███ ███",
      "██ █ ██",
      "██   ██",
      "██   ██",
    ],
    A: [
      " ███ ",
      "██ ██",
      "█████",
      "██ ██",
      "██ ██",
    ],
  };

  const rows = 5;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black z-50">
      <div className="space-y-1">
        {[...Array(rows)].map((_, rowIdx) => (
          <div key={rowIdx} className="flex gap-4">
            {text.split("").map((char, i) => (
              <span
                key={i}
                className="text-[#00ff66] font-mono text-xl font-bold glow whitespace-pre inline-block"
                style={{
                  minWidth: "10ch",
                  letterSpacing: "0px",
                  fontVariantLigatures: "none",
                }}
              >
                {letters[char]?.[rowIdx] || ""}
              </span>
            ))}
          </div>
        ))}
      </div>

      <style jsx>{`
        .glow {
          text-shadow: 0 0 10px rgba(0, 255, 102, 1),
            0 0 20px rgba(0, 255, 102, 0.8), 0 0 30px rgba(0, 255, 102, 0.6),
            0 0 40px rgba(0, 255, 102, 0.4);
          animation: flicker 1.5s infinite alternate ease-in-out;
        }

        @keyframes flicker {
          0%,
          100% {
            opacity: 1;
            text-shadow: 0 0 10px rgba(0, 255, 102, 1),
              0 0 20px rgba(0, 255, 102, 0.8), 0 0 30px rgba(0, 255, 102, 0.6),
              0 0 40px rgba(0, 255, 102, 0.4);
          }
          50% {
            opacity: 0.9;
            text-shadow: 0 0 5px rgba(0, 255, 102, 1),
              0 0 10px rgba(0, 255, 102, 0.8), 0 0 15px rgba(0, 255, 102, 0.6),
              0 0 20px rgba(0, 255, 102, 0.4);
          }
        }
      `}</style>
    </div>
  );
}
