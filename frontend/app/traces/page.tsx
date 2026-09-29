"use client";

import { Activity, Clock, CheckCircle2, ChevronRight } from "lucide-react";

const TRACES = [
  {
    run_id: "run-98a4e1",
    query: "Which region generated highest revenue in Q2 according to pricing policy?",
    intent: "HYBRID_ANALYSIS",
    latency: "1,240ms",
    tokens: 380,
    steps: [
      { name: "Supervisor Agent", duration: "210ms", summary: "Intent classified as HYBRID_ANALYSIS" },
      { name: "RAG Research Agent", duration: "450ms", summary: "Retrieved 3 chunks from pricing_strategy_guide.md" },
      { name: "Data Analyst Agent", duration: "780ms", summary: "Executed SELECT region, SUM(revenue) FROM transactions" },
      { name: "Pricing Intelligence Agent", duration: "320ms", summary: "Detected 15 bps pricing rate violation in US Credit" },
      { name: "Responsible AI Layer", duration: "140ms", summary: "Verified citation groundedness and safety" }
    ]
  },
  {
    run_id: "run-77f2b9",
    query: "Summarize the uploaded pricing policy and identify important constraints.",
    intent: "DOCUMENT_QA",
    latency: "680ms",
    tokens: 220,
    steps: [
      { name: "Supervisor Agent", duration: "180ms", summary: "Intent classified as DOCUMENT_QA" },
      { name: "RAG Research Agent", duration: "380ms", summary: "Retrieved 4 chunks from regional_pricing_rules.md" },
      { name: "Responsible AI Layer", duration: "120ms", summary: "Validated citations" }
    ]
  }
];

export default function TracesPage() {
  return (
    <div className="space-y-6">
      <div className="pb-3 border-b border-slate-800">
        <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
          <Activity className="h-5 w-5 text-cyan-400" />
          <span>Agent Execution Trace Inspector</span>
        </h1>
        <p className="text-xs text-slate-400">
          Step-by-step agent execution waterfall, node latencies & token consumption
        </p>
      </div>

      <div className="space-y-4">
        {TRACES.map((t) => (
          <div key={t.run_id} className="p-5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-4 shadow-lg">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <span className="text-[10px] font-mono text-cyan-400 uppercase font-bold">{t.run_id} • {t.intent}</span>
                <p className="text-xs font-semibold text-slate-100">"{t.query}"</p>
              </div>

              <div className="flex items-center space-x-3 text-xs text-slate-400 font-mono">
                <span>Latency: <strong className="text-amber-400">{t.latency}</strong></span>
                <span>Tokens: <strong className="text-cyan-400">{t.tokens}</strong></span>
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-[11px] font-bold text-slate-400">Execution Steps Waterfall:</p>
              {t.steps.map((s, i) => (
                <div key={i} className="flex items-center justify-between p-2.5 rounded bg-slate-950 border border-slate-850 text-xs">
                  <div className="flex items-center space-x-2">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />
                    <span className="font-semibold text-slate-200">{s.name}</span>
                  </div>
                  <div className="flex items-center space-x-4 text-slate-400 font-mono text-[11px]">
                    <span>{s.summary}</span>
                    <span className="text-amber-400 font-bold">{s.duration}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
