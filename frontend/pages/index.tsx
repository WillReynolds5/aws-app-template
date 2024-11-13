import { useRouter } from "next/router";
import { Button } from "@/components/ui/button";

export default function Home() {
  const router = useRouter();

  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex-1">
        {/* Main Content */}
        <section className="w-full">
          <div className="container mx-auto px-4">
            <h1>Welcome</h1>
            <Button onClick={() => router.push("/auth")} className="mt-4">
              Login
            </Button>
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer className="w-full py-4">
        <div className="container mx-auto px-4">
          <p className="text-center">Footer content</p>
        </div>
      </footer>
    </div>
  );
}
