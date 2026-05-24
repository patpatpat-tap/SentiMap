"use client";
import React, { useMemo } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ResponsiveContainer, Cell, PieChart, Pie,
} from "recharts";

// ─── Types ────────────────────────────────────────────────────────────────────
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
type Props = { grievances: Grievance[]; heatZones: HeatZone[]; selectedLocation: string | null; stats: any };

type EmotionKey = "Anger"|"Frustration"|"Sarcasm"|"Resignation"|"Fear"|"Disgust"|"Sadness"|"Trust";

// ─── Warm Color Palette ───────────────────────────────────────────────────────
const EMOTION_COLORS: Record<EmotionKey, string> = {
  Anger:       "#ef4444",
  Frustration: "#f97316",
  Sarcasm:     "#a855f7",
  Resignation: "#64748b",
  Fear:        "#22d3ee",
  Disgust:     "#84cc16",
  Sadness:     "#3b82f6",
  Trust:       "#10b981",
};
const EMOTION_ORDER: EmotionKey[] = ["Anger","Frustration","Sarcasm","Resignation","Fear","Disgust","Sadness","Trust"];

// ─── Tooltip style (warm/light) ──────────────────────────────────────────────────
const TStyle = {
  background: "rgba(15, 23, 42, 0.85)",
  border: "1px solid rgba(148, 163, 184, 0.25)",
  borderRadius: "10px",
  padding: "10px 14px",
  color: "#e2e8f0",
  fontSize: "13px",
  boxShadow: "0 18px 48px rgba(2,6,23,0.45)",
  backdropFilter: "blur(16px)",
};

const CustomBarTooltip = ({ active, payload, label }: any) => {
  const filtered = (payload || []).filter((p: any) => Number(p?.value) > 0);
  if (!active || filtered.length === 0) return null;
  return (
    <div style={TStyle}>
      <p style={{ fontWeight: 700, marginBottom: 4, color: "#94a3b8", fontSize: 11, textTransform: "uppercase", letterSpacing: "0.1em" }}>{label}</p>
      {filtered.map((p: any) => (
        <p key={p.name} style={{ color: p.fill || p.color, margin: "2px 0" }}>{p.name}: <strong>{p.value}</strong></p>
      ))}
    </div>
  );
};

const CustomPieTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  const { name, value, payload: inner } = payload[0];
  return (
    <div style={TStyle}>
      <p style={{ fontWeight: 700, color: inner.fill }}>{name}</p>
      <p style={{ color: "#e2e8f0" }}>{value} ({((value / inner.total) * 100).toFixed(1)}%)</p>
    </div>
  );
};

const RADIAN = Math.PI / 180;
const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
  if (percent < 0.05) return null;
  const r = innerRadius + (outerRadius - innerRadius) * 0.55;
  const x = cx + r * Math.cos(-midAngle * RADIAN);
  const y = cy + r * Math.sin(-midAngle * RADIAN);
  return <text x={x} y={y} fill="white" textAnchor="middle" dominantBaseline="central" fontSize={12} fontWeight={700}>{`${(percent * 100).toFixed(0)}%`}</text>;
};

// ─── Card & Section Title ──────────────────────────────────────────────────────
function Card({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`rounded-2xl border border-[rgba(148,163,184,0.18)] bg-[linear-gradient(160deg,rgba(20,28,48,0.9),rgba(15,23,42,0.95))] p-6 shadow-[0_18px_60px_rgba(2,6,23,0.45)] backdrop-blur-[16px] ${className}`}>
      {children}
    </div>
  );
}

function SectionTitle({ title, sub }: { title: string; sub: string }) {
  return (
    <div className="mb-5">
      <h2 style={{ color: "#cbd5f5", fontWeight: 800, fontSize: "11px", letterSpacing: "0.18em", textTransform: "uppercase", margin: 0 }}>{title}</h2>
      <p style={{ color: "#94a3b8", fontSize: "12px", marginTop: 4 }}>{sub}</p>
    </div>
  );
}


