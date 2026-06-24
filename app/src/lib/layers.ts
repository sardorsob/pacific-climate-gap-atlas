export type AtlasLayer = {
  id: string;
  label: string;
  description: string;
};

export const atlasLayers: AtlasLayer[] = [
  {
    id: "adaptation_gap_score",
    label: "Adaptation gap",
    description: "Pressure minus visible capacity, shown with missingness caveats.",
  },
  {
    id: "climate_signal",
    label: "Climate signal",
    description: "Observed changes in temperature, rainfall, and sea level indicators.",
  },
  {
    id: "observed_stress",
    label: "Observed stress",
    description: "Disaster-affected people and other stress indicators where available.",
  },
  {
    id: "adaptation_capacity",
    label: "Adaptation capacity",
    description: "Monitoring, infrastructure, and governance proxies.",
  },
];
