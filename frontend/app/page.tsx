"use client";
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import dynamic from 'next/dynamic';
import Sidebar from './components/Sidebar';
import GrievanceFeed from './components/GrievanceFeed';
import AnalyticsPage from './components/AnalyticsPage';

// Dynamic import for Leaflet map (browser-only)
const SentiMapMap = dynamic(
  () => import('./components/SentiMapMap'),
  { ssr: false, loading: () => <div className="flex-1 bg-[#0f1219]"></div> }
);

type Grievance = {
  title: string; body: string; created_date: string; upvotes: number; num_comments: number;
  url: string; sentiment_score: number; sentiment_label: "positive" | "negative" | "neutral";
  sarcasm_detected: boolean; sentiment_confidence: number; locations: string[]; platform?: string;
  emotion_anger?: boolean; emotion_frustration?: boolean; emotion_fear?: boolean;
  emotion_disgust?: boolean; emotion_sadness?: boolean; emotion_resignation?: boolean;
  emotion_trust?: boolean; emotions_list?: string;
};

type HeatZone = {
  location: string; coords: [number, number]; count: number; avg_sentiment: number;
  severity_color: string; radii: { outer: number; mid: number; core: number }; platforms: string[];
};

export default function SentiMapDashboard() {
  const [grievances, setGrievances] = useState<Grievance[]>([]);
  const [heatZones, setHeatZones] = useState<HeatZone[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hoveredLocation, setHoveredLocation] = useState<string | null>(null);
  const [selectedLocation, setSelectedLocation] = useState<string | null>(null);
  const [stats, setStats] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<"dashboard" | "analytics">("dashboard");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/data');
        if (response.data?.status === 'error' || !response.data?.data) {
          throw new Error(response.data?.message || 'No data returned from API');
        }
        const enrichedData = response.data.data.map((item: any) => ({
          ...item,
          platform: item.url?.includes('reddit') ? 'Reddit' : item.url?.includes('facebook') ? 'Facebook' : 'Unknown'
        }));
        setGrievances(enrichedData);
        try {
          const heatmapResponse = await axios.get('/api/heatmap');
          setHeatZones(heatmapResponse.data.heatmap || []);
        } catch (e) { console.warn("Could not fetch heatmap data:", e); }
        try {
          const statsResponse = await axios.get('/api/stats');
          setStats(statsResponse.data);
        } catch (e) { console.warn("Could not fetch statistics:", e); }
      } catch (error) {
        console.error("Error fetching data:", error);
        setError("The data API is unavailable right now. Start the FastAPI backend or check the proxy configuration.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const totalReports = grievances.length;
  const severeCount = grievances.filter(g => g.sentiment_label === "negative").length;
  const sarcasticCount = grievances.filter(g => g.sarcasm_detected).length;
  const hotspotCount = heatZones.length;
  const negativePct = totalReports > 0 ? Math.round((severeCount / totalReports) * 100) : 0;
  const sarcasticPct = totalReports > 0 ? Math.round((sarcasticCount / totalReports) * 100) : 0;

  if (loading) {
    return (
      <div style={{ minHeight: "100vh", background: "#0b0f16", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ textAlign: "center" }}>
          <div style={{ width: 64, height: 64, margin: "0 auto 16px", border: "4px solid rgba(148,163,184,0.25)", borderTopColor: "#38bdf8", borderRadius: "50%", animation: "spin 1s linear infinite" }} />
          <p style={{ color: "#e2e8f0", fontSize: 16, fontWeight: 600 }}>Loading SentiMap...</p>
        </div>
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ minHeight: "100vh", background: "#0b0f16", display: "flex", alignItems: "center", justifyContent: "center", padding: 32 }}>
        <div style={{ maxWidth: 480, background: "rgba(15, 23, 42, 0.75)", border: "1px solid rgba(239,68,68,0.6)", borderRadius: 16, padding: 32, boxShadow: "0 18px 48px rgba(2,6,23,0.45)", backdropFilter: "blur(16px)" }}>
          <h1 style={{ color: "#f87171", fontSize: 28, fontWeight: 900, marginBottom: 12 }}>Connection Error</h1>
          <p style={{ color: "#e2e8f0", marginBottom: 8 }}>{error}</p>
          <p style={{ fontSize: 13, color: "#94a3b8" }}>Expected endpoint: <span style={{ color: "#e2e8f0", fontWeight: 700 }}>/api/data</span></p>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell" style={{ height: "100vh", display: "flex", overflow: "hidden" }}>
      {/* ── Fixed Sidebar ── */}
      <Sidebar
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />

      {/* ── Main content (offset by sidebar width 220px) ── */}
      <div style={{ marginLeft: 92, flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>
        {activeTab === "dashboard" ? (
          <div style={{ flex: 1, display: "flex", overflow: "hidden" }}>
            {/* 70% Map */}
            <div style={{ width: "70%", height: "100%", position: "relative", padding: 16 }}>
              <SentiMapMap
                heatZones={heatZones}
                hoveredLocation={hoveredLocation}
                selectedLocation={selectedLocation}
                onLocationSelect={setSelectedLocation}
                onLocationHover={setHoveredLocation}
              />
            </div>
            {/* 30% Feed */}
            <div style={{ width: "30%", height: "100%", display: "flex", flexDirection: "column", gap: 12, padding: 16 }}>
              <div style={{
                flex: "0 0 30%",
                background: "linear-gradient(160deg, rgba(30, 41, 59, 0.75), rgba(15, 23, 42, 0.95))",
                border: "1px solid rgba(148, 163, 184, 0.18)",
                borderRadius: 16,
                padding: 16,
                boxShadow: "0 18px 48px rgba(2,6,23,0.45)",
                display: "grid",
                gridTemplateColumns: "repeat(2, 1fr)",
                gap: 12,
              }}>
                {[
                  { label: "Reports", value: totalReports, color: "#22d3ee", icon: "📄" },
                  { label: "Severe", value: severeCount, color: "#f97316", icon: "⚠" },
                  { label: "Sarcastic", value: sarcasticCount, color: "#c084fc", icon: "✧" },
                  { label: "Hotspots", value: hotspotCount, color: "#f59e0b", icon: "🔥" },
                ].map((card) => (
                  <div
                    key={card.label}
                    style={{
                      borderRadius: 14,
                      background: "rgba(51, 65, 85, 0.55)",
                      border: "1px solid rgba(148, 163, 184, 0.16)",
                      padding: 16,
                      display: "flex",
                      flexDirection: "column",
                      alignItems: "center",
                      justifyContent: "center",
                      textAlign: "center",
                      gap: 6,
                    }}
                  >
                    <div style={{
                      width: 28,
                      height: 28,
                      borderRadius: 12,
                      background: `${card.color}22`,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      color: card.color,
                      fontSize: 12,
                      fontWeight: 800,
                    }}>
                      {card.icon}
                    </div>
                    <div style={{ color: "#e2e8f0", fontSize: 22, fontWeight: 800, letterSpacing: "-0.02em" }}>{card.value}</div>
                    <div style={{ color: "#94a3b8", fontSize: 10, fontWeight: 700, letterSpacing: "0.2em", textTransform: "uppercase" }}>{card.label}</div>
                  </div>
                ))}
              </div>
              <div style={{
                flex: "1 1 70%",
                minHeight: 0,
                background: "linear-gradient(160deg, rgba(15, 23, 42, 0.95), rgba(10, 15, 26, 0.95))",
                border: "1px solid rgba(148, 163, 184, 0.18)",
                borderRadius: 16,
                boxShadow: "0 18px 48px rgba(2,6,23,0.45)",
                overflow: "hidden",
              }}>
                <GrievanceFeed
                  grievances={grievances}
                  hoveredLocation={hoveredLocation}
                  selectedLocation={selectedLocation}
                  onLocationSelect={setSelectedLocation}
                  onLocationHover={setHoveredLocation}
                />
              </div>
            </div>
          </div>
        ) : (
          <div style={{ flex: 1, overflowY: "auto" }}>
            <AnalyticsPage
              grievances={grievances}
              heatZones={heatZones}
              selectedLocation={selectedLocation}
              stats={stats}
            />
          </div>
        )}
      </div>
    </div>
  );
}