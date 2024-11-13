import "../styles/globals.css";
import type { AppProps } from "next/app";
import { AuthWrapper } from "@/components/AuthWrapper";
import GoogleAnalytics from "@/components/GoogleAnalytics";

import "../amplify";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      {/* <GoogleAnalytics ga_id="" /> */}
      <AuthWrapper>
        <Component {...pageProps} />
      </AuthWrapper>
    </>
  );
}
