import { useEffect, useState } from "react";

const characters = "abcdefghijklmnopqrstuvwxyz#%&^+=-";

interface TextScrambleProps {
  texts: string[];
  interval?: number;
}

export function TextScramble({ texts, interval = 3000 }: TextScrambleProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [displayText, setDisplayText] = useState(texts[0]);
  const [isScrambling, setIsScrambling] = useState(false);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setIsScrambling(true);
      let iterations = 0;
      const nextIndex = (currentIndex + 1) % texts.length;

      const scrambleId = setInterval(() => {
        setDisplayText((prev) => {
          const next = texts[nextIndex];
          const result = next
            .split("")
            .map((letter, idx) => {
              if (iterations > idx) return letter;
              return characters[Math.floor(Math.random() * characters.length)];
            })
            .join("");

          if (iterations >= next.length) {
            clearInterval(scrambleId);
            setIsScrambling(false);
            setCurrentIndex(nextIndex);
          }
          iterations += 1;
          return result;
        });
      }, 20);
    }, interval);

    return () => clearInterval(intervalId);
  }, [currentIndex, texts, interval]);

  return (
    <span
      className={`transition-all duration-200 ${
        isScrambling ? "text-purple-500" : ""
      }`}
    >
      {displayText}
    </span>
  );
}
