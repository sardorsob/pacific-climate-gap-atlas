import type { Geo, ReportingStatus } from "../../lib/atlasData";
import type { ScoreKey } from "../../lib/encoding";
import {
  radiusFor,
  ringVariant,
  scoreColor,
  uncertaintyColor,
  valueForScore,
} from "../../lib/encoding";
import { GRATICULE_LATS, GRATICULE_LONS } from "../../lib/projection";
import type { ViewMode } from "../../lib/types";

export type AtlasMapState = {
  activeScore: ScoreKey;
  viewMode: ViewMode;
  outlookOn: boolean;
  selectedCode: string | null;
  compareCode: string | null;
  priorityCodes: string[];
};

export type AtlasPointProperties = {
  code: string;
  name: string;
  storyLabel: string;
  scoreValue: number | null;
  fillColor: string;
  strokeColor: string;
  radius: number;
  opacity: number;
  selected: boolean;
  compare: boolean;
  priority: boolean;
  dimmed: boolean;
  withheld: boolean;
  reportingStatus: ReportingStatus;
  ringVariant: ReturnType<typeof ringVariant>;
  strokeDasharray: number[] | null;
  hatch: boolean;
  geometryStatus: "centroid_fallback";
};

export type AtlasPointFeature = {
  type: "Feature";
  geometry: {
    type: "Point";
    coordinates: [number, number];
  };
  properties: AtlasPointProperties;
};

export type AtlasFeatureCollection = {
  type: "FeatureCollection";
  features: AtlasPointFeature[];
};

export type GraticuleFeature = {
  type: "Feature";
  geometry: {
    type: "LineString";
    coordinates: [[number, number], [number, number]];
  };
  properties: {
    kind: "longitude" | "latitude";
    value: number;
  };
};

export type GraticuleFeatureCollection = {
  type: "FeatureCollection";
  features: GraticuleFeature[];
};

export function fitBoundsForPacific(): [[number, number], [number, number]] {
  return [[130, -30], [240, 20]];
}

export function buildGraticuleFeatureCollection(options?: {
  longitudes?: number[];
  latitudes?: number[];
  bounds?: [[number, number], [number, number]];
}): GraticuleFeatureCollection {
  const longitudes = options?.longitudes ?? GRATICULE_LONS;
  const latitudes = options?.latitudes ?? GRATICULE_LATS;
  const bounds = options?.bounds ?? fitBoundsForPacific();
  const [[minLon, minLat], [maxLon, maxLat]] = bounds;

  return {
    type: "FeatureCollection",
    features: [
      ...longitudes.map((lon) => ({
        type: "Feature" as const,
        geometry: {
          type: "LineString" as const,
          coordinates: [[lon, minLat], [lon, maxLat]] as [[number, number], [number, number]],
        },
        properties: { kind: "longitude" as const, value: lon },
      })),
      ...latitudes.map((lat) => ({
        type: "Feature" as const,
        geometry: {
          type: "LineString" as const,
          coordinates: [[minLon, lat], [maxLon, lat]] as [[number, number], [number, number]],
        },
        properties: { kind: "latitude" as const, value: lat },
      })),
    ],
  };
}

export function markerPaintFor(status: ReportingStatus): {
  strokeColor: string;
  strokeDasharray: number[] | null;
  hatch: boolean;
} {
  const variant = ringVariant(status);
  if (variant === "hatch") {
    return { strokeColor: "#9fb4bf", strokeDasharray: [1, 2], hatch: true };
  }
  if (variant === "dashed") {
    return { strokeColor: "#d4dde2", strokeDasharray: [2, 2], hatch: false };
  }
  return { strokeColor: "rgba(6,16,24,0.62)", strokeDasharray: null, hatch: false };
}

export function buildAtlasFeatureCollection(geos: Geo[], state: AtlasMapState): AtlasFeatureCollection {
  const hasSelection = state.selectedCode !== null;

  return {
    type: "FeatureCollection",
    features: geos.map((geo) => {
      const isSelected = geo.code === state.selectedCode;
      const isCompare = geo.code === state.compareCode && geo.code !== state.selectedCode;
      const isPriority = state.viewMode === "coverage" && state.priorityCodes.includes(geo.code);
      const withheld = state.outlookOn && geo.outlookDisplay === "withhold";
      const dimmed =
        (hasSelection && !isSelected && geo.code !== state.compareCode) ||
        (state.viewMode === "coverage" && !isPriority && geo.storyPriority > 3);
      const scoreValue = scoreValueFor(geo, state, withheld);
      const paint = markerPaintFor(geo.reportingStatus);

      return {
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [geo.lon, geo.lat],
        },
        properties: {
          code: geo.code,
          name: geo.name,
          storyLabel: geo.storyLabel,
          scoreValue,
          fillColor: markerFillFor(geo, state),
          strokeColor: withheld ? "#9fb4bf" : paint.strokeColor,
          radius: radiusFor(geo.indicators),
          opacity: dimmed ? 0.32 : 1,
          selected: isSelected,
          compare: isCompare,
          priority: isPriority,
          dimmed,
          withheld,
          reportingStatus: geo.reportingStatus,
          ringVariant: ringVariant(geo.reportingStatus),
          strokeDasharray: withheld ? [1, 2] : paint.strokeDasharray,
          hatch: paint.hatch,
          geometryStatus: "centroid_fallback",
        },
      };
    }),
  };
}

function scoreValueFor(geo: Geo, state: AtlasMapState, withheld: boolean): number | null {
  if (withheld) return null;
  if (state.outlookOn) return geo.outlook2030Flat;
  if (state.viewMode === "uncertainty") return geo.rankRange;
  if (state.viewMode === "coverage") return null;
  return valueForScore(geo, state.activeScore);
}

function markerFillFor(geo: Geo, state: AtlasMapState): string {
  if (state.outlookOn) {
    if (geo.outlookDisplay === "withhold") return "transparent";
    return scoreColor("gap", geo.outlook2030Flat);
  }
  if (state.viewMode === "uncertainty") return uncertaintyColor(geo.rankRange);
  if (state.viewMode === "coverage") return "#64777f";
  return scoreColor(state.activeScore, valueForScore(geo, state.activeScore));
}
