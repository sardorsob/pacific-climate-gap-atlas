// Simple, honest equirectangular projection for the mockup map.
// The Pacific straddles the antimeridian, so western longitudes (e.g. -170)
// are shifted by +360 to keep the region contiguous. This is a schematic
// composition, not a true geographic projection.

const LON_MIN = 130;
const LON_MAX = 240;
const LAT_MIN = -30;
const LAT_MAX = 20;

export type Point = { x: number; y: number };

export function projectPoint(
  lon: number,
  lat: number,
  width: number,
  height: number,
  pad: number,
): Point {
  const lonShift = lon < 0 ? lon + 360 : lon;
  const fx = (lonShift - LON_MIN) / (LON_MAX - LON_MIN);
  const fy = (LAT_MAX - lat) / (LAT_MAX - LAT_MIN);
  return {
    x: pad + fx * (width - pad * 2),
    y: pad + fy * (height - pad * 2),
  };
}

// Longitude gridlines (graticule) for GIS flavour, in shifted-lon space.
export const GRATICULE_LONS = [140, 160, 180, 200, 220];
export const GRATICULE_LATS = [-20, -10, 0, 10];

export function gridX(lonShift: number, width: number, pad: number): number {
  return pad + ((lonShift - LON_MIN) / (LON_MAX - LON_MIN)) * (width - pad * 2);
}

export function gridY(lat: number, height: number, pad: number): number {
  return pad + ((LAT_MAX - lat) / (LAT_MAX - LAT_MIN)) * (height - pad * 2);
}
