"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  MessageSquareCode,
  FileText,
  BarChart3,
  Bot,
  Activity,
  Award,
  ShieldCheck,
  Settings,
  Zap
} from "lucide-react";

const NAV_ITEMS = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Agentic Chat", href: "/chat", icon: MessageSquareCode },
  { name: "Documents & RAG", href: "/documents", icon: FileText },
  { name: "Data Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Agents Registry", href: "/agents", icon: Bot },
  { name: "Execution Traces", href: "/traces", icon: Activity },
  { name: "LLM Evaluations", href: "/evaluations", icon: Award },
  { name: "AI Observability", href: "/observability", icon: ShieldCheck },
  { name: "Settings", href: "/settings", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-slate-900/90 border-r border-slate-800 text-slate-200 flex flex-col justify-between h-screen sticky top-0 backdrop-blur-md z-40">
      <div>
        {/* Brand Header */}
        <div className="p-6 border-b border-slate-800/80 flex items-center space-x-3">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Zap className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
              FinAI Nexus
            </h1>
            <p className="text-xs text-cyan-400 font-medium tracking-wide">Enterprise Pricing AI</p>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="p-4 space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? "bg-gradient-to-r from-cyan-500/20 to-blue-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm"
                    : "text-slate-400 hover:text-slate-100 hover:bg-slate-800/60"
                }`}
              >
                <Icon className={`h-4 w-4 ${isActive ? "text-cyan-400" : "text-slate-400"}`} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Footer Info Badge */}
      <div className="p-4 border-t border-slate-800/80">
        <div className="p-3 bg-slate-850/70 rounded-xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400 font-medium">Orchestrator</span>
            <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              LangGraph Active
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400 font-medium">Mode</span>
            <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              DEMO_MODE=true
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}
