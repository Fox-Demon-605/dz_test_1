"use client";

import { useEffect, useState } from "react";

export function MSWProvider({ children }: { children: React.ReactNode }) {
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    async function initMSW() {
      const { worker } = await import("./browser");
      await worker.start({
        onUnhandledRequest: "bypass",
        quiet: true,
      });
      setIsReady(true);
    }

    initMSW();
  }, []);

  if (!isReady) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  return <>{children}</>;
}
