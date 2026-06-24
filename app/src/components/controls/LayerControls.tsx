import type { AtlasLayer } from "../../lib/layers";

type LayerControlsProps = {
  layers: AtlasLayer[];
  selectedLayerId: string;
};

export function LayerControls({ layers, selectedLayerId }: LayerControlsProps) {
  return (
    <nav className="layer-controls" aria-label="Atlas layers">
      {layers.map((layer) => (
        <button
          className="layer-controls__button"
          aria-pressed={layer.id === selectedLayerId}
          key={layer.id}
          type="button"
          title={layer.description}
        >
          {layer.label}
        </button>
      ))}
    </nav>
  );
}
