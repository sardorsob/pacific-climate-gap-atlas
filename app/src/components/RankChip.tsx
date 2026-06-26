import type { Geo } from "../mock/mockAtlasData";
import { rankChipText } from "../lib/encoding";

// Never show a bare rank: this chip pairs the rank range with a robustness tag.
export function RankChip({ geo }: { geo: Geo }) {
  return (
    <span className="rank-chip" title="Leave-one-indicator stress test">
      <span className="rank-chip__range">{rankChipText(geo)}</span>
      <span className={`rank-chip__tag rank-chip__tag--${geo.robustness}`}>
        {geo.robustness}
      </span>
    </span>
  );
}
