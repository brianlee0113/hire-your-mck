"""Build the compact map outlines the renderer draws (renderer/geo/*.json) from Natural Earth GeoJSON.

Natural Earth (naturalearthdata.com) is in the public domain. Download the two files, then run:
  python tools/geo/build_geo.py ne_110m_admin_0_countries.geojson ne_50m_admin_1_states_provinces_lakes.geojson

Output, per geography: {"width", "height", "regions": {code: {"name", "paths": [[x, y, x, y, ...], ...], "label": [x, y]}}}
in projected units (0..width, 0..height, y down), simplified and rounded so the files stay small.
- world.json: Miller cylindrical projection, cropped to 58°S–83°N, Antarctica dropped, keyed by ISO 3166-1 alpha-3.
- us_states.json: Albers equal-area conic (US standard parallels), Alaska and Hawaii as insets, keyed by USPS code.
"""
import json, math, sys

# ---- projections ------------------------------------------------------------------------------
A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
M = math.sqrt(3) / 2


def equal_earth(lon, lat):
    p = math.radians(lat)
    th = math.asin(M * math.sin(p))
    t2 = th * th
    t6 = t2 * t2 * t2
    x = math.radians(lon) * math.cos(th) / (M * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)))
    y = th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))
    return x, -y


def miller(lon, lat):
    """Miller cylindrical, the look of world maps in the learned decks (Greenland large, no Antarctica)."""
    lat = max(-58.0, min(83.0, lat))  # crop as the reference maps do
    return math.radians(lon), -1.25 * math.log(math.tan(math.pi / 4 + 0.4 * math.radians(lat)))


def albers(lon, lat, lon0=-96.0, lat0=37.5, p1=29.5, p2=45.5):
    f1, f2, f0 = map(math.radians, (p1, p2, lat0))
    n = (math.sin(f1) + math.sin(f2)) / 2
    c = math.cos(f1) ** 2 + 2 * n * math.sin(f1)
    r0 = math.sqrt(c - 2 * n * math.sin(f0)) / n
    r = math.sqrt(c - 2 * n * math.sin(math.radians(lat))) / n
    th = n * math.radians(lon - lon0)
    return r * math.sin(th), -(r0 - r * math.cos(th))


# Insets in lower-48 Albers units: (left, top, width) — Alaska and Hawaii sit under the south-west, as in most US maps.
INSETS = {"AK": (-0.37, 0.07, 0.19), "HI": (-0.165, 0.15, 0.085)}
KEEP = {"AK": (-170.0, -129.0), "HI": (-161.0, -154.0)}  # drop the far Aleutians and the north-western Hawaiian islands


def albers_usa(lon, lat, state):
    if state == "AK":
        return albers(lon, lat, lon0=-154, lat0=50, p1=55, p2=65)
    if state == "HI":
        return albers(lon, lat, lon0=-157, lat0=3, p1=8, p2=18)
    return albers(lon, lat)


def fit_insets(regions):
    """Scale and move the Alaska and Hawaii outlines into their inset boxes."""
    for code, (x0, y0, w) in INSETS.items():
        if code not in regions:
            continue
        pts = [p for r in regions[code]["rings"] for p in r]
        bx0, bx1 = min(p[0] for p in pts), max(p[0] for p in pts)
        by0 = min(p[1] for p in pts)
        s = w / (bx1 - bx0)
        regions[code]["rings"] = [[(x0 + (x - bx0) * s, y0 + (y - by0) * s) for x, y in r] for r in regions[code]["rings"]]


# ---- simplification -----------------------------------------------------------------------------
def _dp(pts, tol):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy) or 1e-12
    dmax, idx = 0.0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / norm
        if d > dmax:
            dmax, idx = d, i
    if dmax <= tol:
        return [pts[0], pts[-1]]
    return _dp(pts[: idx + 1], tol)[:-1] + _dp(pts[idx:], tol)


