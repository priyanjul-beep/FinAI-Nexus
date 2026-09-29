"use client";

import { useState } from "react";
import { FileText, Upload, Search, CheckCircle, Database, Trash2 } from "lucide-react";

const INITIAL_DOCS = [
  { id: "doc-1", filename: "pricing_strategy_guide.md", file_type: "Markdown", size: "4.2 KB", pages: 3, status: "INDEXED", created_at: "2026-09-29" },
  { id: "doc-2", filename: "interchange_policy.md", file_type: "Markdown", size: "2.8 KB", pages: 2, status: "INDEXED", created_at: "2026-09-29" },
  { id: "doc-3", filename: "regional_pricing_rules.md", file_type: "Markdown", size: "3.1 KB", pages: 2, status: "INDEXED", created_at: "2026-09-29" },
  { id: "doc-4", filename: "product_pricing_handbook.md", file_type: "Markdown", size: "2.1 KB", pages: 1, status: "INDEXED", created_at: "2026-09-29" },
  { id: "doc-5", filename: "revenue_optimization_guidelines.md", file_type: "Markdown", size: "1.9 KB", pages: 1, status: "INDEXED", created_at: "2026-09-29" },
  { id: "doc-6", filename: "risk_governance_policy.md", file_type: "Markdown", size: "1.5 KB", pages: 1, status: "INDEXED", created_at: "2026-09-29" }
];

export default function DocumentsPage() {
  const [docs, setDocs] = useState(INITIAL_DOCS);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setSearchResults([
      { filename: "pricing_strategy_guide.md", page: 1, text: "Enterprise Premium Credit (PRD_CREDIT_PREM): 1.85% - 2.25% (Recommended Baseline: 1.95%). Margin target above 42%.", score: 0.94 },
      { filename: "regional_pricing_rules.md", page: 1, text: "India (APAC_IN): Due to regulatory caps, instant debit fees cannot exceed 0.40%. Credit card processing is targeted at 1.70% - 1.90%.", score: 0.88 },
      { filename: "interchange_policy.md", page: 2, text: "PSD2 interchange caps restrict consumer card interchange to 0.20% for debit and 0.30% for credit.", score: 0.82 }
    ]);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <FileText className="h-5 w-5 text-cyan-400" />
            <span>Document Management & Vector Index</span>
          </h1>
          <p className="text-xs text-slate-400">
            Enterprise PDF/Markdown ingestion, semantic chunking & pgvector indexing
          </p>
        </div>

        <label className="cursor-pointer inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 text-white font-semibold text-xs shadow-md transition-all">
          <Upload className="h-4 w-4" />
          <span>Upload Policy PDF / MD</span>
          <input type="file" className="hidden" accept=".pdf,.md,.txt" />
        </label>
      </div>

      {/* Grid: Document List & Vector Search Tester */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Document List */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-sm font-bold text-slate-200">Indexed Platform Documents ({docs.length})</h2>

          <div className="bg-slate-900/80 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="p-3">Filename</th>
                  <th className="p-3">Type</th>
                  <th className="p-3">Pages</th>
                  <th className="p-3">Status</th>
                  <th className="p-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {docs.map((d) => (
                  <tr key={d.id} className="hover:bg-slate-850/50 transition-colors">
                    <td className="p-3 font-semibold text-slate-200 flex items-center space-x-2">
                      <FileText className="h-4 w-4 text-cyan-400" />
                      <span>{d.filename}</span>
                    </td>
                    <td className="p-3 text-slate-400">{d.file_type}</td>
                    <td className="p-3 text-slate-400">{d.pages}</td>
                    <td className="p-3">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        {d.status}
                      </span>
                    </td>
                    <td className="p-3 text-right">
                      <button className="text-slate-500 hover:text-red-400 p-1">
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Vector Search Tester */}
        <div className="space-y-4">
          <h2 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
            <Database className="h-4 w-4 text-cyan-400" />
            <span>Semantic Vector Search Tester</span>
          </h2>

          <form onSubmit={handleSearch} className="space-y-2">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Enter query to test RAG top-k retrieval..."
                className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-3 pr-9 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50"
              />
              <button type="submit" className="absolute right-2 top-2 text-cyan-400">
                <Search className="h-4 w-4" />
              </button>
            </div>
          </form>

          {searchResults.length > 0 && (
            <div className="space-y-2">
              <p className="text-[11px] font-bold text-slate-400">Top-k Retrieved Chunks:</p>
              {searchResults.map((res, i) => (
                <div key={i} className="p-3 bg-slate-900 border border-slate-800 rounded-xl space-y-1 text-xs">
                  <div className="flex items-center justify-between text-[10px] text-cyan-400 font-bold">
                    <span>{res.filename} (Page {res.page})</span>
                    <span>Similarity: {(res.score * 100).toFixed(1)}%</span>
                  </div>
                  <p className="text-slate-300 italic">"{res.text}"</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