// ─── Grievance Category Rules ─────────────────────────────────────────────────
const CATEGORY_RULES = [
  {
    name: "Enforcement abuse",
    fill: "#f59e0b",
    keywords: [
      "citom", "lto", "ltfrb", "apprehend", "apprehension", "kotong",
      "enforcer", "enforcement", "checkpoint", "ticket", "penalty", "fine",
      "abuso", "abuse", "extortion", "corrupt", "corruption",
    ],
  },
  {
    name: "Transport service",
    fill: "#ef4444",
    keywords: [
      "jeepney", "jeep", "taxi", "bus", "puv", "commute", "commuting",
      "driver", "conductor", "pasahero", "fare", "overcharging", "plite", "plete",
      "angkas", "habal", "grab", "move it",
    ],
  },
  {
    name: "Infrastructure failure",
    fill: "#ea580c",
    keywords: [
      "brt", "roadwork", "pothole", "flood", "drainage", "unfinished",
      "repair", "construction", "road", "bridge", "traffic light", "signal",
    ],
  },
  {
    name: "Policy frustration",
    fill: "#dc2626",
    keywords: [
      "one-way", "one way", "scheme", "policy", "ordinance", "regulation",
      "rule", "ban", "coding", "implementation",
    ],
  },
  {
    name: "Road safety",
    fill: "#b45309",
    keywords: [
      "accident", "disgrasya", "reckless", "counterflow", "speeding",
      "hit and run", "collision", "crash", "injury", "danger",
    ],
  },
] as const;

const CustomCategoryTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={TStyle}>
      <p style={{ fontWeight: 700, marginBottom: 4, color: "#94a3b8", fontSize: 11, textTransform: "uppercase", letterSpacing: "0.1em" }}>{label}</p>
      <p style={{ color: payload[0].fill, margin: "2px 0" }}>Posts: <strong>{payload[0].value}</strong></p>
    </div>
  );
};

