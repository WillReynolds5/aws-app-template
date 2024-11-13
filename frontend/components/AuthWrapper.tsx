import { useEffect, useState, useCallback } from "react";
import { getCurrentUser, fetchAuthSession } from "aws-amplify/auth";
import { useRouter } from "next/router";
import React, { ReactNode } from "react";
import { ClipLoader } from "react-spinners";

const publicRoutes = [
  "/",
  "/auth",
  "/documents/terms",
  "/documents/privacy",
  "/documents/complaints",
];

// Updated LoadingSpinner component using Tailwind classes
const LoadingSpinner = () => (
  <div className="fixed inset-0 flex items-center justify-center bg-white bg-opacity-80 z-50">
    <ClipLoader color="hsl(var(--primary))" size={50} />
  </div>
);

export function AuthWrapper({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  const checkAdminPage = useCallback(async () => {
    try {
      const session = await fetchAuthSession();
      const idToken = session.tokens?.idToken;
      const payload = idToken?.payload;

      if (payload && payload["cognito:groups"]) {
        const groups = payload["cognito:groups"] as string[];
        if (groups.includes("admin")) {
          setIsAdmin(true);
        } else {
          router.push("/conversations");
        }
      } else {
        router.push("/conversations");
      }
    } catch (error) {
      router.push("/conversations");
    }
  }, [router]);

  const checkAuthStatus = useCallback(async () => {
    try {
      const user = await getCurrentUser();
      setIsAuthenticated(true);
      if (router.pathname === "/auth") {
        router.push("/conversations");
      }
    } catch (error) {
      if (!publicRoutes.includes(router.pathname)) {
        router.push("/auth");
      }
    } finally {
      setIsLoading(false);
    }
  }, [router]);

  useEffect(() => {
    const checkAuth = async () => {
      const startTime = Date.now();
      await checkAuthStatus();
      if (router.pathname.includes("admin")) {
        await checkAdminPage();
      }
      const elapsedTime = Date.now() - startTime;

      // Ensure the loading spinner is visible for at least 1 second
      if (elapsedTime < 1000) {
        setTimeout(() => setIsLoading(false), 1000 - elapsedTime);
      } else {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, [checkAuthStatus, checkAdminPage, router.pathname]);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated && !publicRoutes.includes(router.pathname)) {
    return null;
  }

  if (!isAdmin && router.pathname.includes("admin")) {
    return null;
  }

  return <>{children}</>;
}
