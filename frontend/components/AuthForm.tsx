"use client";

import * as React from "react";
import { useState } from "react";
import { signUp, signIn } from "aws-amplify/auth";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { useRouter } from "next/router";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function UserAuthForm() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [authMode, setAuthMode] = useState<"signin" | "signup">("signin");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(event: React.SyntheticEvent) {
    event.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      if (authMode === "signin") {
        const { nextStep } = await signIn({
          username: email,
          password,
        });

        if (nextStep.signInStep === "DONE") {
          router.push("/conversations");
        }
      } else {
        const { isSignUpComplete } = await signUp({
          username: email,
          password,
          options: {
            userAttributes: {
              email,
              name,
            },
          },
        });

        if (isSignUpComplete) {
          router.push("/conversations");
        }
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="grid gap-6">
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <form onSubmit={onSubmit}>
        <div className="grid gap-2">
          <div className="grid gap-1">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              placeholder="name@example.com"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          {authMode === "signup" && (
            <div className="grid gap-1">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                placeholder="Enter your name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          )}

          <div className="grid gap-1">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              placeholder="Enter your password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <Button type="submit" disabled={isLoading}>
            {authMode === "signin" ? "Sign In" : "Sign Up"}
          </Button>
        </div>
      </form>

      <Button
        variant="link"
        onClick={() => setAuthMode(authMode === "signin" ? "signup" : "signin")}
      >
        {authMode === "signin"
          ? "Don't have an account? Sign up"
          : "Already have an account? Sign in"}
      </Button>
    </div>
  );
}
