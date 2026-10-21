"""Helpers for the Lecture 6 (persistence) notebook: letters for vertices, example data,
tables and plotting. Feel free to read it.
"""
import gudhi
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display
from matplotlib.patches import Polygon

# ---------------------------------------------------------------------------
# Vertex names: letters in the notebook, integers inside a SimplexTree (as in Lecture 5)
# ---------------------------------------------------------------------------


def letter2int(letter: str) -> int:
    """'A' -> 0, 'B' -> 1, 'C' -> 2, ..."""
    return ord(letter) - ord("A")


def int2letter(i: int) -> str:
    """0 -> 'A', 1 -> 'B', 2 -> 'C', ..."""
    return chr(ord("A") + i)


# the running example of the lecture: where to draw the vertices A, B, C, D
SLIDE_COORDS = np.array([[0.00, 0.30], [0.30, 0.00], [0.57, 0.73], [1.00, 0.60]])

# ---------------------------------------------------------------------------
# Point clouds
# ---------------------------------------------------------------------------

_rng = np.random.default_rng(6)


def _circle(n: int, R: float, center=(0, 0), noise: float = 0.05) -> np.ndarray:
    t = _rng.uniform(0, 2 * np.pi, n)
    return np.column_stack([center[0] + R * np.cos(t), center[1] + R * np.sin(t)]) + _rng.normal(0, noise, (n, 2))


_square = _rng.uniform(-1, 1, (300, 2))
CLOUDS = {
    "circle": _circle(60, 1),
    "two circles": np.vstack([_circle(50, 1, (-1.4, 0)), _circle(30, 0.5, (1.4, 0))]),
    "figure eight": np.vstack([_circle(40, 0.7, (-0.7, 0)), _circle(40, 0.7, (0.7, 0))]),
    "three blobs": np.vstack([_rng.normal(c, 0.15, (25, 2)) for c in [(0, 0), (2, 0.5), (1, 2)]]),
    "disk": _square[(_square ** 2).sum(axis=1) <= 1][:120],
}

# ---------------------------------------------------------------------------
# The letters of Lecture 4: points every 0.05 along the strokes of each capital letter
# ---------------------------------------------------------------------------


def _arc(cx, cy, rx, ry, t0, t1, n=400) -> np.ndarray:
    t = np.radians(np.linspace(t0, t1, n))
    return np.column_stack([cx + rx * np.cos(t), cy + ry * np.sin(t)])


def _resample(poly, h: float) -> np.ndarray:
    """Evenly spaced points (at most h apart) along a polyline, endpoints included."""
    poly = np.asarray(poly, dtype=float)
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(poly, axis=0), axis=1))])
    t = np.linspace(0, s[-1], max(1, int(np.ceil(s[-1] / h))) + 1)
    return np.column_stack([np.interp(t, s, poly[:, 0]), np.interp(t, s, poly[:, 1])])


def stroke_cloud(strokes, h: float = 0.05) -> np.ndarray:
    pts = np.vstack([_resample(s, h) for s in strokes])
    keep = []
    for p in pts:                               # drop the duplicates where strokes meet
        if all(np.linalg.norm(p - q) > 1e-6 for q in keep):
            keep.append(p)
    return np.array(keep)


_H, _M = 1.4, 0.7   # height and middle of a letter; width is 1
_bowl = lambda y, end: np.vstack([[(0, y + 2 * .35)], _arc(0.6, y + .35, .35, .35, 90, -90), [end]])
_qx, _qy = 0.5 + 0.5 * np.cos(np.radians(-45)), _M + _M * np.sin(np.radians(-45))
LETTER_STROKES = {
    "A": [[(0, 0), (0.2, 0.56), (0.5, _H), (0.8, 0.56), (1, 0)], [(0.2, 0.56), (0.8, 0.56)]],
    "B": [[(0, 0), (0, _M), (0, _H)], _bowl(_M, (0, _M)),
          np.vstack([[(0, _M)], _arc(0.65, 0.35, .35, .35, 90, -90), [(0, 0)]])],
    "C": [_arc(0.55, _M, 0.5, _M, 45, 315)],
    "D": [np.vstack([[(0, 0), (0, _H)], _arc(0.3, _M, 0.7, _M, 90, -90), [(0, 0)]])],
    "E": [[(1, _H), (0, _H), (0, _M), (0, 0), (1, 0)], [(0, _M), (0.8, _M)]],
    "F": [[(1, _H), (0, _H), (0, _M), (0, 0)], [(0, _M), (0.8, _M)]],
    "G": [np.vstack([_arc(0.5, _M, 0.5, _M, 45, 360), [(0.55, _M)]])],
    "H": [[(0, 0), (0, _M), (0, _H)], [(1, 0), (1, _M), (1, _H)], [(0, _M), (1, _M)]],
    "I": [[(0.5, 0), (0.5, _H)]],
    "J": [np.vstack([[(0.8, _H)], _arc(0.45, 0.4, 0.35, 0.4, 0, -180)])],
    "K": [[(0, 0), (0, _M), (0, _H)], [(1, _H), (0, _M), (1, 0)]],
    "L": [[(0, _H), (0, 0), (1, 0)]],
    "M": [[(0, 0), (0, _H), (0.5, 0.5), (1, _H), (1, 0)]],
    "N": [[(0, 0), (0, _H), (1, 0), (1, _H)]],
    "O": [_arc(0.5, _M, 0.5, _M, 0, 360)],
    "P": [[(0, 0), (0, _M), (0, _H)], _bowl(_M, (0, _M))],
    "Q": [_arc(0.5, _M, 0.5, _M, -45, 315), [(_qx, _qy), (1.1, -0.1)]],
    "R": [[(0, 0), (0, _M), (0, _H)], _bowl(_M, (0.35, _M)), [(0.35, _M), (0, _M)], [(0.35, _M), (1, 0)]],
    "S": [_arc(0.5, 1.05, 0.45, 0.35, 20, 270), _arc(0.5, 0.35, 0.45, 0.35, 90, -160)],
    "T": [[(0, _H), (0.5, _H), (1, _H)], [(0.5, _H), (0.5, 0)]],
    "U": [np.vstack([[(0, _H)], _arc(0.5, 0.5, 0.5, 0.5, 180, 360), [(1, _H)]])],
    "V": [[(0, _H), (0.5, 0), (1, _H)]],
    "W": [[(0, _H), (0.25, 0), (0.5, 0.9), (0.75, 0), (1, _H)]],
    "X": [[(0, 0), (0.5, _M)], [(1, _H), (0.5, _M)], [(0, _H), (0.5, _M)], [(1, 0), (0.5, _M)]],
    "Y": [[(0, _H), (0.5, _M)], [(1, _H), (0.5, _M)], [(0.5, _M), (0.5, 0)]],
    "Z": [[(0, _H), (1, _H), (0, 0), (1, 0)]],
}
LETTERS = {L: stroke_cloud(s) for L, s in LETTER_STROKES.items()}


