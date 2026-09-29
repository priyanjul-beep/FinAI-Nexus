import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "FinAI Nexus - Enterprise Pricing Intelligence & Decision Automation",
  description: "Enterprise Agentic AI Platform for Pricing Intelligence & Decision Automation",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 antialiased font-sans min-h-screen flex">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <Navbar />
          <main className="flex-1 p-6 overflow-y-auto bg-gradient-to-b from-slate-950 to-slate-900">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