// ─── Main Component ───────────────────────────────────────────────────────────
export default function AnalyticsPage({ grievances, heatZones, selectedLocation, stats }: Props) {
  const filtered = useMemo(() => {
    if (!selectedLocation) return grievances;
    return grievances.filter((g) => g.locations?.some((l) => l === selectedLocation));
  }, [grievances, selectedLocation]);

  // Read global emotion counts directly from the backend API
  const emotionCounts = useMemo(() => {
    const fallbackCounts = filtered.reduce(
      (acc, g) => {
        if (g.emotion_anger) acc.Anger += 1;
        if (g.emotion_frustration) acc.Frustration += 1;
        if (g.sarcasm_detected) acc.Sarcasm += 1;
        if (g.emotion_resignation) acc.Resignation += 1;
        if (g.emotion_fear) acc.Fear += 1;
        if (g.emotion_disgust) acc.Disgust += 1;
        if (g.emotion_sadness) acc.Sadness += 1;
        if (g.emotion_trust) acc.Trust += 1;
        return acc;
      },
      { Anger: 0, Frustration: 0, Sarcasm: 0, Resignation: 0, Fear: 0, Disgust: 0, Sadness: 0, Trust: 0 }
    );

    const rawCounts = stats?.emotion_counts;
    if (!rawCounts) return fallbackCounts;
    return {
      Anger: rawCounts.anger || fallbackCounts.Anger,
      Frustration: rawCounts.frustration || fallbackCounts.Frustration,
      Sarcasm: rawCounts.sarcasm || fallbackCounts.Sarcasm,
      Resignation: rawCounts.resignation || fallbackCounts.Resignation,
      Fear: rawCounts.fear || fallbackCounts.Fear,
      Disgust: rawCounts.disgust || fallbackCounts.Disgust,
      Sadness: rawCounts.sadness || fallbackCounts.Sadness,
      Trust: rawCounts.trust || fallbackCounts.Trust,
    };
  }, [stats, filtered]);

  const totalSignals = useMemo(() => Object.values(emotionCounts).reduce((a, b) => a + b, 0), [emotionCounts]);

  const emotionDistData = useMemo(() =>
    EMOTION_ORDER.map((e) => ({
      name: e, count: emotionCounts[e],
      pct: totalSignals ? Math.round((emotionCounts[e] / totalSignals) * 100) : 0,
      fill: EMOTION_COLORS[e],
    })), [emotionCounts, totalSignals]);

  const severityData = useMemo(() => {
    let severe = 0, moderate = 0, low = 0;
    filtered.forEach((g) => {
      const s = g.sentiment_score ?? 0;
      if (s <= -0.75) severe++; else if (s <= -0.5) moderate++; else low++;
    });
    const total = filtered.length || 1;
    return [
      { name: "Severe",   value: severe,   fill: "#dc2626", total },
      { name: "Moderate", value: moderate, fill: "#ea580c", total },
      { name: "Low",      value: low,      fill: "#b45309", total },
    ];
  }, [filtered]);

  const sarcasmData = useMemo(() => {
    const sarcastic = filtered.filter((g) => g.sarcasm_detected).length;
    const direct = filtered.length - sarcastic;
    const total = filtered.length || 1;
    return [
      { name: "Sarcastic", value: sarcastic, fill: "#a855f7", total },
      { name: "Direct",    value: direct,    fill: "#22d3ee", total },
    ];
  }, [filtered]);

  const dominantEmotions = useMemo(() =>
    EMOTION_ORDER.map((e) => ({ name: e, count: emotionCounts[e] }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 3),
    [emotionCounts]);

  const hotspotEmotionData = useMemo(() => {
    const locationMap: Record<string, Record<EmotionKey, number>> = {};
    grievances.forEach((g) => {
      // Create an array of active emotions directly from the grievance boolean flags
      const activeEmotions: EmotionKey[] = [];
      if (g.emotion_anger) activeEmotions.push("Anger");
      if (g.emotion_frustration) activeEmotions.push("Frustration");
      if (g.sarcasm_detected) activeEmotions.push("Sarcasm");
      if (g.emotion_resignation) activeEmotions.push("Resignation");
      if (g.emotion_fear) activeEmotions.push("Fear");
      if (g.emotion_disgust) activeEmotions.push("Disgust");
      if (g.emotion_sadness) activeEmotions.push("Sadness");
      if (g.emotion_trust) activeEmotions.push("Trust");

      g.locations?.forEach((loc) => {
        if (!locationMap[loc]) locationMap[loc] = { Anger: 0, Frustration: 0, Sarcasm: 0, Resignation: 0, Fear: 0, Disgust: 0, Sadness: 0, Trust: 0 };
        activeEmotions.forEach((e) => locationMap[loc][e]++);
      });
    });
    return Object.entries(locationMap)
      .map(([loc, counts]) => ({ loc, total: Object.values(counts).reduce((a, b) => a + b, 0), ...counts }))
      .sort((a, b) => b.total - a.total)
      .slice(0, 8)
      .map(({ loc, total, ...rest }) => ({ location: loc, ...rest }));
  }, [grievances]);

  const noData = filtered.length === 0;
  const categoryBars = useMemo(() => {
    const counts = CATEGORY_RULES.map((rule) => ({
      name: rule.name,
      posts: 0,
      fill: rule.fill,
    }));

    filtered.forEach((g) => {
      const text = `${g.title || ""} ${g.body || ""} ${g.emotions_list || ""}`.toLowerCase();
      CATEGORY_RULES.forEach((rule, idx) => {
        const matched = rule.keywords.some((kw) => text.includes(kw));
        if (matched) counts[idx].posts += 1;
      });
    });

    return counts
      .filter((c) => c.posts > 0)
      .sort((a, b) => b.posts - a.posts)
      .slice(0, 5);
  }, [filtered]);

  const categoryMax = useMemo(() => {
    const maxValue = Math.max(1, ...categoryBars.map((c) => c.posts));
    return Math.ceil(maxValue / 5) * 5;
  }, [categoryBars]);

  return (
    <div style={{ minHeight: "100%", padding: "32px 32px 48px", overflowY: "auto" }}>

      {/* ── Page Header ── */}
      <div id="section-overview" style={{ marginBottom: 32, scrollMarginTop: 24 }}>
        <h1 style={{
          fontSize: "28px", fontWeight: 800, letterSpacing: "0.01em", lineHeight: 1,
          color: "#e2e8f0",
          margin: 0,
        }}>
          Analytics
        </h1>
        <p style={{ color: "#94a3b8", fontSize: "12px", marginTop: 6, letterSpacing: "0.08em", textTransform: "uppercase" }}>
          {filtered.length} grievances · {totalSignals} multi-label emotion signals · r/Cebu
        </p>
      </div>

      {noData && (
          <div style={{ textAlign: "center", padding: "64px 0", color: "#94a3b8" }}>
          <p style={{ fontSize: 18 }}>No grievances match the current filter.</p>
          <p style={{ fontSize: 13, marginTop: 6 }}>Clear the location filter on the Dashboard.</p>
        </div>
      )}

      {!noData && (
        <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 24 }}>
            <div id="section-emotion" style={{ scrollMarginTop: 24 }}>
              <Card>
                <SectionTitle title="Emotion Distribution" sub="Frequency across all reports (multi-label)" />
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={emotionDistData} layout="vertical" margin={{ top: 0, right: 60, left: 10, bottom: 0 }}>
                    <CartesianGrid horizontal={false} stroke="rgba(148,163,184,0.12)" />
                    <XAxis type="number" tick={{ fill: "#94a3b8", fontSize: 11 }} axisLine={false} tickLine={false} allowDecimals={false} />
                    <YAxis type="category" dataKey="name" tick={{ fill: "#e2e8f0", fontSize: 12, fontWeight: 600 }} axisLine={false} tickLine={false} width={90} />
                    <Tooltip content={<CustomBarTooltip />} cursor={{ fill: "rgba(148,163,184,0.08)" }} />
                    <Bar dataKey="count" radius={[0, 8, 8, 0]} barSize={20}>
                      {emotionDistData.map((entry) => <Cell key={entry.name} fill={entry.fill} />)}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </Card>
            </div>
            <div>
              <Card>
                <SectionTitle title="Dominant Emotions" sub="Top 3 by signal count" />
                <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                  {dominantEmotions.map((e, idx) => {
                    const pct = totalSignals ? Math.round((e.count / totalSignals) * 100) : 0;
                    const color = EMOTION_COLORS[e.name as EmotionKey];
                    return (
                      <div key={e.name} style={{
                        padding: 12,
                        borderRadius: 14,
                        background: "rgba(15, 23, 42, 0.6)",
                        border: "1px solid rgba(148,163,184,0.18)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        gap: 12,
                      }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 12, flex: 1 }}>
                          <div style={{
                            width: 34,
                            height: 34,
                            borderRadius: 12,
                            background: `${color}22`,
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            color,
                            fontWeight: 800,
                          }}>
                            #{idx + 1}
                          </div>
                          <div style={{ flex: 1 }}>
                            <div style={{ color: "#e2e8f0", fontWeight: 700, fontSize: 13 }}>#{idx + 1} {e.name}</div>
                            <div style={{ height: 6, background: "rgba(148,163,184,0.2)", borderRadius: 999, marginTop: 6, overflow: "hidden" }}>
                              <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: 999 }} />
                            </div>
                          </div>
                        </div>
                        <div style={{ color: "#e2e8f0", fontWeight: 700 }}>{e.count}</div>
                      </div>
                    );
                  })}
                </div>
              </Card>
            </div>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 24 }}>
            <div id="section-severity" style={{ scrollMarginTop: 24 }}>
              <Card>
                <SectionTitle title="Severity Mix" sub="Negative grievances bucketed by polarity" />
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Pie data={severityData} cx="50%" cy="50%" innerRadius={55} outerRadius={85} dataKey="value" labelLine={false} label={renderCustomLabel}>
                      {severityData.map((entry) => <Cell key={entry.name} fill={entry.fill} />)}
                    </Pie>
                    <Tooltip content={<CustomPieTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
                <div style={{ display: "flex", justifyContent: "center", gap: 14, marginTop: 12, flexWrap: "wrap" }}>
                  {severityData.map((d) => (
                    <div key={d.name} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 12, color: "#cbd5f5" }}>
                      <span style={{ width: 10, height: 10, borderRadius: "50%", background: d.fill, display: "inline-block" }} />
                      {d.name}
                    </div>
                  ))}
                </div>
              </Card>
            </div>

            <div id="section-sarcasm" style={{ scrollMarginTop: 24 }}>
              <Card>
                <SectionTitle title="Sarcasm vs Direct" sub="Volume of sarcastic vs direct posts" />
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Pie data={sarcasmData} cx="50%" cy="50%" innerRadius={55} outerRadius={85} dataKey="value" labelLine={false} label={renderCustomLabel}>
                      {sarcasmData.map((entry) => <Cell key={entry.name} fill={entry.fill} />)}
                    </Pie>
                    <Tooltip content={<CustomPieTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
                <div style={{ display: "flex", justifyContent: "center", gap: 14, marginTop: 12, flexWrap: "wrap" }}>
                  {sarcasmData.map((d) => (
                    <div key={d.name} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 12, color: "#cbd5f5" }}>
                      <span style={{ width: 10, height: 10, borderRadius: "50%", background: d.fill, display: "inline-block" }} />
                      {d.name}
                    </div>
                  ))}
                </div>
              </Card>
            </div>

            <div id="section-category" style={{ scrollMarginTop: 24 }}>
              <Card>
                <SectionTitle title="Category Breakdown" sub="Rule-based topics from grievance text" />
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={categoryBars} layout="vertical" margin={{ top: 0, right: 40, left: 20, bottom: 0 }}>
                    <CartesianGrid horizontal={false} stroke="rgba(148,163,184,0.12)" />
                    <XAxis type="number" tick={{ fill: "#94a3b8", fontSize: 11 }} axisLine={false} tickLine={false} allowDecimals={false} domain={[0, categoryMax]} />
                    <YAxis type="category" dataKey="name" tick={{ fill: "#e2e8f0", fontSize: 11, fontWeight: 600 }} axisLine={false} tickLine={false} width={120} />
                    <Tooltip content={<CustomCategoryTooltip />} cursor={{ fill: "rgba(148,163,184,0.08)" }} />
                    <Bar dataKey="posts" radius={[0, 8, 8, 0]} barSize={20}>
                      {categoryBars.map((entry) => <Cell key={entry.name} fill={entry.fill} />)}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </Card>
            </div>
          </div>

          {hotspotEmotionData.length > 0 && (
            <div id="section-hotspot" style={{ scrollMarginTop: 24 }}>
              <Card className="h-[380px]">
                <SectionTitle title="Emotion by Hotspot" sub="Top 8 locations · stacked emotion mix" />
                <ResponsiveContainer width="100%" height={310}>
                  <BarChart data={hotspotEmotionData} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                    <CartesianGrid vertical={false} stroke="rgba(148,163,184,0.12)" />
                    <XAxis dataKey="location" tick={{ fill: "#94a3b8", fontSize: 11 }} axisLine={false} tickLine={false} interval={0} />
                    <YAxis tick={{ fill: "#94a3b8", fontSize: 11 }} axisLine={false} tickLine={false} allowDecimals={false} />
                    <Tooltip content={<CustomBarTooltip />} cursor={{ fill: "rgba(148,163,184,0.08)" }} />
                    <Legend wrapperStyle={{ paddingTop: 12, fontSize: 11, color: "#94a3b8" }} iconType="circle" iconSize={8} />
                    {EMOTION_ORDER.map((e) => (
                      <Bar key={e} dataKey={e} stackId="a" fill={EMOTION_COLORS[e]} />
                    ))}
                  </BarChart>
                </ResponsiveContainer>
              </Card>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
