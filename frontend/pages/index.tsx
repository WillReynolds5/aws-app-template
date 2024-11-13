import { Button } from "@/components/ui/button";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";
import { TextScramble } from "@/components/text-scramble";
import { useState } from "react";
import { apiAuth } from "@/utils/axios";

export default function HomePage() {
  const [promptText, setPromptText] = useState("");

  const handleOptimizeClick = async () => {
    try {
      const response = await apiAuth.post("/prompt", {
        prompt: promptText,
      });

      if (response.data) {
        console.log("Optimized prompt:", response.data);
        // You can handle the response here, maybe show it in the UI
      }
    } catch (error) {
      console.error("Error optimizing prompt:", error);
      // Handle error here
    }
  };

  const slogans = [
    "Stop wasting time prompt engineering.",
    "Optimize your prompts in minutes.",
    "AI-powered prompt optimization.",
    "Craft the perfect prompt instantly.",
    "Better prompts, better results.",
  ];

  return (
    <div className="flex min-h-screen">
      <main className="flex-1 flex">
        <div className="flex-1 flex items-center justify-center">
          <div className="max-w-xl w-full space-y-8 text-center px-4">
            <h1 className="text-7xl font-extrabold tracking-tight text-zinc-800">
              AUTO
              <span className="animate-text-gradient bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 bg-clip-text bg-300% text-transparent">
                PROMPT
              </span>
            </h1>
            <p className="mx-auto max-w-2xl text-xl font-light leading-relaxed tracking-wider text-zinc-600/80 h-[2rem] flex items-center justify-center">
              <TextScramble texts={slogans} interval={5000} />
            </p>
            <div className="w-full max-w-2xl space-y-4">
              <textarea
                className="w-full rounded-lg border border-zinc-200 bg-white p-4 text-zinc-800 shadow-lg focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                placeholder="Explain your task here..."
                rows={4}
                value={promptText}
                onChange={(e) => setPromptText(e.target.value)}
              />
              <Button
                className="w-full rounded-lg bg-gradient-to-r from-purple-500/50 via-pink-500/50 to-blue-500/50 
                  bg-white/50 text-white 
                  shadow-lg transition-all hover:shadow-xl hover:opacity-90
                  border border-white/20 backdrop-blur-sm
                  hover:ring-2 hover:ring-white/20
                  animate-glow"
                size="lg"
                onClick={handleOptimizeClick}
              >
                Optimize Prompt
              </Button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
