"use client";

import { useState } from "react";
import { Settings, Save, ShieldCheck, Cpu } from "lucide-react";

export default function SettingsPage() {
  const [provider, setProvider] = useState("mock");
  const [model, setModel] = useState("gpt-4o");
  const [topK, setTopK] = useState(5);
  const [strictCitations, setStrictCitations] = useState(true);

  return (
    <div className="space-y-6 max-w-3xl">
      <div className="pb-3 border-b border-slate-800">
        <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
          <Settings className="h-5 w-5 text-cyan-400" />
          <span>Platform Settings & Configuration</span>
        </h1>
        <p className="text-xs text-slate-400">
          LLM Providers, Vector Search Thresholds & Responsible AI Guardrail Controls
        </p>
      </div>

      <div className="space-y-5">
        {/* LLM Provider */}
        <div className="p-5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-3">
          <h3 className="text-xs font-bold text-slate-200 flex items-center space-x-2">
            <Cpu className="h-4 w-4 text-cyan-400" />
            <span>LLM Provider Configuration</span>
          </h3>

          <div className="grid grid-cols-3 gap-3">
            {[
              { id: "mock", name: "Mock / Offline", desc: "Zero-credential DEMO_MODE" },
              { id: "openai", name: "OpenAI GPT-4o", desc: "OpenAI API Provider" },
              { id: "gemini", name: "Google Gemini", desc: "Gemini 1.5 Pro Provider" }
            ].map((p) => (
              <button
                key={p.id}
                onClick={() => setProvider(p.id)}
                className={`p-3 rounded-xl border text-left space-y-1 transition-all ${
                  provider === p.id
                    ? "bg-cyan-500/10 border-cyan-500 text-cyan-300"
                    : "bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                <div className="text-xs font-bold">{p.name}</div>
                <div className="text-[10px] text-slate-500">{p.desc}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Vector Search Parameters */}
        <div className="p-5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-3">
          <h3 className="text-xs font-bold text-slate-200">RAG Vector Search Parameters</h3>

          <div className="space-y-2">
            <label className="text-xs text-slate-400 flex items-center justify-between">
              <span>Top-k Context Retrieval Chunks ({topK})</span>
            </label>
            <input
              type="range"
              min="1"
              max="10"
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="w-full"
            />
          </div>
        </div>

        {/* Guardrails */}
        <div className="p-5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-3">
          <h3 className="text-xs font-bold text-slate-200 flex items-center space-x-2">
            <ShieldCheck className="h-4 w-4 text-emerald-400" />
            <span>Responsible AI Guardrails</span>
          </h3>

          <div className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-850">
            <div>
              <p className="text-xs font-semibold text-slate-200">Strict Citation Verification</p>
              <p className="text-[10px] text-slate-400">Flag responses generated without direct document context</p>
            </div>
            <input
              type="checkbox"
              checked={strictCitations}
              onChange={(e) => setStrictCitations(e.target.checked)}
              className="h-4 w-4 rounded accent-cyan-500"
            />
          </div>
        </div>

        <button className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 text-white font-bold text-xs shadow-lg transition-all">
          <Save className="h-4 w-4" />
          <span>Save Settings</span>
        </button>
      </div>
    </div>
  );
}
