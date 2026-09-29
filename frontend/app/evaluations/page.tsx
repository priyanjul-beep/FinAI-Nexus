"use client";

import { Award, CheckCircle2, Play, AlertCircle } from "lucide-react";

const EVAL_METRICS = [
  { name: "Faithfulness", score: "98.2%", status: "PASSED", color: "text-emerald-400" },
  { name: "Answer Relevance", score: "97.5%", status: "PASSED", color: "text-cyan-400" },
  { name: "Citation Accuracy", score: "100.0%", status: "PASSED", color: "text-emerald-400" },
  { name: "Context Precision", score: "94.8%", status: "PASSED", color: "text-blue-400" },
  { name: "Hallucination Risk", score: "2.1%", status: "SAFE (<5%)", color: "text-purple-400" },
];

const TEST_CASES = [
  {
    id: "eval-1",
    question: "According to pricing policy, which products are violating pricing range?",
    expected: "US PRD_CREDIT_PREM (priced 1.70% vs min 1.85%)",
    generated: "US PRD_CREDIT_PREM priced at 1.70% is 15 bps below minimum 1.85% threshold.",
    faithfulness: 0.98,
    relevance: 0.97,
    passed: true
  },
  {
    id: "eval-2",
    question: "What is the interchange rate for US Consumer Credit?",
    expected: "1.65% + $0.10",
    generated: "US Consumer Credit interchange rate is 1.65% with $0.10 fixed fee.",
    faithfulness: 1.00,
    relevance: 0.98,
    passed: true
  }
];

export default function EvaluationsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Award className="h-5 w-5 text-cyan-400" />
            <span>LLM Response Evaluation Framework</span>
          </h1>
          <p className="text-xs text-slate-400">
            Automated quality evaluation: Faithfulness, Relevance, Citation Accuracy & Hallucination Metrics
          </p>
        </div>

        <button className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold text-xs shadow-md">
          <Play className="h-3.5 w-3.5 fill-current" />
          <span>Run Evaluation Benchmark</span>
        </button>
      </div>

      {/* Metrics Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {EVAL_METRICS.map((m) => (
          <div key={m.name} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
            <span className="text-[11px] font-medium text-slate-400">{m.name}</span>
            <div className={`text-xl font-bold ${m.color}`}>{m.score}</div>
            <span className="text-[10px] font-mono text-emerald-400">{m.status}</span>
          </div>
        ))}
      </div>

      {/* Test Cases Table */}
      <div className="p-5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-3">
        <h3 className="text-xs font-bold text-slate-200">Evaluation Test Cases Benchmark Results</h3>

        <div className="space-y-3">
          {TEST_CASES.map((tc) => (
            <div key={tc.id} className="p-4 bg-slate-950 rounded-xl border border-slate-850 space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-bold text-cyan-400">{tc.id}: "{tc.question}"</span>
                <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  PASSED
                </span>
              </div>
              <p className="text-slate-400">Expected: <span className="text-slate-200 font-mono">{tc.expected}</span></p>
              <p className="text-slate-400">Generated: <span className="text-slate-200 font-mono">{tc.generated}</span></p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
