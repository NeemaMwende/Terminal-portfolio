// import Terminal from "../components/Terminal";

// export default function Home() {
//   return (
//     <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
//       <Terminal />
//     </div>
//   );
// }
"use client";

import { useEffect, useState } from "react";
import Terminal from "../components/Terminal";
import TerminalLoader from "../components/TerminalLoader";

export default function Page() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000); // 1 second loader

    return () => clearTimeout(timer);
  }, []);

  return (
    <>
      {loading && <TerminalLoader text="NEEMA" />}
      {!loading && <Terminal />}
    </>
  );
}
