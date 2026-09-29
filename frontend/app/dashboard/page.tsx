"use client";

import Link from "next/link";
import {
  Bot,
  FileText,
  Activity,
  Zap,
  Award,
  ArrowUpRight,
  ShieldCheck,
  TrendingUp,
  AlertTriangle,
  Play
} from "lucide-react";

const METRICS = [
  { name: "Total AI Requests", value: "1,248", change: "+14.2%", icon: Activity, color: "text-cyan-400" },
  { name: "Active Agents", value: "7 Agents", change: "100% Operational", icon: Bot, color: "text-emerald-400" },
  { name: "Indexed Policy Docs", value: "6 Documents", change: "28 Vector Chunks", icon: FileText, color: "text-blue-400" },
  { name: "Average Latency", value: "1.24s", change: "p95: 2.85s", icon: Zap, color: "text-amber-400" },
  { name: "Evaluation Score", value: "98.5%", change: "Faithfulness 0.98", icon: Award, color: "text-purple-400" },
  { name: "Safety & Guardrails", value: "0 Violations", change: "PII & Injection Safe", icon: ShieldCheck, color: "text-teal-400" },
];

const DEMO_SCENARIOS = [
  {
    title: "Scenario 1: Regional Revenue",
    query: "Which region generated the highest revenue in Q2?",
    type: "Data Analysis (SQL)"
  },
  {
    title: "Scenario 2: Revenue Decline",
    query: "Why did revenue decline in Region A?",
    type: "Pricing Analysis"
  },
  {
    title: "Scenario 3: Policy Violation",
    query: "According to the pricing policy, which products are outside the recommended pricing range?",
    type: "Hybrid RAG + SQL"
  },
  {
    title: "Scenario 4: Regional Strategy",
    query: "Compare pricing strategy across India and Singapore.",
    type: "Multi-Region RAG"
  },
  {
    title: "Scenario 5: Price vs Volume Elasticity",
    query: "Find products where pricing increased but transaction volume decreased.",
    type: "Pricing Intelligence"
  },
  {
    title: "Scenario 6: Executive Q2 Report",
    query: "Generate an executive pricing performance report for Q2.",
    type: "Full Report Generation"
  },
  {
    title: "Scenario 7: Policy Constraints",
    query: "Summarize the uploaded pricing policy and identify important constraints.",
    type: "Document Summary RAG"
  },
  {
    title: "Scenario 8: Hybrid RAG + SQL Reasoning",
    query: "According to the pricing policy, what is the recommended pricing range for Product X and how does our current pricing compare?",
    type: "Full Hybrid Orchestration"
  },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex items-center justify-between bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950 p-6 rounded-2xl border border-slate-800 shadow-xl">
        <div className="space-y-1">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-semibold">
            <Zap className="h-3.5 w-3.5" />
            <span>Multi-Agent LangGraph System Active</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            FinAI Nexus Intelligence Center
          </h1>
          <p className="text-xs text-slate-400">
            Enterprise Decision Automation & Multi-Agent Pricing Analytics Platform
          </p>
        </div>

        <Link
          href="/chat"
          className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold text-xs transition-all shadow-lg shadow-cyan-500/25"
        >
          <span>Launch Agentic Workspace</span>
          <ArrowUpRight className="h-4 w-4" />
        </Link>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {METRICS.map((m) => {
          const Icon = m.icon;
          return (
            <div key={m.name} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2 hover:border-slate-700 transition-colors">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-medium text-slate-400">{m.name}</span>
                <Icon className={`h-4 w-4 ${m.color}`} />
              </div>
              <div className="text-lg font-bold text-slate-100">{m.value}</div>
              <div className="text-[10px] text-cyan-400 font-medium">{m.change}</div>
            </div>
          );
        })}
      </div>

      {/* Main Content Grid: Scenario Launcher & Multi-Agent Status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Scenario Launcher */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-slate-200 flex items-center space-x-2">
              <Play className="h-4 w-4 text-cyan-400" />
              <span>Production Demo Scenarios</span>
            </h2>
            <span className="text-xs text-slate-400">Click to execute scenario in Agentic Chat</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {DEMO_SCENARIOS.map((sc) => (
              <Link
                key={sc.title}
                href={`/chat?q=${encodeURIComponent(sc.query)}`}
                className="p-4 rounded-xl bg-slate-900/70 border border-slate-800/90 hover:border-cyan-500/40 hover:bg-slate-900 transition-all group space-y-2 block"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-cyan-400 group-hover:text-cyan-300">
                    {sc.title}
                  </span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">
                    {sc.type}
                  </span>
                </div>
                <p className="text-xs text-slate-300 line-clamp-2 italic">
                  "{sc.query}"
                </p>
              </Link>
            ))}
          </div>
        </div>

        {/* Multi-Agent System Graph Status */}
        <div className="space-y-4">
          <h2 className="text-base font-bold text-slate-200 flex items-center space-x-2">
            <Bot className="h-4 w-4 text-emerald-400" />
            <span>Autonomous Agent Fleet</span>
          </h2>

          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3">
            {[
              { name: "Supervisor Orchestrator", role: "Dynamic Intent Routing", status: "ONLINE" },
              { name: "RAG Research Agent", role: "Vector Search & Citations", status: "ONLINE" },
              { name: "Data Analyst Agent", role: "Read-Only NL-to-SQL", status: "ONLINE" },
              { name: "Pricing Intelligence", role: "Policy & Margin Auditor", status: "ONLINE" },
              { name: "Recommendation Engine", role: "Actionable Insights", status: "ONLINE" },
              { name: "Report Generation", role: "Executive Report Generator", status: "ONLINE" },
              { name: "Responsible AI Layer", role: "Hallucination & PII Audit", status: "ONLINE" },
            ].map((ag) => (
              <div key={ag.name} className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-850">
                <div>
                  <p className="text-xs font-semibold text-slate-200">{ag.name}</p>
                  <p className="text-[10px] text-slate-400">{ag.role}</p>
                </div>
                <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  {ag.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
