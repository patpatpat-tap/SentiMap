'use client';

import React, { useEffect, useState } from 'react';

type HeatZone = {
  location: string;
  coords: [number, number];
  count: number;
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

// Lazy load the actual map component only on client
const MapComponent = React.lazy(() => import('./MapComponentInner'));

export default function SentiMapMap(props: SentiMapMapProps) {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) {
    return <div className="w-full h-full bg-[#0f1219]"></div>;
  }

  return (
    <React.Suspense fallback={<div className="w-full h-full bg-[#0f1219]"></div>}>
      <MapComponent {...props} />
    </React.Suspense>
  );
}
