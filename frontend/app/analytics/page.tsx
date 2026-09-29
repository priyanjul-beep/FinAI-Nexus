"use client";

import { useState } from "react";
import { BarChart3, Play, ShieldCheck, Database, Table, CheckCircle2 } from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

const SAMPLE_SQL = "SELECT region, product_code, SUM(revenue) as total_revenue, AVG(pricing_rate) as avg_rate FROM transactions GROUP BY region, product_code ORDER BY total_revenue DESC LIMIT 10;";

export default function AnalyticsPage() {
  const [sql, setSql] = useState(SAMPLE_SQL);
  const [data, setData] = useState<any[]>([
    { region: "US", product_code: "PRD_CREDIT_PREM", total_revenue: 4850000, avg_rate: 1.95 },
    { region: "EU", product_code: "PRD_CREDIT_PREM", total_revenue: 3200000, avg_rate: 0.85 },
    { region: "APAC_IN", product_code: "PRD_DEBIT_INST", total_revenue: 2100000, avg_rate: 0.40 },
    { region: "APAC_SG", product_code: "PRD_XBORDER_PAY", total_revenue: 1450000, avg_rate: 2.70 },
    { region: "LATAM_BR", product_code: "PRD_COMMERCIAL_CARD", total_revenue: 980000, avg_rate: 2.35 }
  ]);

  const handleRun = () => {
    // Interactive re-fetch simulation
    setData([
      { region: "US", product_code: "PRD_CREDIT_PREM", total_revenue: 4850000, avg_rate: 1.95 },
      { region: "EU", product_code: "PRD_CREDIT_PREM", total_revenue: 3200000, avg_rate: 0.85 },
      { region: "APAC_IN", product_code: "PRD_DEBIT_INST", total_revenue: 2100000, avg_rate: 0.40 },
      { region: "APAC_SG", product_code: "PRD_XBORDER_PAY", total_revenue: 1450000, avg_rate: 2.70 }
    ]);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <BarChart3 className="h-5 w-5 text-cyan-400" />
            <span>Read-Only SQL & Data Analytics Engine</span>
          </h1>
          <p className="text-xs text-slate-400">
            Natural language SQL generation, query validation guardrails & Recharts visualization
          </p>
        </div>

        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold">
          <ShieldCheck className="h-3.5 w-3.5" />
          <span>Strict READ-ONLY Enforcement Active</span>
        </div>
      </div>

      {/* Query Runner Input */}
      <div className="p-4 bg-slate-900/80 border border-slate-800 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-slate-300 flex items-center space-x-2">
            <Database className="h-4 w-4 text-cyan-400" />
            <span>SQL Query Editor</span>
          </span>
          <button
            onClick={handleRun}
            className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 text-white font-semibold text-xs shadow-md transition-all"
          >
            <Play className="h-3.5 w-3.5 fill-current" />
            <span>Execute Query</span>
          </button>
        </div>

        <textarea
          value={sql}
          onChange={(e) => setSql(e.target.value)}
          rows={3}
          className="w-full bg-slate-950 font-mono text-xs text-cyan-300 p-3 rounded-lg border border-slate-800 focus:outline-none focus:border-cyan-500/50"
        />
      </div>

      {/* Output Grid: Recharts & Data Table */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recharts */}
        <div className="p-5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-3">
          <h3 className="text-xs font-bold text-slate-200">Revenue Analytics Chart</h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="region" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", fontSize: "11px" }} />
                <Bar dataKey="total_revenue" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Data Table */}
        <div className="p-5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-3">
          <h3 className="text-xs font-bold text-slate-200 flex items-center space-x-2">
            <Table className="h-4 w-4 text-cyan-400" />
            <span>Returned Dataset ({data.length} Rows)</span>
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="p-2">Region</th>
                  <th className="p-2">Product</th>
                  <th className="p-2">Revenue ($)</th>
                  <th className="p-2">Avg Rate (%)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {data.map((r, i) => (
                  <tr key={i} className="hover:bg-slate-850/50">
                    <td className="p-2 font-bold text-slate-200">{r.region}</td>
                    <td className="p-2 text-slate-400 font-mono text-[11px]">{r.product_code}</td>
                    <td className="p-2 text-cyan-400 font-semibold">${r.total_revenue.toLocaleString()}</td>
                    <td className="p-2 text-emerald-400">{r.avg_rate}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
