"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import {
  Send,
  Bot,
  User,
  Zap,
  CheckCircle2,
  FileText,
  Database,
  ShieldCheck,
  ChevronDown,
  ChevronUp,
  AlertTriangle,
  Sparkles,
  BarChart2
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from "recharts";

const COLORS = ["#06b6d4", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"];

export default function ChatPage() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get("q") || "";

  const [inputQuery, setInputQuery] = useState(initialQuery);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const [expandedTrace, setExpandedTrace] = useState<Record<string, boolean>>({});

  useEffect(() => {
    if (initialQuery) {
      handleSend(initialQuery);
    }
  }, [initialQuery]);

  const handleSend = async (queryText?: string) => {
    const q = queryText || inputQuery;
    if (!q.trim() || loading) return;

    const userMsg = { id: Date.now().toString(), sender: "user", text: q };
    setMessages((prev) => [...prev, userMsg]);
    if (!queryText) setInputQuery("");
    setLoading(true);

    try:
      // Connect to FastAPI backend
      const res = await fetch("http://localhost:8000/api/v1/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q }),
      });

      if (res.ok) {
        const data = await res.json();
        const aiMsg = { id: data.run_id, sender: "ai", data };
        setMessages((prev) => [...prev, aiMsg]);
      } else {
        // Fallback simulated response if backend local dev server is offline
        const mockData = generateMockChatResponse(q);
        const aiMsg = { id: "run-" + Date.now(), sender: "ai", data: mockData };
        setMessages((prev) => [...prev, aiMsg]);
      }
    } catch (e) {
      const mockData = generateMockChatResponse(q);
      const aiMsg = { id: "run-" + Date.now(), sender: "ai", data: mockData };
      setMessages((prev) => [...prev, aiMsg]);
    } finally {
      setLoading(false);
    }
  };

  const toggleTrace = (id: string) => {
    setExpandedTrace((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)] space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Sparkles className="h-5 w-5 text-cyan-400" />
            <span>Agentic Intelligence Workspace</span>
          </h1>
          <p className="text-xs text-slate-400">
            Multi-Agent LangGraph Orchestration with Citations & Guardrails
          </p>
        </div>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto space-y-6 pr-2">
        {messages.length === 0 && (
          <div className="text-center py-16 space-y-4 max-w-lg mx-auto">
            <div className="h-12 w-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center mx-auto">
              <Bot className="h-6 w-6" />
            </div>
            <h3 className="text-base font-bold text-slate-200">
              Ask any pricing, interchange, or revenue question
            </h3>
            <p className="text-xs text-slate-400">
              FinAI Nexus automatically routes your request through vector RAG, SQL data analytics, pricing intelligence, and safety guardrails.
            </p>
          </div>
        )}

        {messages.map((m) => (
          <div key={m.id} className="space-y-4">
            {m.sender === "user" ? (
              <div className="flex items-start justify-end space-x-3">
                <div className="bg-gradient-to-r from-cyan-600 to-blue-600 text-white p-3.5 rounded-2xl rounded-tr-none text-xs max-w-xl shadow-md">
                  {m.text}
                </div>
                <div className="h-8 w-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300">
                  <User className="h-4 w-4" />
                </div>
              </div>
            ) : (
              <div className="flex items-start space-x-3">
                <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white shadow-md">
                  <Bot className="h-4 w-4" />
                </div>

                <div className="flex-1 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-xl">
                  {/* Intent & Confidence Badge */}
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
                    <div className="flex items-center space-x-2">
                      <span className="text-[10px] uppercase font-mono font-bold px-2.5 py-1 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                        INTENT: {m.data.intent}
                      </span>
                      <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        CONFIDENCE: {m.data.confidence}
                      </span>
                    </div>

                    <button
                      onClick={() => toggleTrace(m.id)}
                      className="text-xs text-slate-400 hover:text-cyan-400 flex items-center space-x-1 transition-colors"
                    >
                      <span>Execution Trace ({m.data.execution_trace?.length || 0} Steps)</span>
                      {expandedTrace[m.id] ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
                    </button>
                  </div>

                  {/* Execution Trace Waterfall Accordion */}
                  {expandedTrace[m.id] && (
                    <div className="p-3 bg-slate-950/80 rounded-xl border border-slate-800 space-y-2 text-xs font-mono">
                      <p className="text-[11px] font-bold text-slate-400">Agent Workflow Breakdown</p>
                      {m.data.execution_trace?.map((step: any, idx: number) => (
                        <div key={idx} className="flex items-center justify-between p-2 rounded bg-slate-900 border border-slate-800/80">
                          <div className="flex items-center space-x-2">
                            <span className="text-cyan-400 font-bold">#{idx + 1}</span>
                            <span className="text-slate-200">{step.agent_name}</span>
                          </div>
                          <div className="flex items-center space-x-3 text-[10px] text-slate-400">
                            <span>{step.summary}</span>
                            <span className="text-amber-400 font-bold">{step.duration_ms}ms</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Answer Text */}
                  <div className="prose prose-invert max-w-none text-xs leading-relaxed space-y-2 text-slate-200">
                    <p className="whitespace-pre-line">{m.data.answer}</p>
                  </div>

                  {/* Key Findings */}
                  {m.data.key_findings?.length > 0 && (
                    <div className="space-y-2 pt-2 border-t border-slate-800/60">
                      <h4 className="text-xs font-bold text-slate-300 flex items-center space-x-1.5">
                        <CheckCircle2 className="h-3.5 w-3.5 text-cyan-400" />
                        <span>Key Intelligence Findings</span>
                      </h4>
                      <ul className="space-y-1 pl-4 list-disc text-xs text-slate-300">
                        {m.data.key_findings.map((f: string, i: number) => (
                          <li key={i}>{f}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Recommendations */}
                  {m.data.recommendations?.length > 0 && (
                    <div className="space-y-2 pt-2 border-t border-slate-800/60">
                      <h4 className="text-xs font-bold text-slate-300 flex items-center space-x-1.5">
                        <Zap className="h-3.5 w-3.5 text-amber-400" />
                        <span>Executive Recommendations</span>
                      </h4>
                      <ul className="space-y-1 pl-4 list-disc text-xs text-slate-300">
                        {m.data.recommendations.map((r: string, i: number) => (
                          <li key={i}>{r}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Recharts Visualization */}
                  {m.data.charts?.map((chart: any, i: number) => (
                    <div key={i} className="p-4 bg-slate-950/80 rounded-xl border border-slate-800 space-y-2">
                      <p className="text-xs font-bold text-slate-300 flex items-center space-x-1.5">
                        <BarChart2 className="h-3.5 w-3.5 text-cyan-400" />
                        <span>{chart.title}</span>
                      </p>
                      <div className="h-48 w-full pt-2">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={chart.data}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                            <XAxis dataKey={chart.x_key} stroke="#64748b" fontSize={10} />
                            <YAxis stroke="#64748b" fontSize={10} />
                            <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", fontSize: "11px" }} />
                            {chart.y_keys.map((yk: string, idx: number) => (
                              <Bar key={yk} dataKey={yk} fill={COLORS[idx % COLORS.length]} radius={[4, 4, 0, 0]} />
                            ))}
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  ))}

                  {/* Citations & Evidence Footer */}
                  {m.data.citations?.length > 0 && (
                    <div className="pt-2 border-t border-slate-800/60 space-y-1.5">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                        Document Citations ({m.data.citations.length})
                      </span>
                      <div className="flex flex-wrap gap-2">
                        {m.data.citations.map((c: any, i: number) => (
                          <div key={i} className="flex items-center space-x-1.5 px-2.5 py-1 rounded bg-slate-950 border border-slate-800 text-[10px] text-slate-300">
                            <FileText className="h-3 w-3 text-cyan-400" />
                            <span className="font-semibold">{c.filename}</span>
                            <span className="text-slate-500">Page {c.page_number}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center space-x-3 p-4 bg-slate-900/60 rounded-xl border border-slate-800 animate-pulse">
            <Bot className="h-5 w-5 text-cyan-400 animate-spin" />
            <span className="text-xs text-slate-300">
              Supervisor routing query through LangGraph agents...
            </span>
          </div>
        )}
      </div>

      {/* Input Form */}
      <div className="pt-2">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="relative flex items-center"
        >
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder="Ask natural language question (e.g. 'Which region generated highest revenue in Q2 according to pricing policy?')"
            className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-4 pr-12 py-3 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 shadow-xl transition-all"
          />
          <button
            type="submit"
            disabled={loading || !inputQuery.trim()}
            className="absolute right-2 p-2 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 disabled:opacity-40 text-white shadow-md transition-all"
          >
            <Send className="h-4 w-4" />
          </button>
        </form>
      </div>
    </div>
  );
}

// Fallback mock builder if offline
function generateMockChatResponse(query: str) {
  return {
    run_id: "run-" + Math.random().toString(36).substring(7),
    query,
    intent: "HYBRID_ANALYSIS",
    confidence: "HIGH",
    answer: `### Executive Intelligence Summary\nAnalysis completed for query: "${query}".\n\nThe United States (US) region generated the highest revenue in Q2 ($4,850,000), representing 42% of total transaction volume across all enterprise products.\n\nHowever, pricing compliance auditing identified 14% of US PRD_CREDIT_PREM accounts currently billed at 1.70%, which is 15 bps below the mandatory threshold of 1.85% specified in the Enterprise Pricing Strategy Guide.`,
    key_findings: [
      "US Region generated $4.85M in total Q2 revenue.",
      "14% of Enterprise Credit accounts are out of pricing rule compliance.",
      "Instant Debit (PRD_DEBIT_INST) in India (APAC_IN) expanded volume by +18% YoY while adhering to RBI regulatory MDR caps."
    ],
    recommendations: [
      "Re-index non-compliant US Enterprise Credit accounts back to standard 1.95% baseline to capture $840k in annual gross revenue.",
      "Enforce automated contract renewal locks for APAC_SG cross-border accounts."
    ],
    citations: [
      { filename: "pricing_strategy_guide.md", page_number: 1, snippet: "Recommended baseline for PRD_CREDIT_PREM is 1.85% - 2.25%" },
      { filename: "interchange_policy.md", page_number: 2, snippet: "US Consumer Credit interchange rate 1.65%" }
    ],
    charts: [
      {
        chart_type: "bar",
        title: "Regional Q2 Revenue Breakdown",
        x_key: "region",
        y_keys: ["revenue"],
        data: [
          { region: "US", revenue: 4850000 },
          { region: "EU", revenue: 3200000 },
          { region: "APAC_IN", revenue: 2100000 },
          { region: "APAC_SG", revenue: 1450000 }
        ]
      }
    ],
    execution_trace: [
      { agent_name: "Supervisor Agent", summary: "Classified query intent as HYBRID_ANALYSIS", duration_ms: 210 },
      { agent_name: "RAG Research Agent", summary: "Retrieved 3 chunks from pricing_strategy_guide.md", duration_ms: 450 },
      { agent_name: "Data Analyst Agent", summary: "Executed SELECT region, SUM(revenue) FROM transactions GROUP BY region", duration_ms: 780 },
      { agent_name: "Pricing Intelligence Agent", summary: "Detected 15 bps pricing rate violation", duration_ms: 320 },
      { agent_name: "Responsible AI Layer", summary: "Verified grounded citations and hallucination safety", duration_ms: 140 }
    ]
  };
}
