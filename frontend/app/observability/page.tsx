"use client";

import { ShieldCheck, Activity, Zap, DollarSign, BarChart2 } from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

const LATENCY_DATA = [
  { agent: "Supervisor", latency: 210 },
  { agent: "RAG Researcher", latency: 450 },
  { agent: "Data Analyst", latency: 780 },
  { agent: "Pricing Agent", latency: 320 },
  { agent: "Recommendation", latency: 290 },
  { agent: "Responsible AI", latency: 140 }
];

export default function ObservabilityPage() {
  return (
    <div className="space-y-6">
      <div className="pb-3 border-b border-slate-800">
        <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
          <ShieldCheck className="h-5 w-5 text-cyan-400" />
          <span>AI Observability & Cost Tracking</span>
        </h1>
        <p className="text-xs text-slate-400">
          OpenTelemetry-compatible latency tracking, token consumption & LLMOps telemetry
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
          <span className="text-[11px] text-slate-400">Total Tokens Consumed</span>
          <div className="text-xl font-bold text-cyan-400">148,500</div>
        </div>
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
          <span className="text-[11px] text-slate-400">Estimated Cost</span>
          <div className="text-xl font-bold text-emerald-400">$1.4850 USD</div>
        </div>
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
          <span className="text-[11px] text-slate-400">Avg Request Latency</span>
          <div className="text-xl font-bold text-amber-400">1.24s</div>
        </div>
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
          <span className="text-[11px] text-slate-400">RAG Retrieval Rate</span>
          <div className="text-xl font-bold text-purple-400">100% Success</div>
        </div>
      </div>

      <div className="p-5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-3">
        <h3 className="text-xs font-bold text-slate-200">Agent Latency Breakdown (Milliseconds)</h3>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={LATENCY_DATA}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="agent" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} />
              <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", fontSize: "11px" }} />
              <Bar dataKey="latency" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
