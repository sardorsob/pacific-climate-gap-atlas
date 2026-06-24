import { Map } from "lucide-react";

export function AtlasMap() {
  return (
    <div className="map-canvas" role="img" aria-label="Draft Pacific region map placeholder">
      <div className="map-canvas__grid" />
      <div className="map-canvas__label">
        <Map aria-hidden="true" size={22} />
        <span>GIS layer canvas</span>
      </div>
      <div className="map-canvas__note">
        App-ready GeoJSON will render here after TASK-005.
      </div>
    </div>
  );
}
