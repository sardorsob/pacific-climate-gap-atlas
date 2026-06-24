import { BookOpen, Database, TrendingUp } from "lucide-react";

const cards = [
  {
    icon: TrendingUp,
    label: "Climate signal",
    text: "Temperature, rainfall, and sea-level indicators will summarize change here.",
  },
  {
    icon: Database,
    label: "Adaptation capacity",
    text: "Monitoring, power, fisheries, and governance proxy coverage will appear here.",
  },
  {
    icon: BookOpen,
    label: "Method notes",
    text: "Missingness, source notes, and caveats stay close to every score.",
  },
];

export function CountryPanel() {
  return (
    <aside className="country-panel" aria-label="Country detail panel">
      <p className="eyebrow">Pacific Adaptation Gap Atlas</p>
      <h1>Explore where climate pressure and response capacity are out of balance.</h1>
      <p className="country-panel__intro">
        Select a geography after app data is generated. The panel will show the adaptation
        gap score, pillar evidence, missingness, and source links.
      </p>
      <div className="country-panel__cards">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <section className="evidence-card" key={card.label}>
              <Icon aria-hidden="true" size={20} />
              <div>
                <h2>{card.label}</h2>
                <p>{card.text}</p>
              </div>
            </section>
          );
        })}
      </div>
    </aside>
  );
}
