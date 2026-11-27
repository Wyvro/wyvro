#!/usr/bin/env python3
"""Draws the Wyvro logo as plain SVG paths.

Run from the repository root:  python3 brand/logo.py
It rewrites the .svg files and preview.html next to this script.

The idea: the word is a wyvern seen from the side, facing right. The points of
W, Y, V and R are the spines along its back, and the O is its eye.
"""
import math
import pathlib

HERE = pathlib.Path(__file__).parent

WEIGHT = 15.0   # thickness of every stroke
CAP = 120.0     # height of the letters: top is y=0, baseline is y=CAP
OVER = 2.0      # sharp points poke this far past the top and baseline, so they do not look short

CREAM, INK = "#ebdbb2", "#282828"
EMBER, EMBER_DARK = "#fe8019", "#c2500c"
NIGHT, PARCHMENT = "#1d2021", "#f2e5bc"


# ---------- geometry ----------

def unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    return (dx / n, dy / n)


def intersect(l1, l2):
    """Where two lines cross. A line is (point, direction)."""
    (p, r), (q, s) = l1, l2
    rxs = r[0] * s[1] - r[1] * s[0]
    t = ((q[0] - p[0]) * s[1] - (q[1] - p[1]) * s[0]) / rxs
    return (p[0] + t * r[0], p[1] + t * r[1])


def band(pts, w=WEIGHT, start=None, end=None):
    """Outline of a line through pts drawn w thick, with sharp corners.

    start and end are the lines the two ends are cut along; square by default.
    """
    segs = []
    for a, b in zip(pts, pts[1:]):
        d = unit(a, b)
        n = (-d[1], d[0])
        segs.append((
            ((a[0] + n[0] * w / 2, a[1] + n[1] * w / 2), d),
            ((a[0] - n[0] * w / 2, a[1] - n[1] * w / 2), d),
            n,
        ))
    start = start or (pts[0], segs[0][2])
    end = end or (pts[-1], segs[-1][2])
    left = [intersect(segs[0][0], start)]
    right = [intersect(segs[0][1], start)]
    for s1, s2 in zip(segs, segs[1:]):
        left.append(intersect(s1[0], s2[0]))
        right.append(intersect(s1[1], s2[1]))
    left.append(intersect(segs[-1][0], end))
    right.append(intersect(segs[-1][1], end))
    return left + right[::-1]


def swept(a, b, y=0.0, w=WEIGHT, slant=(1.0, 1.0)):
    """Cut for the end of a stroke at a (b is its other end): a spine swept back
    to the left, with its tip at height y."""
    d = unit(a, b)
    n = (-d[1], d[0])
    edges = [((a[0] + k * n[0] * w / 2, a[1] + k * n[1] * w / 2), d) for k in (1, -1)]
    level = ((0.0, y), (1.0, 0.0))
    for edge, other in (edges, edges[::-1]):
        cut = (intersect(edge, level), slant)
        if intersect(other, cut)[1] >= y - 1e-6:
            return cut


def flat(y):
    return ((0.0, y), (1.0, 0.0))


def fit(pts, targets, w=WEIGHT):
    """Slide corners up or down until their sharp tips land on the target heights."""
    pts = [list(p) for p in pts]
    n = len(pts)
    for _ in range(60):
        out = band(pts, w)
        for i, t in targets.items():
            a, b = out[i], out[2 * n - 1 - i]
            tip = min(a[1], b[1]) if t < pts[i][1] else max(a[1], b[1])
            pts[i][1] += (t - tip) * 0.7
    return [tuple(p) for p in pts]


def shift(poly, dx, dy=0.0):
    return [(x + dx, y + dy) for x, y in poly]


def d_poly(poly):
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in poly) + " Z"


def extent(polys):
    xs = [x for p in polys for x, _ in p]
    return min(xs), max(xs)


# ---------- letters (each drawn with its left edge near x=0) ----------

TOP, BASE = -OVER, CAP + OVER


def letter_w():
    pts = fit([(0, 0), (28, 94), (48.5, 26), (69, 94), (97, 0)], {1: BASE, 2: TOP, 3: BASE})
    return [band(pts, start=swept(pts[0], pts[1]), end=swept(pts[-1], pts[-2]))]


def letter_y():
    pts = [(0, 0), (31, 62), (62, 0)]
    arms = band(pts, start=swept(pts[0], pts[1]), end=swept(pts[-1], pts[-2]))
    stem = band([(31, 62), (31, CAP)], end=flat(CAP))
    return [arms, stem]


def letter_v():
    pts = fit([(0, 0), (35, 98), (70, 0)], {1: BASE})
    return [band(pts, start=swept(pts[0], pts[1]), end=swept(pts[-1], pts[-2]))]


def letter_r(pointed_top=True):
    h = WEIGHT / 2
    stem_pts = [(h, 0), (h, CAP)]
    stem = band(stem_pts, start=swept(stem_pts[0], stem_pts[1]) if pointed_top else flat(0), end=flat(CAP))
    # The bowl leaves the stem along the same 45 degree line as the stem's swept top.
    off = h * math.sqrt(2)
    bx = 45.0
    bowl = band([(h, h + off), (bx, bx + off), (h, 80)])
    leg = band([(11, 69), (52, CAP)], end=flat(CAP))
    return [stem, bowl, leg]


# ---------- the head ----------

RING = 61.0  # outer radius of the O, a touch over half the cap height


