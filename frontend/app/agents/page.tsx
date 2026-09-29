"use client";

import { Bot, Zap, ShieldCheck, Database, FileText, Activity, Award } from "lucide-react";

const AGENTS = [
  { id: "agent-1", name: "Supervisor Orchestrator", node: "supervisor_node", role: "Classifies query intent and dynamically routes execution plan.", icon: Zap, color: "text-amber-400" },
  { id: "agent-2", name: "RAG Research Agent", node: "rag_node", role: "Performs vector similarity search across policy docs and extracts page citations.", icon: FileText, color: "text-cyan-400" },
  { id: "agent-3", name: "Data Analyst Agent", node: "data_analyst_node", role: "Generates read-only SQL, validates safety, executes queries and constructs charts.", icon: Database, color: "text-blue-400" },
  { id: "agent-4", name: "Pricing Intelligence Agent", node: "pricing_agent_node", role: "Analyzes margin rules vs actual transaction rates and detects anomalies.", icon: Activity, color: "text-purple-400" },
  { id: "agent-5", name: "Recommendation Agent", node: "recommendation_agent_node", role: "Synthesizes actionable business recommendations with confidence levels.", icon: Award, color: "text-emerald-400" },
  { id: "agent-6", name: "Report Generation Agent", node: "report_agent_node", role: "Assembles structured executive intelligence reports.", icon: FileText, color: "text-teal-400" },
  { id: "agent-7", name: "Responsible AI Layer", node: "responsible_ai_node", role: "Audits citation groundedness, detects hallucination risk, PII, and prompt injection.", icon: ShieldCheck, color: "text-emerald-400" }
];

export default function AgentsPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="pb-3 border-b border-slate-800">
        <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
          <Bot className="h-5 w-5 text-cyan-400" />
          <span>Autonomous Agent Fleet Registry</span>
        </h1>
        <p className="text-xs text-slate-400">
          Stateful multi-agent orchestration graph built on LangGraph framework
        </p>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {AGENTS.map((ag) => {
          const Icon = ag.icon;
          return (
            <div key={ag.id} className="p-5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-cyan-500/40 transition-all space-y-3 shadow-lg">
              <div className="flex items-center justify-between">
                <div className="h-9 w-9 rounded-xl bg-slate-850 flex items-center justify-center border border-slate-800">
                  <Icon className={`h-5 w-5 ${ag.color}`} />
                </div>
                <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  STATUS: ACTIVE
                </span>
              </div>

              <div>
                <h3 className="text-sm font-bold text-slate-100">{ag.name}</h3>
                <p className="text-[10px] font-mono text-cyan-400">{ag.node}</p>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">{ag.role}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
