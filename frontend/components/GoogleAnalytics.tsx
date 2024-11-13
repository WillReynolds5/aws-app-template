import Script from "next/script";
import { useEffect } from "react";
import { useRouter } from "next/router";

declare global {
  interface Window {
    gtag: (
      command: "config" | "event" | "js",
      targetId: string,
      config?: {
        page_path?: string;
        send_page_view?: boolean;
        timing_complete?: boolean;
        [key: string]: any;
      }
    ) => void;
    dataLayer: any[];
  }
}

const GoogleAnalytics = ({ ga_id }: { ga_id: string }) => {
  const router = useRouter();

  useEffect(() => {
    const handleRouteChange = (url: string) => {
      window.gtag("config", ga_id, {
        page_path: url,
        send_page_view: true,
      });
    };

    // Track route changes in SPA
    router.events.on("routeChangeComplete", handleRouteChange);

    // Cleanup
    return () => {
      router.events.off("routeChangeComplete", handleRouteChange);
    };
  }, [router.events, ga_id]);

  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${ga_id}`}
        strategy="afterInteractive"
      />
      <Script
        id="google-analytics"
        strategy="afterInteractive"
        dangerouslySetInnerHTML={{
          __html: `
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${ga_id}', {
              page_path: window.location.pathname,
              send_page_view: true,
              // Enhanced measurement settings
              timing_complete: true
            });
          `,
        }}
      />
    </>
  );
};

export default GoogleAnalytics;
