"use client";

import { Shield, User, Bell, Search } from "lucide-react";

export default function Navbar() {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/60 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30">
      {/* Search Input */}
      <div className="relative w-96">
        <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
        <input
          type="text"
          placeholder="Search pricing rules, documents, transactions..."
          className="w-full bg-slate-950/60 border border-slate-800 rounded-lg pl-9 pr-4 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors"
        />
      </div>

      {/* Right Controls */}
      <div className="flex items-center space-x-4">
        <button className="relative p-2 text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800/60 transition-colors">
          <Bell className="h-4 w-4" />
          <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-cyan-500"></span>
        </button>

        <div className="h-4 w-[1px] bg-slate-800"></div>

        {/* User Info */}
        <div className="flex items-center space-x-3">
          <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-xs font-bold text-white shadow-md">
            PA
          </div>
          <div className="text-left">
            <p className="text-xs font-semibold text-slate-200">Senior Pricing Analyst</p>
            <div className="flex items-center space-x-1">
              <Shield className="h-3 w-3 text-cyan-400" />
              <span className="text-[10px] text-cyan-400 font-medium">Role: ANALYST</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