def simplify(ring, tol):
    if len(ring) < 8:
        return ring
    out = _dp(ring, tol)
    return out if len(out) >= 4 else ring


def polygons(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    if geom["type"] == "MultiPolygon":
        return geom["coordinates"]
    return []


def area(ring):
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]))) / 2


def build(features, key, name, project, tol, min_area, width, insets=False):
    regions = {}
    pts_all = []
    for f in features:
        code = key(f["properties"])
        if not code:
            continue
        rings = []
        for poly in polygons(f["geometry"]):
            lo, hi = KEEP.get(code, (-999, 999)) if insets else (-999, 999)
            if not all(lo <= lon <= hi for lon, _ in poly[0]):
                continue
            ring = [project(lon, lat, code) for lon, lat in poly[0]]  # outer ring only; lakes and holes are not drawn
            if area(ring) < min_area:
                continue
            rings.append(simplify(ring, tol))
        if rings:
            regions.setdefault(code, {"name": name(f["properties"]), "rings": []})["rings"] += rings
            pts_all += [p for r in rings for p in r]
    if insets:
        fit_insets(regions)
        pts_all = [p for r in regions.values() for ring in r["rings"] for p in ring]
    x0 = min(p[0] for p in pts_all); x1 = max(p[0] for p in pts_all)
    y0 = min(p[1] for p in pts_all); y1 = max(p[1] for p in pts_all)
    s = width / (x1 - x0)
    out = {}
    for code, r in regions.items():
        paths, big, best = [], None, -1
        for ring in r["rings"]:
            q = [((x - x0) * s, (y - y0) * s) for x, y in ring]
            a = area(q)
            if a > best:
                best, big = a, q
            paths.append([round(v, 1) for p in q for v in p])
        a2 = cx = cy = 0.0  # area centroid of the largest ring: where a label or bubble goes
        for (ax_, ay_), (bx_, by_) in zip(big, big[1:] + big[:1]):
            cr = ax_ * by_ - bx_ * ay_
            a2 += cr; cx += (ax_ + bx_) * cr; cy += (ay_ + by_) * cr
        cx, cy = (cx / (3 * a2), cy / (3 * a2)) if a2 else (big[0][0], big[0][1])
        out[code] = {"name": r["name"], "paths": paths, "label": [round(cx, 1), round(cy, 1)]}
    return {"width": round(width, 1), "height": round((y1 - y0) * s, 1), "regions": dict(sorted(out.items()))}


def main(world_path, states_path, out_dir="renderer/geo"):
    import os
    os.makedirs(out_dir, exist_ok=True)
    w = json.load(open(world_path))

    def iso3(p):
        c = p.get("ISO_A3")
        if c in (None, "-99"):
            c = p.get("ADM0_A3")  # France, Norway and a few others carry -99 in ISO_A3
        return None if p.get("ADM0_A3") == "ATA" else c
    world = build(w["features"], iso3, lambda p: p.get("NAME_EN") or p.get("NAME"),
                  lambda lon, lat, _c: miller(lon, lat), tol=0.004, min_area=2e-5, width=1000)
    json.dump(world, open(f"{out_dir}/world.json", "w"), separators=(",", ":"))
    s = json.load(open(states_path))
    us = [f for f in s["features"] if f["properties"].get("iso_a2") == "US"]
    def postal(p):
        c = (p.get("postal") or p.get("iso_3166_2", "US-")[3:])
        return c or None
    states = build(us, postal, lambda p: p.get("name"), albers_usa, tol=0.0015, min_area=2e-6, width=1000, insets=True)
    json.dump(states, open(f"{out_dir}/us_states.json", "w"), separators=(",", ":"))
    for n in ("world", "us_states"):
        d = json.load(open(f"{out_dir}/{n}.json"))
        print(n, len(d["regions"]), "regions", os.path.getsize(f"{out_dir}/{n}.json") // 1024, "KB")


if __name__ == "__main__":
    main(*sys.argv[1:])
