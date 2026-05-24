"use client";
import React from "react";

type SidebarProps = {
  activeTab: "dashboard" | "analytics";
  onTabChange: (tab: "dashboard" | "analytics") => void;
};

const ICONS = {
  map: "M12 22s8-4.5 8-10A8 8 0 104 12c0 5.5 8 10 8 10zm0-11a3 3 0 110-6 3 3 0 010 6z",
  layers: "M12 3l9 5-9 5-9-5 9-5zm0 10l9 5-9 5-9-5 9-5z",
  chart: "M4 19h16M7 16V8m5 8V5m5 11v-6",
  settings: "M12 15.5a3.5 3.5 0 100-7 3.5 3.5 0 000 7zm7.4-3a6.6 6.6 0 00.04-.7 6.6 6.6 0 00-.04-.7l2.1-1.6a.7.7 0 00.16-.9l-2-3.5a.7.7 0 00-.86-.3l-2.5 1a6.6 6.6 0 00-1.2-.7l-.4-2.7a.7.7 0 00-.7-.6h-4a.7.7 0 00-.7.6l-.4 2.7c-.43.2-.83.43-1.2.7l-2.5-1a.7.7 0 00-.86.3l-2 3.5a.7.7 0 00.16.9l2.1 1.6c-.03.23-.04.46-.04.7s.01.47.04.7l-2.1 1.6a.7.7 0 00-.16.9l2 3.5c.2.34.6.48.86.3l2.5-1c.37.27.77.5 1.2.7l.4 2.7c.06.34.36.6.7.6h4c.35 0 .64-.26.7-.6l.4-2.7c.43-.2.83-.43 1.2-.7l2.5 1c.26.18.66.04.86-.3l2-3.5a.7.7 0 00-.16-.9l-2.1-1.6z",
};

export default function Sidebar({
  activeTab,
  onTabChange,
}: SidebarProps) {
  return (
    <aside
      style={{
        width: "92px",
        minWidth: "92px",
        height: "100vh",
        background: "transparent",
        display: "flex",
        flexDirection: "column",
        position: "fixed",
        top: 0,
        left: 0,
        zIndex: 100,
        pointerEvents: "none",
      }}
    >
      <div style={{
        position: "absolute",
        top: 10,
        left: 8,
        width: 76,
        height: 160,
        borderRadius: 28,
        background: "radial-gradient(circle at 50% 30%, rgba(56,189,248,0.35), rgba(14,165,233,0.08) 60%, transparent 70%)",
        filter: "blur(10px)",
        opacity: 0.9,
        zIndex: 0,
      }} />
      <div style={{
        margin: "16px auto",
        width: "64px",
        height: "calc(100vh - 32px)",
        borderRadius: "28px",
        background: "linear-gradient(180deg, rgba(17, 32, 60, 0.9) 0%, rgba(7, 13, 26, 0.95) 100%)",
        border: "1px solid rgba(148, 163, 184, 0.25)",
        boxShadow: "0 22px 60px rgba(2,6,23,0.6)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "14px 0",
        position: "relative",
        zIndex: 1,
        pointerEvents: "auto",
      }}>
        <div style={{
          position: "relative",
          width: "100%",
          display: "flex",
          justifyContent: "center",
          marginBottom: 14,
          marginTop: 2,
        }}>
          <div style={{
            position: "absolute",
            top: -10,
            width: 64,
            height: 64,
            borderRadius: 18,
            background: "radial-gradient(circle at 50% 40%, rgba(56,189,248,0.55), rgba(14,165,233,0.18) 70%, transparent 78%)",
            filter: "blur(6px)",
            opacity: 0.8,
          }} />
          <div style={{
            width: 40,
            height: 40,
            borderRadius: 14,
            background: "linear-gradient(180deg, rgba(25, 118, 210, 0.55) 0%, rgba(14, 74, 173, 0.65) 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f8fafc" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d={ICONS.map} />
            </svg>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 12, alignItems: "center" }}>
          <IconButton
            icon={ICONS.layers}
            active={activeTab === "dashboard"}
            onClick={() => onTabChange("dashboard")}
            label="Maps"
          />
          <IconButton
            icon={ICONS.chart}
            active={activeTab === "analytics"}
            onClick={() => onTabChange("analytics")}
            label="Analytics"
          />
        </div>

        <div style={{ marginTop: "auto", marginBottom: 8 }}>
          <IconButton icon={ICONS.settings} active={false} onClick={() => {}} />
        </div>
      </div>
    </aside>
  );
}

function IconButton({
  icon,
  active,
  onClick,
  label,
}: { icon: string; active: boolean; onClick: () => void; label?: string }) {
  return (
    <button
      onClick={onClick}
      title={label}
      style={{
        width: 40,
        height: 40,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: active ? "rgba(56, 189, 248, 0.18)" : "transparent",
        border: "none",
        cursor: "pointer",
        borderRadius: 12,
        border: active ? "1px solid rgba(56,189,248,0.5)" : "1px solid transparent",
        transition: "all 0.2s",
      }}
    >
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke={active ? "#e2e8f0" : "#cbd5f5"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d={icon} />
      </svg>
    </button>
  );
}
