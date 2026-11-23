"""Simplified Natural Earth world map (studio/tvs/world.geojson) cropped to Europe-Africa-Asia, equirectangular."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(H + '/../../../studio/tvs/world.geojson'))
L0, L1, A0, A1, W = -20, 135, -12, 62, 1000
S = W / (L1 - L0); HH = (A1 - A0) * S
def P(lon, lat): return ((lon - L0) * S, (A1 - lat) * S)
def ring(r):
    pts = []; last = None
    for lon, lat in r:
        x, y = P(lon, lat); q = (round(x), round(y))
        if q != last: pts.append(q); last = q
    if len(pts) < 3: return ''
    if all(x < -5 or x > W + 5 for x, _ in pts) or all(y < -5 or y > HH + 5 for _, y in pts): return ''
    return 'M' + 'L'.join(f'{x},{y}' for x, y in pts) + 'Z'
def svg(fill=None, cls='wm'):
    fill = fill or {}
    out = [f'<svg class="{cls}" viewBox="0 0 {W} {HH:.0f}" width="{W}" height="{HH:.0f}">']
    for f in G['features']:
        a3 = f['properties']['ADM0_A3']; g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        d = ''.join(ring(p[0]) for p in polys)
        if not d: continue
        out.append(f'<path id="{cls}-{a3}" d="{d}" style="fill:{fill.get(a3, "#E9E2CF")}"/>')
    out.append('</svg>')
    return ''.join(out)
if __name__ == '__main__':
    s = svg(); print(len(s), HH)