def d_circle(cx, cy, r, sweep=0):
    return (
        f"M{cx - r:.2f} {cy:.2f} A{r} {r} 0 1 {sweep} {cx + r:.2f} {cy:.2f} "
        f"A{r} {r} 0 1 {sweep} {cx - r:.2f} {cy:.2f} Z"
    )


def d_ring(cx, cy, r_out=RING, r_in=RING - WEIGHT):
    return d_circle(cx, cy, r_out) + " " + d_circle(cx, cy, r_in, 1)


def d_slit(cx, cy, half=27.0, r=40.0, tilt=0.0):
    """A reptile's pupil: two arcs meeting in points."""
    t = math.radians(tilt)
    dx, dy = half * math.sin(t), half * math.cos(t)
    p, q = (cx + dx, cy - dy), (cx - dx, cy + dy)
    return (
        f"M{p[0]:.2f} {p[1]:.2f} A{r} {r} 0 0 1 {q[0]:.2f} {q[1]:.2f} "
        f"A{r} {r} 0 0 1 {p[0]:.2f} {p[1]:.2f} Z"
    )


def head(cx, cy):
    """The O: a plain ring with a slit pupil. Returns (ink paths, accent paths)."""
    return [d_ring(cx, cy)], [d_slit(cx, cy)]


# ---------- putting the word together ----------

def set_word(groups, gaps):
    """Place letter groups left to right. gaps[i] is the space before group i+1."""
    placed, x = [], 0.0
    for i, polys in enumerate(groups):
        lo, hi = extent(polys)
        dx = x - lo
        placed.append([shift(p, dx) for p in polys])
        x = hi + dx + (gaps[i] if i < len(gaps) else 0.0)
    return placed, x


def wordmark():
    groups, gaps = [letter_w(), letter_y(), letter_v(), letter_r()], [9, 9, 15, 15]
    placed, x = set_word(groups, gaps)
    cx = x + RING
    ink = [d_poly(p) for g in placed for p in g]
    head_ink, accent = head(cx, CAP / 2)
    return ink + head_ink, accent, cx + RING


def svg(ink, accent, box, ink_fill, accent_fill, background=None):
    x, y, w, h = box
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.0f} {y:.0f} {w:.0f} {h:.0f}" role="img" aria-label="Wyvro">']
    if background:
        parts.append(background)
    parts.append(f'<path fill="{accent_fill}" d="{" ".join(accent)}"/>')
    parts.append(f'<g fill="{ink_fill}" fill-rule="evenodd">' + "".join(f'<path d="{d}"/>' for d in ink) + "</g>")
    parts.append("</svg>")
    return "\n".join(parts)


def icon(dark=True):
    """The O on a rounded square, 200 units across with the O filling about 60% of it."""
    ink, accent = head(100.0, 100.0)
    back = f'<rect width="200" height="200" rx="44" fill="{NIGHT if dark else PARCHMENT}"/>'
    return svg(ink, accent, (0, 0, 200, 200), CREAM if dark else INK, EMBER if dark else EMBER_DARK, back)


def main():
    ink, accent, width = wordmark()
    box = (-24, -44, width + 48, CAP + 88)
    out = {
        "wyvro-logo-on-dark.svg": svg(ink, accent, box, CREAM, EMBER),
        "wyvro-logo-on-light.svg": svg(ink, accent, box, INK, EMBER_DARK),
        "wyvro-icon-dark.svg": icon(True),
        "wyvro-icon-light.svg": icon(False),
    }
    for name, text in out.items():
        (HERE / name).write_text(text + "\n")

    sizes = "".join(
        f'<div class="chip" style="width:{px}px;height:{px}px">{out[f"wyvro-icon-{tone}.svg"]}</div>'
        for px in (128, 64, 32, 16) for tone in ("dark", "light")
    )
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Wyvro logo</title>
<style>
  body {{ margin: 0; padding: 32px 40px 56px; background: #282828; color: #d5c4a1;
         font: 15px/1.5 -apple-system, "Helvetica Neue", sans-serif; }}
  h1 {{ font-size: 20px; margin: 0 0 4px; color: #ebdbb2; }}
  h2 {{ font-size: 16px; margin: 36px 0 2px; color: #ebdbb2; }}
  p {{ margin: 0 0 12px; max-width: 70ch; }}
  .pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  .dark, .light {{ border-radius: 10px; padding: 28px 36px; }}
  .dark {{ background: {NIGHT}; }} .light {{ background: {PARCHMENT}; }}
  .pair svg {{ display: block; width: 100%; height: auto; }}
  .row {{ display: flex; align-items: flex-end; gap: 14px; margin-bottom: 14px; }}
  .chip svg {{ display: block; width: 100%; height: 100%; }}
</style></head><body>
  <h1>Wyvro logo</h1>
  <p>The word is a wyvern seen from the side, facing right: the points of the letters are the spines on its back and the O is its eye.</p>
  <section><h2>Logo</h2>
    <div class="pair">
      <div class="dark">{out["wyvro-logo-on-dark.svg"]}</div>
      <div class="light">{out["wyvro-logo-on-light.svg"]}</div>
    </div>
  </section>
  <section><h2>Icon</h2><p>The O alone, for a browser tab or a phone home screen, at 128, 64, 32 and 16 pixels.</p>
  <div class="row">{sizes}</div></section>
</body></html>
"""
    (HERE / "preview.html").write_text(page)
    print("wrote", ", ".join(sorted(out)), "and preview.html")


if __name__ == "__main__":
    main()