def _alpha(points) -> gudhi.SimplexTree:
    """The alpha filtration of a point cloud, with radii (not squared radii) as filtration values."""
    return gudhi.AlphaComplex(points=points).create_simplex_tree(output_squared_values=False)


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------


def show_table(fn, n: int, title: str, strict: bool = False, infinity: bool = False) -> None:
    """A table with fn(i, j) for 1 <= i <= j <= n (i < j if strict), laid out as in the lecture:
    one column per i (1 to n, left to right) and one row per j (n down to 1, top to bottom), like the
    axes of a persistence diagram. With infinity=True there is one more row on top, j = n + 1 (infinity)."""
    columns = list(range(1, n + 1))
    rows = list(range(n + 1 if infinity else n, 0, -1))
    data = []
    for j in rows:
        data.append([fn(i, j) if (i < j if strict else i <= j) else "" for i in columns])
    table = pd.DataFrame(data, index=[f"j = {j}" if j <= n else "j = ∞" for j in rows],
                         columns=[f"i = {i}" for i in columns])
    display(table.style.set_caption(title))


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------


def draw(points, complex_, ax=None, title=None, ms=30, lw=1.2, labels=None, alpha=0.6) -> plt.Axes:
    """Draw a complex (SimplexTree or list of simplices) with vertex i at points[i].
    labels=True writes the vertex letters A, B, C, ...; a list of strings writes those instead."""
    simplices = [s for s, _ in complex_.get_simplices()] \
        if hasattr(complex_, "get_simplices") else [list(s) for s in complex_]
    points = np.asarray(points, dtype=float)
    if ax is None:
        _, ax = plt.subplots(figsize=(4, 4))
    for s in simplices:
        if len(s) == 2:
            ax.plot(*points[s].T, color="black", lw=lw, zorder=2)
        elif len(s) == 3:
            ax.add_patch(Polygon(points[s], color="#7FB3D5", alpha=alpha, zorder=1))
    vertices = [s[0] for s in simplices if len(s) == 1]
    ax.scatter(*points[vertices].T, s=ms, color="black", zorder=3)
    if labels is True:
        labels = [int2letter(i) for i in range(len(points))]
    if labels:
        for v in vertices:
            ax.annotate(labels[v], points[v], xytext=(6, 4), textcoords="offset points", fontsize=11)
    ax.set_aspect("equal"); ax.margins(0.12); ax.set_axis_off()
    ax.set_title(title, fontsize=10)
    return ax


def plot_filtration(st: gudhi.SimplexTree, coords, ncols: int = 8) -> None:
    """One panel per filtration value a_1 < a_2 < ...: the simplices with value <= a_i, i.e. K_i.
    Vertices that are not in K_i yet are grey circles."""
    values = sorted(set(v for _, v in st.get_simplices()))
    coords = np.asarray(coords, dtype=float)
    ncols = min(ncols, len(values))
    nrows = int(np.ceil(len(values) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(2.1 * ncols, 2.1 * nrows), squeeze=False)
    for ax in axes.flat:
        ax.set_axis_off()
    for i, a in enumerate(values):
        ax = axes.flat[i]
        ax.scatter(*coords.T, s=40, facecolors="none", edgecolors="#BBBBBB", zorder=0)
        for v in range(len(coords)):
            if not st.find([v]) or st.filtration([v]) > a:       # not in K_i yet: grey name
                ax.annotate(int2letter(v), coords[v], xytext=(6, 4), textcoords="offset points", fontsize=11, color="#AAAAAA")
        draw(coords, [s for s, v in st.get_simplices() if v <= a], ax=ax, labels=True)
        ax.set_title(f"$K_{{{i + 1}}}$", fontsize=11)
    plt.tight_layout(); plt.show()


def plot_radii(points, radii: list[float], classify, name: str = "") -> None:
    """One panel per radius: the alpha complex of `points` at that radius, titled with classify."""
    fig, axes = plt.subplots(1, len(radii), figsize=(3.2 * len(radii), 3.6))
    for ax, r in zip(np.atleast_1d(axes), radii):
        st = _alpha(points)
        st.prune_above_filtration(r)
        draw(points, st, ax=ax, ms=6, lw=0.8)
        for p in points:
            ax.add_patch(plt.Circle(p, r, color="#C39BD3", alpha=0.15, lw=0, zorder=0))
        ax.set_title(f"{name} at r = {r}: (b0, b1) = {classify(points, r)}", fontsize=10)
    plt.tight_layout(); plt.show()
