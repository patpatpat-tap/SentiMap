"use client";
import React, { useEffect, useMemo, useRef } from 'react';

type Grievance = {
  title: string; body: string; created_date: string; upvotes: number; num_comments: number;
  url: string; sentiment_score: number; sentiment_label: "positive" | "negative" | "neutral";
  sarcasm_detected: boolean; sentiment_confidence: number; locations: string[]; platform?: string;
  emotion_anger?: boolean; emotion_frustration?: boolean; emotion_fear?: boolean;
  emotion_disgust?: boolean; emotion_sadness?: boolean; emotion_resignation?: boolean;
  emotion_trust?: boolean; emotions_list?: string;
};

type GrievanceFeedProps = {
  grievances: Grievance[];
  hoveredLocation: string | null;
  selectedLocation: string | null;
  onLocationSelect: (location: string | null) => void;
  onLocationHover: (location: string | null) => void;
};

const EMOTION_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  Sarcasm: { bg: "rgba(88, 28, 135, 0.35)", text: "#c084fc", border: "rgba(192,132,252,0.45)" },
  Anger: { bg: "rgba(127, 29, 29, 0.45)", text: "#f87171", border: "rgba(248,113,113,0.4)" },
  Frustration: { bg: "rgba(154, 52, 18, 0.45)", text: "#fb923c", border: "rgba(251,146,60,0.4)" },
  Fear: { bg: "rgba(113, 63, 18, 0.45)", text: "#f59e0b", border: "rgba(245,158,11,0.4)" },
  Disgust: { bg: "rgba(63, 63, 70, 0.45)", text: "#a1a1aa", border: "rgba(161,161,170,0.35)" },
  Sadness: { bg: "rgba(30, 64, 175, 0.4)", text: "#60a5fa", border: "rgba(96,165,250,0.35)" },
  Trust: { bg: "rgba(22, 101, 52, 0.4)", text: "#4ade80", border: "rgba(74,222,128,0.35)" },
  Resignation: { bg: "rgba(120, 53, 15, 0.4)", text: "#fbbf24", border: "rgba(251,191,36,0.35)" },
};

