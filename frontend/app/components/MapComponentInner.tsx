'use client';

import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Circle, CircleMarker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for Leaflet default marker icons
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});
L.Marker.prototype.setIcon(DefaultIcon);

type HeatZone = {
  location: string;
  coords: [number, number];
  count: number;
  sarcasm_count?: number;
  avg_sentiment: number;
  severity_color: string;
  radii: { outer: number; mid: number; core: number };
  platforms: string[];
};

type SentiMapMapProps = {
  heatZones: HeatZone[];
  hoveredLocation: string | null;
  selectedLocation: string | null;
  onLocationSelect: (location: string) => void;
  onLocationHover: (location: string | null) => void;
};

export default function MapComponentInner({
  heatZones,
  hoveredLocation,
  selectedLocation,
  onLocationSelect,
  onLocationHover
}: SentiMapMapProps) {
  const mapCenter: [number, number] = [10.3157, 123.8854];
  const mapZoom = 12;

  const getSeverity = (avgSentiment: number) => {
    const severity = Math.max(0, -avgSentiment);
    if (severity > 0.66) return "severe";
    if (severity > 0.33) return "moderate";
    return "minor";
  };

  const severityCounts = heatZones.reduce(
    (acc, zone) => {
      const severity = getSeverity(zone.avg_sentiment);
      acc[severity] += 1;
      return acc;
    },
    { severe: 0, moderate: 0, minor: 0 }
  );

  const LegendControl = () => {
    const map = useMap();

    useEffect(() => {
      const control = L.control({ position: 'bottomleft' });

      control.onAdd = () => {
        const container = L.DomUtil.create('div', 'sentimap-legend');
        container.style.background = 'linear-gradient(140deg, rgba(11,18,30,0.92), rgba(8,12,22,0.78))';
        container.style.border = '1px solid rgba(148,163,184,0.14)';
        container.style.borderRadius = '14px';
        container.style.padding = '12px 14px';
        container.style.margin = '0 0 52px 12px';
        container.style.boxShadow = '0 20px 48px rgba(2,6,23,0.55)';
        container.style.color = '#e2e8f0';
        container.style.fontFamily = '"Poppins", system-ui, sans-serif';
        container.style.width = '220px';
        container.style.backdropFilter = 'blur(14px)';
        container.style.webkitBackdropFilter = 'blur(14px)';

        container.innerHTML = `
          <div style="font-size:12px;letter-spacing:0.2em;text-transform:uppercase;color:#94a3b8;">Grievance Intensity</div>
          <div style="margin-top:10px;display:flex;flex-direction:column;gap:10px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div style="display:flex;gap:8px;align-items:center;">
                <span style="width:8px;height:8px;border-radius:999px;background:#ef4444;display:inline-block;box-shadow:0 0 10px rgba(239,68,68,0.35);"></span>
                <span style="font-size:12px;font-weight:600;">Critical</span>
              </div>
              <span style="font-size:11px;color:#94a3b8;">75%+</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div style="display:flex;gap:8px;align-items:center;">
                <span style="width:8px;height:8px;border-radius:999px;background:#f97316;display:inline-block;box-shadow:0 0 10px rgba(249,115,22,0.35);"></span>
                <span style="font-size:12px;font-weight:600;">Moderate</span>
              </div>
              <span style="font-size:11px;color:#94a3b8;">55-75%</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div style="display:flex;gap:8px;align-items:center;">
                <span style="width:8px;height:8px;border-radius:999px;background:#eab308;display:inline-block;box-shadow:0 0 10px rgba(234,179,8,0.35);"></span>
                <span style="font-size:12px;font-weight:600;">Low</span>
              </div>
              <span style="font-size:11px;color:#94a3b8;">&lt;55%</span>
            </div>
          </div>
        `;

        L.DomEvent.disableClickPropagation(container);
        L.DomEvent.disableScrollPropagation(container);
        return container;
      };

      control.addTo(map);

      return () => {
        control.remove();
      };
    }, [map]);

    return null;
  };

  const LocationPillControl = () => {
    const map = useMap();

    useEffect(() => {
      const control = L.control({ position: 'bottomright' });

      control.onAdd = () => {
        const container = L.DomUtil.create('div', 'sentimap-location-pill');
        container.style.background = 'linear-gradient(140deg, rgba(11,18,30,0.92), rgba(8,12,22,0.78))';
        container.style.border = '1px solid rgba(148,163,184,0.14)';
        container.style.borderRadius = '12px';
        container.style.padding = '8px 12px';
        container.style.margin = '0 12px 18px 0';
        container.style.boxShadow = '0 20px 48px rgba(2,6,23,0.55)';
        container.style.color = '#cbd5f5';
        container.style.fontFamily = '"Poppins", system-ui, sans-serif';
        container.style.fontSize = '11px';
        container.style.letterSpacing = '0.08em';
        container.style.textTransform = 'uppercase';
        container.style.backdropFilter = 'blur(14px)';
        container.style.webkitBackdropFilter = 'blur(14px)';

        const formatCoord = (value: number, pos: string, neg: string) => {
          const label = value >= 0 ? pos : neg;
          return `${Math.abs(value).toFixed(4)}°${label}`;
        };

        const updateBadge = () => {
          const center = map.getCenter();
          const zoom = map.getZoom();
          const lat = formatCoord(center.lat, 'N', 'S');
          const lng = formatCoord(center.lng, 'E', 'W');
          container.textContent = `${lat}, ${lng} · z${zoom.toFixed(1)}`;
        };

        updateBadge();
        map.on('move', updateBadge);
        map.on('zoom', updateBadge);

        L.DomEvent.disableClickPropagation(container);
        L.DomEvent.disableScrollPropagation(container);
        return container;
      };

      control.addTo(map);

      return () => {
        map.off('move');
        map.off('zoom');
        control.remove();
      };
    }, [map]);

    return null;
  };


  return (
    <div className="map-shell relative w-full h-full">
      <div
        className="pointer-events-none absolute left-1/2 top-1/2 z-[600] h-6 w-6 -translate-x-1/2 -translate-y-1/2"
        aria-hidden="true"
      >
        <div className="absolute left-1/2 top-0 h-6 w-px -translate-x-1/2 bg-white/70"></div>
        <div className="absolute left-0 top-1/2 h-px w-6 -translate-y-1/2 bg-white/70"></div>
        <div className="absolute left-1/2 top-1/2 h-2 w-2 -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/70"></div>
      </div>
      <MapContainer
        center={mapCenter}
        zoom={mapZoom}
        style={{ 
          height: '100%', 
          width: '100%',
          backgroundColor: '#0f1219',
          borderRadius: '12px',
          overflow: 'hidden'
        }}
        className="map-container map-rounded"
        zoomControl={true}
        scrollWheelZoom={true}
        attributionControl={false}
      >
        <LegendControl />
        <LocationPillControl />
        {/* OpenStreetMap Tiles - Light */}
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          maxZoom={19}
          minZoom={1}
          className="sentimap-tiles"
        />

        {/* Heat Zones */}
        {heatZones.map((zone, index) => {
          const isHovered = hoveredLocation === zone.location;
          const isSelected = selectedLocation === zone.location;

          const outerRadius = zone.radii?.outer ?? Math.max(200, zone.count * 80);
          const midRadius = zone.radii?.mid ?? Math.max(120, zone.count * 50);
          const isHighlighted = isHovered || isSelected;
          const coreRadius = (8 + zone.count * 2.5) + (isHighlighted ? 3 : 0);

          return (
            <React.Fragment key={index}>
              {/* Outer Glow (5% opacity) */}
              <Circle
                center={zone.coords}
                radius={outerRadius}
                pathOptions={{
                  color: zone.severity_color,
                  weight: 0,
                  opacity: 0.05,
                  fillOpacity: 0.05,
                  fillColor: zone.severity_color
                }}
                eventHandlers={{
                  mouseover: () => onLocationHover(zone.location),
                  mouseout: () => onLocationHover(null),
                  click: () => onLocationSelect(zone.location)
                }}
              />

              {/* Mid Ring (12% opacity) */}
              <Circle
                center={zone.coords}
                radius={midRadius}
                pathOptions={{
                  color: zone.severity_color,
                  weight: 0,
                  opacity: 0.12,
                  fillOpacity: 0.12,
                  fillColor: zone.severity_color
                }}
                eventHandlers={{
                  mouseover: () => onLocationHover(zone.location),
                  mouseout: () => onLocationHover(null),
                  click: () => onLocationSelect(zone.location)
                }}
              />

              {/* Core Marker (80-95% opacity, increases if hovered/selected) */}
              <CircleMarker
                center={zone.coords}
                radius={coreRadius}
                pathOptions={{
                  color: isHighlighted ? "#ffffff" : zone.severity_color,
                  weight: isHighlighted ? 2 : 1,
                  opacity: isHighlighted ? 1 : 0.85,
                  fillOpacity: isHighlighted ? 0.95 : 0.8,
                  fillColor: zone.severity_color
                }}
                eventHandlers={{
                  mouseover: () => onLocationHover(zone.location),
                  mouseout: () => onLocationHover(null),
                  click: () => onLocationSelect(zone.location)
                }}
              >
                <Popup>
                  <div className="text-sm">
                    <div className="flex items-start justify-between gap-3">
                      <p className="font-bold text-slate-900">{zone.location}</p>
                      <span className="rounded-full bg-red-100 px-2 py-0.5 text-[11px] font-semibold text-red-600">
                        {(Math.max(0, -zone.avg_sentiment) * 100).toFixed(0)}%
                      </span>
                    </div>
                    <p className="mt-1 text-xs text-slate-600">
                      {zone.count} reports • {zone.sarcasm_count ?? 0} sarcastic
                    </p>
                  </div>
                </Popup>
              </CircleMarker>
            </React.Fragment>
          );
        })}
      </MapContainer>
    </div>
    );
}
