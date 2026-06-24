import { AtlasMap } from "./components/map/AtlasMap";
import { LayerControls } from "./components/controls/LayerControls";
import { CountryPanel } from "./components/panels/CountryPanel";
import { atlasLayers } from "./lib/layers";

export function App() {
  return (
    <main className="atlas-shell">
      <section className="atlas-map-region" aria-label="Pacific Adaptation Gap Atlas map">
        <AtlasMap />
        <LayerControls layers={atlasLayers} selectedLayerId="adaptation_gap_score" />
      </section>
      <CountryPanel />
    </main>
  );
}
