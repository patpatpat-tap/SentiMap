"use client";
import React from 'react';

type StatsBarProps = {
  totalReports: number;
  severeCount: number;
  sarcasticCount: number;
  hotspotCount: number;
  activeTab: "dashboard" | "analytics";
  onTabChange: (tab: "dashboard" | "analytics") => void;
};

export default function StatsBar({
  totalReports = 180,
  severeCount = 140,
  sarcasticCount = 42,
  hotspotCount = 27,
  activeTab,
  onTabChange,
}: StatsBarProps) {
  const negativePct = totalReports > 0 ? Math.round((severeCount / totalReports) * 100) : 0;
  const sarcasticPct = totalReports > 0 ? Math.round((sarcasticCount / totalReports) * 100) : 0;

  return (
    <div className="bg-gradient-to-b from-[rgba(15,23,42,0.98)] to-[rgba(15,23,42,0.92)] border-b border-[rgba(96,165,250,0.1)] h-24 flex items-center px-8">
      <div className="flex items-center justify-between w-full max-w-7xl mx-auto">
        {/* Logo */}
        <div className="flex items-center gap-4">
          <div className="flex h-16 w-16 items-center justify-center">
            <img
              src="/globe.png"
              alt="SentiMap globe"
              className="h-14 w-14 object-contain"
            />
          </div>
          <div>
            <h1 className="font-display text-white text-[34px] leading-none tracking-[0.12em]">SentiMap</h1>
            <p className="text-[#4b5563] text-[11px] tracking-widest uppercase mt-0.5">
              snapshot · Apr 2026
            </p>
          </div>
        </div>

        {/* Dashboard / Analytics Toggle */}
        <div className="flex items-center gap-1 rounded-xl bg-[rgba(255,255,255,0.04)] border border-[rgba(96,165,250,0.12)] p-1">
          <button
            id="tab-dashboard"
            onClick={() => onTabChange("dashboard")}
            className={`px-5 py-2 rounded-lg text-sm font-semibold tracking-wide transition-all duration-200 ${
              activeTab === "dashboard"
                ? "bg-[rgba(96,165,250,0.18)] text-[#60a5fa] shadow-[0_0_12px_rgba(96,165,250,0.15)]"
                : "text-[#6b7280] hover:text-[#94a3b8] hover:bg-[rgba(255,255,255,0.04)]"
            }`}
          >
            <span className="flex items-center gap-2">
              <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                <path d="M1 2.5A1.5 1.5 0 012.5 1h3A1.5 1.5 0 017 2.5v3A1.5 1.5 0 015.5 7h-3A1.5 1.5 0 011 5.5v-3zm8 0A1.5 1.5 0 0110.5 1h3A1.5 1.5 0 0115 2.5v3A1.5 1.5 0 0113.5 7h-3A1.5 1.5 0 019 5.5v-3zm-8 8A1.5 1.5 0 012.5 9h3A1.5 1.5 0 017 10.5v3A1.5 1.5 0 015.5 15h-3A1.5 1.5 0 011 13.5v-3zm8 0A1.5 1.5 0 0110.5 9h3A1.5 1.5 0 0115 10.5v3A1.5 1.5 0 0113.5 15h-3A1.5 1.5 0 019 13.5v-3z"/>
              </svg>
              Dashboard
            </span>
          </button>
          <button
            id="tab-analytics"
            onClick={() => onTabChange("analytics")}
            className={`px-5 py-2 rounded-lg text-sm font-semibold tracking-wide transition-all duration-200 ${
              activeTab === "analytics"
                ? "bg-[rgba(96,165,250,0.18)] text-[#60a5fa] shadow-[0_0_12px_rgba(96,165,250,0.15)]"
                : "text-[#6b7280] hover:text-[#94a3b8] hover:bg-[rgba(255,255,255,0.04)]"
            }`}
          >
            <span className="flex items-center gap-2">
              <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                <path d="M0 11l2-2 4 4L14 3l2 2-10 10z"/>
              </svg>
              Analytics
            </span>
          </button>
        </div>

        {/* Metrics */}
        <div className="flex items-center gap-12">
          {/* Total Reports */}
          <div className="flex flex-col items-center">
            <p className="text-white font-[JetBrainsMono] text-3xl font-bold tracking-wider">{totalReports}</p>
            <p className="text-[#9ca3af] text-xs uppercase tracking-widest mt-1">Total reports</p>
          </div>

          {/* Negative */}
          <div className="flex flex-col items-center">
            <p className="text-[#ef4444] font-[JetBrainsMono] text-3xl font-bold tracking-wider">{severeCount}</p>
            <p className="text-[#9ca3af] text-xs uppercase tracking-widest mt-1">Negative</p>
            <p className="text-[#ef4444] text-[10px] font-semibold mt-0.5">{negativePct}% of total</p>
          </div>

          {/* Sarcastic */}
          <div className="flex flex-col items-center">
            <p className="text-[#c084fc] font-[JetBrainsMono] text-3xl font-bold tracking-wider">{sarcasticCount}</p>
            <p className="text-[#9ca3af] text-xs uppercase tracking-widest mt-1">Sarcastic</p>
            <p className="text-[#c084fc] text-[10px] font-semibold mt-0.5">{sarcasticPct}% of total</p>
          </div>

          {/* Locations with 2+ posts */}
          <div className="flex flex-col items-center">
            <p className="text-[#22d3ee] font-[JetBrainsMono] text-3xl font-bold tracking-wider">{hotspotCount}</p>
            <p className="text-[#9ca3af] text-xs uppercase tracking-widest mt-1 text-center leading-tight">Locations<br/>with 2+ posts</p>
          </div>
        </div>
      </div>
    </div>
  );
}