export default function GrievanceFeed({
  grievances,
  hoveredLocation,
  selectedLocation,
  onLocationSelect,
  onLocationHover
}: GrievanceFeedProps) {
  const feedRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!selectedLocation || !feedRef.current) return;
    const safeLocation = typeof CSS !== "undefined" && CSS.escape
      ? CSS.escape(selectedLocation)
      : selectedLocation.replace(/"/g, '\\"');
    const header = feedRef.current.querySelector("[data-pinned-header]");
    const el = header ?? feedRef.current.querySelector(`[data-location="${safeLocation}"]`);
    el?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [selectedLocation]);

  const sortedGrievances = useMemo(() => {
    const enriched = grievances.map((g) => {
      const primaryLocation = g.locations && g.locations.length > 0 ? g.locations[0] : "Unknown Location";
      const isUnknown = !primaryLocation || primaryLocation === "Unknown Location";
      return { ...g, _primaryLocation: primaryLocation, _isUnknown: isUnknown };
    });
    return enriched.sort((a, b) => Number(a._isUnknown) - Number(b._isUnknown));
  }, [grievances]);

  const pinnedLocation = selectedLocation ?? null;
  const { pinned, rest } = useMemo(() => {
    if (!pinnedLocation) return { pinned: [], rest: sortedGrievances };
    const pinnedItems = sortedGrievances.filter((g) => g._primaryLocation === pinnedLocation);
    const restItems = sortedGrievances.filter((g) => g._primaryLocation !== pinnedLocation);
    return { pinned: pinnedItems, rest: restItems };
  }, [sortedGrievances, pinnedLocation]);

  const getSentimentPillStyle = (sentiment: string) => {
    switch (sentiment) {
      case "negative": return { bg: "rgba(127, 29, 29, 0.4)", text: "#f87171", border: "rgba(248,113,113,0.4)" };
      case "positive": return { bg: "rgba(22, 101, 52, 0.4)", text: "#4ade80", border: "rgba(74,222,128,0.35)" };
      default: return { bg: "rgba(113, 63, 18, 0.4)", text: "#fbbf24", border: "rgba(251,191,36,0.35)" };
    }
  };

  const parseDate = (isoString: string) => {
    if (!isoString) return "Unknown Date";
    try {
      const d = new Date(isoString);
      if (isNaN(d.getTime())) return "Unknown Date";
      return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    } catch {
      return "Unknown Date";
    }
  };

  const parseEmotions = (emotionsList?: string) => {
    if (!emotionsList || emotionsList === "neutral") return [];
    return emotionsList.split(",").map(s => s.trim().charAt(0).toUpperCase() + s.trim().slice(1));
  };

  const getAccentGradient = (sentiment: string, isSarcastic: boolean) => {
    if (isSarcastic) return "linear-gradient(90deg, #ef4444 0%, #a855f7 100%)";
    if (sentiment === "negative") return "linear-gradient(90deg, #f97316 0%, #ef4444 100%)";
    if (sentiment === "positive") return "linear-gradient(90deg, #22c55e 0%, #60a5fa 100%)";
    return "linear-gradient(90deg, #fbbf24 0%, #f97316 100%)";
  };

  return (
    <div className="flex flex-col h-full">
      <div className="px-6 pt-5 pb-4 border-b border-[rgba(148,163,184,0.18)]">
        <h2 className="text-[18px] font-bold text-[#e2e8f0]">Grievance Feed</h2>
        <p className="text-[11px] text-[#94a3b8] mt-1">{grievances.length} reports · r/Cebu dataset</p>
      </div>

      {/* ── Feed ── */}
      <div className="flex-1 overflow-y-auto p-5" ref={feedRef}>
        {sortedGrievances.length === 0 ? (
          <div className="p-6 text-center text-[#94a3b8]">
            <p className="text-sm">No grievances match the selected filter.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {pinnedLocation && pinned.length > 0 && (
              <div className="space-y-4">
                <div data-pinned-header className="relative flex items-center justify-start mb-4">
                  <div className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.2em] text-[#94a3b8]">
                    <span className="h-2 w-2 rounded-full bg-[#10b981]" />
                    {pinnedLocation} · {pinned.length} reports
                  </div>
                  <button
                    type="button"
                    onClick={() => onLocationSelect(null)}
                    className="absolute right-0 text-[11px] font-bold uppercase tracking-[0.2em] text-[#94a3b8] hover:text-[#e2e8f0]"
                  >
                    Clear
                  </button>
                </div>
                {pinned.map((g, idx) => {
                  const primaryLocation = g._primaryLocation;
                  const isUnknown = g._isUnknown;
                  const isHighlighted = !isUnknown && primaryLocation && (primaryLocation === hoveredLocation || primaryLocation === selectedLocation);

                  const topBorderColor = g.sentiment_label === 'negative' ? '#ef4444' : g.sentiment_label === 'positive' ? '#22c55e' : '#eab308';
                  const pillStyle = getSentimentPillStyle(g.sentiment_label);
                  const emotionTags = parseEmotions(g.emotions_list);
                  if (g.sarcasm_detected && !emotionTags.includes("Sarcasm")) emotionTags.unshift("Sarcasm");
                  const limitedEmotions = emotionTags.slice(0, 3);
                  const accentGradient = getAccentGradient(g.sentiment_label, g.sarcasm_detected);
                  const signedMagnitude = Math.min(Math.abs(g.sentiment_score || 0), 1) * 50;
                  const signedLeft = g.sentiment_score >= 0 ? "50%" : `calc(50% - ${signedMagnitude}%)`;

                  return (
                    <div
                      key={`pinned-${idx}`}
                      data-location={primaryLocation}
                      className="relative flex flex-col rounded-2xl bg-[rgba(15,23,42,0.7)] transition-all cursor-pointer"
                      style={{
                        boxShadow: isHighlighted ? "0 22px 64px rgba(2,6,23,0.7)" : "0 16px 48px rgba(2,6,23,0.45)",
                        border: isHighlighted ? "1px solid rgba(226,232,240,0.45)" : "1px solid rgba(148,163,184,0.2)",
                        opacity: isUnknown ? 0.55 : 1,
                      }}
                      onMouseEnter={() => !isUnknown && primaryLocation && onLocationHover(primaryLocation)}
                      onMouseLeave={() => onLocationHover(null)}
                      onClick={() => !isUnknown && primaryLocation && onLocationSelect(primaryLocation)}
                    >
                      <div style={{ height: 4, background: accentGradient, borderTopLeftRadius: 16, borderTopRightRadius: 16 }} />
                      <div className="p-5">
                        <div className="flex items-center justify-between mb-4">
                          <div className="flex flex-wrap gap-2">
                            <span
                              className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.1em] rounded-full border"
                              style={{ backgroundColor: pillStyle.bg, color: pillStyle.text, borderColor: pillStyle.border }}
                            >
                              {g.sentiment_label}
                            </span>
                            {limitedEmotions.map(tag => {
                              const tone = EMOTION_COLORS[tag] || { bg: "rgba(15,23,42,0.8)", text: "#cbd5f5", border: "rgba(148,163,184,0.35)" };
                              return (
                                <span
                                  key={tag}
                                  className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.1em] rounded-full border"
                                  style={{ background: tone.bg, color: tone.text, borderColor: tone.border }}
                                >
                                  {tag}
                                </span>
                              );
                            })}
                          </div>
                          <span className="text-[11px] font-semibold text-[#94a3b8] bg-[rgba(51,65,85,0.6)] px-2 py-1 rounded-full">{parseDate(g.created_date)}</span>
                        </div>

                        <div className="flex items-center gap-1.5 mb-2 text-[10px] font-bold uppercase tracking-[0.2em] text-[#94a3b8]">
                          <span className="w-2 h-2 rounded-full bg-[#22c55e]"></span>
                          {primaryLocation || "Unknown Location"} • CEBU CITY
                        </div>

                        <h3 className="text-[15px] font-bold leading-snug text-[#e2e8f0] mb-3">
                          {g.title}
                        </h3>

                        {g.body && (
                          <div className="bg-[rgba(8,12,22,0.85)] border border-[rgba(148,163,184,0.18)] p-3 mb-4 rounded-xl">
                            <p className="text-[13px] leading-relaxed text-[#cbd5f5] line-clamp-3 italic">
                              "{g.body}"
                            </p>
                          </div>
                        )}

                        <div className="flex items-center gap-3 mb-4">
                          <span className="text-[11px] font-bold uppercase tracking-[0.1em] text-[#94a3b8]">Intensity</span>
                          <div className="flex-1 h-2 bg-[rgba(51,65,85,0.7)] rounded-full overflow-hidden relative">
                            <div className="absolute top-0 bottom-0 left-1/2 w-[1px] bg-[rgba(148,163,184,0.4)]" />
                            <div
                              className="absolute top-0 bottom-0 rounded-full transition-all duration-500"
                              style={{
                                left: signedLeft,
                                width: `${signedMagnitude}%`,
                                background: accentGradient,
                              }}
                            />
                          </div>
                          <span className="text-[12px] font-semibold text-[#94a3b8] w-12 text-right">
                            {(g.sentiment_score > 0 ? '+' : '') + (g.sentiment_score).toFixed(2)}
                          </span>
                        </div>

                        <div className="flex items-center justify-between pt-3 border-t border-[rgba(148,163,184,0.2)]">
                          <div className="flex items-center gap-4 text-[12px] font-semibold text-[#94a3b8]">
                            <span className="flex items-center gap-1.5">🔥 <span className="text-[#e2e8f0]">{g.upvotes}</span></span>
                            <span className="flex items-center gap-1.5">💬 <span className="text-[#e2e8f0]">{g.num_comments}</span></span>
                            <span className="hidden sm:inline-block ml-2 text-[11px]">{g.platform || 'Reddit'} • r/Cebu</span>
                          </div>
                          <a
                            href={g.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[#38bdf8] hover:text-[#0ea5e9] font-bold text-[11px] uppercase tracking-[0.1em]"
                            onClick={(e) => e.stopPropagation()}
                          >
                            Source →
                          </a>
                        </div>
                      </div>
                    </div>
                  );
                })}
                <div className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.2em] text-[#64748b]">
                  <span className="h-[1px] flex-1 bg-[rgba(148,163,184,0.2)]" />
                  All other reports · {rest.length}
                  <span className="h-[1px] flex-1 bg-[rgba(148,163,184,0.2)]" />
                </div>
              </div>
            )}
            {(!pinnedLocation || pinned.length === 0) && rest.map((g, idx) => {
              const primaryLocation = g._primaryLocation;
              const isUnknown = g._isUnknown;
              const isHighlighted = !isUnknown && primaryLocation && (primaryLocation === hoveredLocation || primaryLocation === selectedLocation);
              
              const topBorderColor = g.sentiment_label === 'negative' ? '#ef4444' : g.sentiment_label === 'positive' ? '#22c55e' : '#eab308';
              const pillStyle = getSentimentPillStyle(g.sentiment_label);
              const emotionTags = parseEmotions(g.emotions_list);
              if (g.sarcasm_detected && !emotionTags.includes("Sarcasm")) emotionTags.unshift("Sarcasm");
              const limitedEmotions = emotionTags.slice(0, 3);
              const accentGradient = getAccentGradient(g.sentiment_label, g.sarcasm_detected);
              const signedMagnitude = Math.min(Math.abs(g.sentiment_score || 0), 1) * 50;
              const signedLeft = g.sentiment_score >= 0 ? "50%" : `calc(50% - ${signedMagnitude}%)`;

              return (
                <div
                  key={idx}
                  data-location={primaryLocation}
                  className="relative flex flex-col rounded-2xl bg-[rgba(15,23,42,0.7)] transition-all cursor-pointer"
                  style={{
                    boxShadow: isHighlighted ? "0 22px 64px rgba(2,6,23,0.7)" : "0 16px 48px rgba(2,6,23,0.45)",
                    border: isHighlighted ? "1px solid rgba(226,232,240,0.45)" : "1px solid rgba(148,163,184,0.2)",
                    opacity: isUnknown ? 0.55 : 1,
                  }}
                  onMouseEnter={() => !isUnknown && primaryLocation && onLocationHover(primaryLocation)}
                  onMouseLeave={() => onLocationHover(null)}
                  onClick={() => !isUnknown && primaryLocation && onLocationSelect(primaryLocation)}
                >
                  <div style={{ height: 4, background: accentGradient, borderTopLeftRadius: 16, borderTopRightRadius: 16 }} />
                  <div className="p-5">
                    {/* Top Row: Badges & Date */}
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex flex-wrap gap-2">
                        <span 
                          className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.1em] rounded-full border"
                          style={{ backgroundColor: pillStyle.bg, color: pillStyle.text, borderColor: pillStyle.border }}
                        >
                          {g.sentiment_label}
                        </span>
                        {limitedEmotions.map(tag => {
                          const tone = EMOTION_COLORS[tag] || { bg: "rgba(15,23,42,0.8)", text: "#cbd5f5", border: "rgba(148,163,184,0.35)" };
                          return (
                          <span 
                            key={tag}
                            className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.1em] rounded-full border"
                            style={{ background: tone.bg, color: tone.text, borderColor: tone.border }}
                          >
                            {tag}
                          </span>
                        );})}
                      </div>
                      <span className="text-[11px] font-semibold text-[#94a3b8] bg-[rgba(51,65,85,0.6)] px-2 py-1 rounded-full">{parseDate(g.created_date)}</span>
                    </div>

                    {/* Location Row */}
                    <div className="flex items-center gap-1.5 mb-2 text-[10px] font-bold uppercase tracking-[0.2em] text-[#94a3b8]">
                      <span className="w-2 h-2 rounded-full bg-[#22c55e]"></span>
                      {primaryLocation || "Unknown Location"} • CEBU CITY
                    </div>

                    {/* Title */}
                    <h3 className="text-[15px] font-bold leading-snug text-[#e2e8f0] mb-3">
                      {g.title}
                    </h3>

                    {/* Body Preview */}
                    {g.body && (
                      <div className="bg-[rgba(8,12,22,0.85)] border border-[rgba(148,163,184,0.18)] p-3 mb-4 rounded-xl">
                        <p className="text-[13px] leading-relaxed text-[#cbd5f5] line-clamp-3 italic">
                          "{g.body}"
                        </p>
                      </div>
                    )}

                    {/* Intensity Slider */}
                    <div className="flex items-center gap-3 mb-4">
                      <span className="text-[11px] font-bold uppercase tracking-[0.1em] text-[#94a3b8]">Intensity</span>
                      <div className="flex-1 h-2 bg-[rgba(51,65,85,0.7)] rounded-full overflow-hidden relative">
                        <div className="absolute top-0 bottom-0 left-1/2 w-[1px] bg-[rgba(148,163,184,0.4)]" />
                        <div
                          className="absolute top-0 bottom-0 rounded-full transition-all duration-500"
                          style={{
                            left: signedLeft,
                            width: `${signedMagnitude}%`,
                            background: accentGradient,
                          }}
                        />
                      </div>
                      <span className="text-[12px] font-semibold text-[#94a3b8] w-12 text-right">
                        {(g.sentiment_score > 0 ? '+' : '') + (g.sentiment_score).toFixed(2)}
                      </span>
                    </div>

                    {/* Footer Row */}
                    <div className="flex items-center justify-between pt-3 border-t border-[rgba(148,163,184,0.2)]">
                      <div className="flex items-center gap-4 text-[12px] font-semibold text-[#94a3b8]">
                        <span className="flex items-center gap-1.5">🔥 <span className="text-[#e2e8f0]">{g.upvotes}</span></span>
                        <span className="flex items-center gap-1.5">💬 <span className="text-[#e2e8f0]">{g.num_comments}</span></span>
                        <span className="hidden sm:inline-block ml-2 text-[11px]">{g.platform || 'Reddit'} • r/Cebu</span>
                      </div>
                      <a
                        href={g.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[#38bdf8] hover:text-[#0ea5e9] font-bold text-[11px] uppercase tracking-[0.1em]"
                        onClick={(e) => e.stopPropagation()}
                      >
                        Source →
                      </a>
                    </div>
                  </div>
                </div>
              );
            })}
            {pinnedLocation && pinned.length > 0 && rest.map((g, idx) => {
              const primaryLocation = g._primaryLocation;
              const isUnknown = g._isUnknown;
              const isHighlighted = !isUnknown && primaryLocation && (primaryLocation === hoveredLocation || primaryLocation === selectedLocation);

              const topBorderColor = g.sentiment_label === 'negative' ? '#ef4444' : g.sentiment_label === 'positive' ? '#22c55e' : '#eab308';
              const pillStyle = getSentimentPillStyle(g.sentiment_label);
              const emotionTags = parseEmotions(g.emotions_list);
              if (g.sarcasm_detected && !emotionTags.includes("Sarcasm")) emotionTags.unshift("Sarcasm");
              const limitedEmotions = emotionTags.slice(0, 3);
              const accentGradient = getAccentGradient(g.sentiment_label, g.sarcasm_detected);
              const signedMagnitude = Math.min(Math.abs(g.sentiment_score || 0), 1) * 50;
              const signedLeft = g.sentiment_score >= 0 ? "50%" : `calc(50% - ${signedMagnitude}%)`;

              return (
                <div
                  key={`rest-${idx}`}
                  data-location={primaryLocation}
                  className="relative flex flex-col rounded-2xl bg-[rgba(15,23,42,0.7)] transition-all cursor-pointer"
                  style={{
                    boxShadow: isHighlighted ? "0 22px 64px rgba(2,6,23,0.7)" : "0 16px 48px rgba(2,6,23,0.45)",
                    border: isHighlighted ? "1px solid rgba(226,232,240,0.45)" : "1px solid rgba(148,163,184,0.2)",
                    opacity: isUnknown ? 0.55 : 1,
                  }}
                  onMouseEnter={() => !isUnknown && primaryLocation && onLocationHover(primaryLocation)}
                  onMouseLeave={() => onLocationHover(null)}
                  onClick={() => !isUnknown && primaryLocation && onLocationSelect(primaryLocation)}
                >
                  <div style={{ height: 4, background: accentGradient, borderTopLeftRadius: 16, borderTopRightRadius: 16 }} />
                  <div className="p-5">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex flex-wrap gap-2">
                        <span
                          className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.1em] rounded-full border"
                          style={{ backgroundColor: pillStyle.bg, color: pillStyle.text, borderColor: pillStyle.border }}
                        >
                          {g.sentiment_label}
                        </span>
                        {limitedEmotions.map(tag => {
                          const tone = EMOTION_COLORS[tag] || { bg: "rgba(15,23,42,0.8)", text: "#cbd5f5", border: "rgba(148,163,184,0.35)" };
                          return (
                            <span
                              key={tag}
                              className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.1em] rounded-full border"
                              style={{ background: tone.bg, color: tone.text, borderColor: tone.border }}
                            >
                              {tag}
                            </span>
                          );
                        })}
                      </div>
                      <span className="text-[11px] font-semibold text-[#94a3b8] bg-[rgba(51,65,85,0.6)] px-2 py-1 rounded-full">{parseDate(g.created_date)}</span>
                    </div>

                    <div className="flex items-center gap-1.5 mb-2 text-[10px] font-bold uppercase tracking-[0.2em] text-[#94a3b8]">
                      <span className="w-2 h-2 rounded-full bg-[#22c55e]"></span>
                      {primaryLocation || "Unknown Location"} • CEBU CITY
                    </div>

                    <h3 className="text-[15px] font-bold leading-snug text-[#e2e8f0] mb-3">
                      {g.title}
                    </h3>

                    {g.body && (
                      <div className="bg-[rgba(8,12,22,0.85)] border border-[rgba(148,163,184,0.18)] p-3 mb-4 rounded-xl">
                        <p className="text-[13px] leading-relaxed text-[#cbd5f5] line-clamp-3 italic">
                          "{g.body}"
                        </p>
                      </div>
                    )}

                    <div className="flex items-center gap-3 mb-4">
                      <span className="text-[11px] font-bold uppercase tracking-[0.1em] text-[#94a3b8]">Intensity</span>
                      <div className="flex-1 h-2 bg-[rgba(51,65,85,0.7)] rounded-full overflow-hidden relative">
                        <div className="absolute top-0 bottom-0 left-1/2 w-[1px] bg-[rgba(148,163,184,0.4)]" />
                        <div
                          className="absolute top-0 bottom-0 rounded-full transition-all duration-500"
                          style={{
                            left: signedLeft,
                            width: `${signedMagnitude}%`,
                            background: accentGradient,
                          }}
                        />
                      </div>
                      <span className="text-[12px] font-semibold text-[#94a3b8] w-12 text-right">
                        {(g.sentiment_score > 0 ? '+' : '') + (g.sentiment_score).toFixed(2)}
                      </span>
                    </div>

                    <div className="flex items-center justify-between pt-3 border-t border-[rgba(148,163,184,0.2)]">
                      <div className="flex items-center gap-4 text-[12px] font-semibold text-[#94a3b8]">
                        <span className="flex items-center gap-1.5">🔥 <span className="text-[#e2e8f0]">{g.upvotes}</span></span>
                        <span className="flex items-center gap-1.5">💬 <span className="text-[#e2e8f0]">{g.num_comments}</span></span>
                        <span className="hidden sm:inline-block ml-2 text-[11px]">{g.platform || 'Reddit'} • r/Cebu</span>
                      </div>
                      <a
                        href={g.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[#38bdf8] hover:text-[#0ea5e9] font-bold text-[11px] uppercase tracking-[0.1em]"
                        onClick={(e) => e.stopPropagation()}
                      >
                        Source →
                      </a>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
