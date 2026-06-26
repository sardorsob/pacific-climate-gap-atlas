import type { KeyboardEvent } from "react";
import type { Geo } from "../../mock/mockAtlasData";
import { PRIORITY_ONE } from "../../mock/mockAtlasData";
import type { ScoreKey } from "../../lib/encoding";
import {
  radiusFor,
  ringVariant,
  scoreColor,
  uncertaintyColor,
  valueForScore,
} from "../../lib/encoding";
import type { ViewMode } from "../../lib/types";
import { GRATICULE_LATS, GRATICULE_LONS, gridX, gridY, projectPoint } from "../../lib/projection";

const W = 1000;
const H = 600;
const PAD = 54;

type AtlasMapProps = {
  geos: Geo[];
  activeScore: ScoreKey;
  viewMode: ViewMode;
  outlookOn: boolean;
  selectedCode: string | null;
  onSelect: (code: string) => void;
  activeLayerLabel: string;
};

function fillFor(geo: Geo, activeScore: ScoreKey, viewMode: ViewMode, outlookOn: boolean): string {
  if (outlookOn) {
    if (geo.outlookDisplay === "withhold") return "transparent";
    return scoreColor("gap", geo.outlook2030Flat);
  }
  if (viewMode === "uncertainty") return uncertaintyColor(geo.rankRange);
  if (viewMode === "coverage") return "#64777f"; // neutral: coverage mode reads status via rings, not score
  return scoreColor(activeScore, valueForScore(geo, activeScore));
}

export function AtlasMap({
  geos,
  activeScore,
  viewMode,
  outlookOn,
  selectedCode,
  onSelect,
  activeLayerLabel,
}: AtlasMapProps) {
  const hasSelection = selectedCode !== null;

  const onKey = (event: KeyboardEvent<SVGGElement>, code: string) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onSelect(code);
    }
  };

  return (
    <div className="map-canvas">
      <svg
        className="map-svg"
        viewBox={`0 0 ${W} ${H}`}
        preserveAspectRatio="xMidYMid slice"
        role="img"
        aria-label={`Map of 22 Pacific geographies as centroid points. Active layer: ${activeLayerLabel}. A comparative screen, not a definitive ranking.`}
      >
        <defs>
          <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <rect width="6" height="6" fill="#22323b" />
            <line x1="0" y1="0" x2="0" y2="6" stroke="#7f9aa8" strokeWidth="1.6" />
          </pattern>
        </defs>

        {/* graticule for GIS flavour */}
        <g className="graticule" aria-hidden="true">
          {GRATICULE_LONS.map((lon) => (
            <line key={`lon-${lon}`} x1={gridX(lon, W, PAD)} y1={PAD} x2={gridX(lon, W, PAD)} y2={H - PAD} />
          ))}
          {GRATICULE_LATS.map((lat) => (
            <line key={`lat-${lat}`} x1={PAD} y1={gridY(lat, H, PAD)} x2={W - PAD} y2={gridY(lat, H, PAD)} />
          ))}
        </g>

        {geos.map((geo) => {
          const { x, y } = projectPoint(geo.lon, geo.lat, W, H, PAD);
          const r = radiusFor(geo.indicators);
          const variant = ringVariant(geo.reportingStatus);
          const fill = fillFor(geo, activeScore, viewMode, outlookOn);
          const isSelected = geo.code === selectedCode;
          const isPriority = viewMode === "coverage" && PRIORITY_ONE.includes(geo.code);
          const withheld = outlookOn && geo.outlookDisplay === "withhold";
          const dimmed = (hasSelection && !isSelected) || (viewMode === "coverage" && !isPriority && geo.storyPriority > 3);

          return (
            <g
              key={geo.code}
              className={`atlas-point${dimmed ? " atlas-point--dim" : ""}`}
              role="button"
              tabIndex={0}
              aria-label={`${geo.name}. ${geo.storyLabel}. Rank moves ${geo.rankMin} to ${geo.rankMax}.`}
              onClick={() => onSelect(geo.code)}
              onKeyDown={(e) => onKey(e, geo.code)}
            >
              {isPriority && <circle cx={x} cy={y} r={r + 9} className="atlas-point__priority" />}

              {/* fill body */}
              {variant === "hatch" ? (
                <circle cx={x} cy={y} r={r} fill="url(#hatch)" stroke="#9fb4bf" strokeWidth={1.6} strokeDasharray="2 3" />
              ) : variant === "dashed" ? (
                <circle cx={x} cy={y} r={r} fill={withheld ? "transparent" : fill} fillOpacity={withheld ? 0 : 0.35} stroke="#cdd6dc" strokeWidth={2} strokeDasharray="5 4" />
              ) : (
                <circle cx={x} cy={y} r={r} fill={withheld ? "transparent" : fill} stroke={withheld ? "#9fb4bf" : "rgba(8,18,26,0.55)"} strokeWidth={withheld ? 1.4 : 1.2} strokeDasharray={withheld ? "2 3" : undefined} />
              )}

              {/* selection callout: brackets, not another ring */}
              {isSelected && (
                <g className="atlas-point__select" aria-hidden="true">
                  {[
                    [-1, -1], [1, -1], [-1, 1], [1, 1],
                  ].map(([sx, sy], i) => {
                    const d = r + 8;
                    const len = 7;
                    return (
                      <path
                        key={i}
                        d={`M ${x + sx * d} ${y + sy * d - sy * len} L ${x + sx * d} ${y + sy * d} L ${x + sx * d - sx * len} ${y + sy * d}`}
                      />
                    );
                  })}
                  <text x={x} y={y - r - 14} textAnchor="middle" className="atlas-point__label">
                    {geo.name}
                  </text>
                </g>
              )}

              {(isPriority || (isSelected && viewMode !== "coverage")) && !isSelected && (
                <text x={x} y={y - r - 6} textAnchor="middle" className="atlas-point__code">
                  {geo.code}
                </text>
              )}
            </g>
          );
        })}
      </svg>

      <p className="map-note">Centroid fallback, not boundary geometry. Mockup composition - not a true projection.</p>
    </div>
  );
}
