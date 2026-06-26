import { HelpCircle } from "lucide-react";
import { ATLAS_GEOS, PRIORITY_ONE } from "../../mock/mockAtlasData";

// Shown in the "Where the data goes quiet" view when nothing is selected.
// Makes data absence an inspectable finding, never "no data = no infrastructure".
export function DataQuietCallout({ onPick }: { onPick: (code: string) => void }) {
  const zero = ATLAS_GEOS.filter((g) => g.reportingStatus === "reported_zero_latest_count");
  const missing = ATLAS_GEOS.filter((g) => g.reportingStatus === "missing_monitoring_dataset_row");
  const priority = PRIORITY_ONE.join(", ");

  return (
    <aside className="panel" aria-label="Where the data goes quiet">
      <p className="eyebrow">Signature view</p>
      <h1 className="panel__name">Where the data goes quiet</h1>
      <p className="panel__lede">
        High apparent gap and a thin official record often overlap. The high-gap / low-monitoring
        group here is <strong>{priority}</strong>. Two kinds of silence look different on the map.
      </p>

      <section className="quiet-card quiet-card--zero">
        <h2 className="panel__h"><HelpCircle aria-hidden="true" size={16} /> What does zero mean?</h2>
        <p className="quiet-card__geos">{zero.map((g) => g.name).join(", ")}</p>
        <p className="quiet-card__caveat">
          Latest official monitoring row reports 0; verify source semantics before interpreting this as
          no monitoring infrastructure.
        </p>
        <div className="quiet-card__chips">
          {zero.map((g) => (
            <button key={g.code} type="button" className="chip" onClick={() => onPick(g.code)}>{g.code}</button>
          ))}
        </div>
      </section>

      <section className="quiet-card quiet-card--missing">
        <h2 className="panel__h"><HelpCircle aria-hidden="true" size={16} /> Why is this blank?</h2>
        <p className="quiet-card__geos">{missing.map((g) => g.name).join(", ")}</p>
        <p className="quiet-card__caveat">
          No monitoring rows in processed official data; treat as a reporting gap, not confirmed
          absence.
        </p>
        <div className="quiet-card__chips">
          {missing.map((g) => (
            <button key={g.code} type="button" className="chip" onClick={() => onPick(g.code)}>{g.code}</button>
          ))}
        </div>
      </section>

      <p className="quiet-card__footer">
        A reporting gap is not proof that infrastructure is absent. Monitoring counts are unnormalized
        proxy coverage.
      </p>
    </aside>
  );
}
