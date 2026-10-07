"""Helpers for the Lecture 4 (Homology) notebook: given functions, example complexes,
point clouds, plotting, and the checkers for every exercise.

Nothing in here solves an exercise. Feel free to read it.
"""
import itertools
from typing import Callable, Iterable

import gudhi
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource
from matplotlib.patches import Circle, Polygon

Simplex = tuple[int, ...]                  # e.g. (1, 2, 4), vertices sorted
Chain = tuple[list[Simplex], list[int]]    # (simplices, coefficients), e.g. ([(0, 1), (1, 2)], [2, -1])

# ---------------------------------------------------------------------------
# Given functions
# ---------------------------------------------------------------------------


def chain_dim(chain: Chain) -> int | None:
    """Dimension p of a p-chain `(simplices, coeffs)`, or None for the zero chain `([], [])`.

    Raises ValueError if the chain is not valid: the lists have different lengths,
    a simplex is not a non-empty tuple of distinct sorted vertices, or the simplices
    have different dimensions.
    """
    simplices, coeffs = chain
    if len(simplices) != len(coeffs):
        raise ValueError("need exactly one coefficient per simplex")
    for s in simplices:
        if not isinstance(s, tuple) or len(s) == 0:
            raise ValueError(f"{s!r} is not a non-empty tuple")
        if list(s) != sorted(set(s)):
            raise ValueError(f"{s!r}: vertices must be distinct and sorted")
    dims = {len(s) - 1 for s in simplices}
    if len(dims) > 1:
        raise ValueError(f"simplices of different dimensions {sorted(dims)}")
    return dims.pop() if dims else None


def simplices_of_dim(st: gudhi.SimplexTree, p: int) -> list[Simplex]:
    """Sorted list of the p-simplices of a SimplexTree, as tuples."""
    return sorted(tuple(s) for s, _ in st.get_skeleton(p) if len(s) == p + 1)


def rank_mod2(M: np.ndarray) -> int:
    """Rank of a 0/1 matrix over Z_2 (Gaussian elimination with XOR)."""
    M = np.array(M, dtype=np.uint8) % 2
    rank = 0
    for c in range(M.shape[1]):
        nonzero = np.nonzero(M[rank:, c])[0]
        if len(nonzero) == 0:                     # no pivot in this column
            continue
        pivot = rank + nonzero[0]
        M[[rank, pivot]] = M[[pivot, rank]]       # move the pivot row up
        others = np.nonzero(M[:, c])[0]
        M[others[others != rank]] ^= M[rank]      # clear the rest of the column
        rank += 1
        if rank == M.shape[0]:
            break
    return rank


def complex_from(maximal_simplices: Iterable[Simplex]) -> gudhi.SimplexTree:
    """SimplexTree containing the given simplices and all their faces."""
    st = gudhi.SimplexTree()
    for s in maximal_simplices:
        st.insert(list(s))
    return st


def enclosing_radius(pts: np.ndarray) -> float:
    """Radius of the smallest ball containing 2 or 3 points in the plane (from last session)."""
    if len(pts) == 2:
        return np.linalg.norm(pts[0] - pts[1]) / 2
    a, b, c = pts
    sides = np.array([np.linalg.norm(b - c), np.linalg.norm(a - c), np.linalg.norm(a - b)])
    if sides.max() ** 2 >= (sides ** 2).sum() - sides.max() ** 2:   # obtuse: the longest edge decides
        return sides.max() / 2
    area = abs((b - a)[0] * (c - a)[1] - (b - a)[1] * (c - a)[0]) / 2
    return sides.prod() / (4 * area)                               # acute: the circumradius


def cech(points: np.ndarray, r: float, max_dim: int = 2) -> gudhi.SimplexTree:
    """Cech complex C^r(points) as a SimplexTree, up to triangles.

    Same complex as last session's brute force, but only triples of points that are
    pairwise within 2r are tested (no other triple can have a common point).
    """
    points = np.asarray(points, dtype=float)
    n = len(points)
    dist = np.linalg.norm(points[:, None] - points[None], axis=-1)
    nbrs = [set(np.nonzero(dist[i] <= 2 * r)[0]) - {i} for i in range(n)]   # balls that meet ball i
    st = gudhi.SimplexTree()
    for i in range(n):
        st.insert([i])
    edges = [(i, j) for i in range(n) for j in nbrs[i] if i < j]
    for e in edges:
        st.insert(list(e))
    if max_dim >= 2:
        for i, j in edges:
            for k in nbrs[i] & nbrs[j]:
                if k > j and enclosing_radius(points[[i, j, k]]) <= r:
                    st.insert([i, j, k])
    return st


def _gudhi_betti(st: gudhi.SimplexTree) -> list[int]:
    st.compute_persistence(homology_coeff_field=2, persistence_dim_max=True)
    return st.betti_numbers()


def _gudhi_boundary(st: gudhi.SimplexTree, simplex: Simplex) -> Chain:
    faces = sorted(tuple(f) for f, _ in st.get_boundaries(list(simplex)))
    return faces, [1] * len(faces)


# ---------------------------------------------------------------------------
# Example complexes
# ---------------------------------------------------------------------------

K = complex_from([(0, 4), (0, 3), (1, 2), (1, 4), (2, 3), (1, 2, 4)])   # 5 edges and the triangle [1,2,4]
K_COORDS = np.array([[0.22, 0.90], [1.52, 1.55], [1.00, 0.70], [0.47, 0.30], [0.80, 1.48]])
K3 = complex_from([(0, 2, 4), (0, 2, 3), (0, 3, 4), (2, 3, 4), (1, 4), (1, 2)])   # hollow tetrahedron [0,2,3,4] + edges [1,2], [1,4]
TORUS = complex_from([tuple(sorted((i % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)] +
                     [tuple(sorted((i % 7, (i + 2) % 7, (i + 3) % 7))) for i in range(7)])
TET = complex_from([(0, 1, 2, 3)])
HOLLOW_TET = complex_from(itertools.combinations(range(4), 3))
EMPTY_TRIANGLE = complex_from([(0, 1), (1, 2), (0, 2)])



def _torus_grid(n: int, m: int, R: float, r: float, cx: float) -> tuple[np.ndarray, list[Simplex]]:
    """An n x m grid on the torus around (cx, 0, 0), with big radius R and tube radius r.
    Vertex (i, j) has index i * m + j, at angle u = 2 pi (i - 1/2) / n around the big circle and
    v = 2 pi (j - 1/2) / m around the tube, so square (0, 0) is centred on u = v = 0.
    Square (i, j) is split into two triangles, numbered 2 (i m + j) and 2 (i m + j) + 1."""
    u = 2 * np.pi * (np.arange(n) - 0.5) / n
    v = 2 * np.pi * (np.arange(m) - 0.5) / m
    U, V = np.meshgrid(u, v, indexing="ij")
    points = np.column_stack([(cx + (R + r * np.cos(V)) * np.cos(U)).ravel(),
                              ((R + r * np.cos(V)) * np.sin(U)).ravel(),
                              (r * np.sin(V)).ravel()])
    triangles = []
    for i in range(n):
        for j in range(m):
            a, b = i * m + j, (i + 1) % n * m + j                          # the corners of square (i, j)
            c, d = (i + 1) % n * m + (j + 1) % m, i * m + (j + 1) % m
            triangles += [(a, b, c), (a, c, d)]
    return points, triangles


def _double_torus(n: int = 10, m: int = 6, R: float = 1.0, r: float = 0.45) -> tuple[np.ndarray, list[Simplex]]:
    """A triangulated double torus: two n x m torus grids side by side, each with one square
    removed where they meet (at x = 0), glued along the four edges of that square."""
    c = (R + r * np.cos(np.pi / m)) * np.cos(np.pi / n)       # puts the corners of both squares at x = 0
    A, tri_A = _torus_grid(n, m, R, r, -c)
    B, tri_B = _torus_grid(n, m, R, r, +c)
    h = n // 2                                                # square (0, 0) of A faces +x, square (h, 0) of B faces -x
    del tri_A[0:2]
    del tri_B[2 * h * m: 2 * h * m + 2]
    glue = {(h + 1) * m: 0, h * m: m, h * m + 1: m + 1, (h + 1) * m + 1: 1}   # corner of B -> the same corner of A
    new_index, points = {}, list(A)
    for v in range(n * m):
        if v in glue:
            new_index[v] = glue[v]
        else:
            new_index[v] = len(points)
            points.append(B[v])
    triangles = tri_A + [tuple(new_index[v] for v in t) for t in tri_B]
    return np.array(points), [tuple(sorted(t)) for t in triangles]


DOUBLE_TORUS_COORDS, _double_torus_triangles = _double_torus()

ZOO = {   # Section 7: five shapes to predict
    "shape 1": complex_from([(0, 1, 2)]),                                            # a triangle
    "shape 2": complex_from([(0, 1), (1, 2), (2, 3), (0, 3), (0, 2)]),               # a square with a diagonal, only edges
    "shape 3": complex_from([(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]),       # shape 2, cut along the diagonal
    "shape 4": complex_from([(0, 2, 3), (2, 3, 5), (0, 3, 4), (0, 1, 4), (1, 4, 5), (1, 2, 5)]),   # slide 17: a ring
    "shape 5": complex_from(_double_torus_triangles),                                # a (hollow) double torus
}
ZOO_COORDS = {
    "shape 1": np.array([[0, 0], [1, 0], [0.5, 0.87]]),
    "shape 2": np.array([[0, 0], [1, 0], [1, 1], [0, 1]]),
    "shape 3": np.array([[0, 0], [1, 0], [1, 1], [-0.2, 0.2], [0.8, 1.2], [-0.2, 1.2]]),
    "shape 4": np.array([[0.90, 1.22], [1.52, 0.30], [0.28, 0.30], [0.90, 0.86], [1.14, 0.50], [0.66, 0.50]]),
    "shape 5": DOUBLE_TORUS_COORDS,                                                  # in 3D
}
ZOO_LABELS = {"shape 5": "shape 5 (double torus)"}   # panel titles, when not just the name

# ---------------------------------------------------------------------------
# Point clouds
# ---------------------------------------------------------------------------


def circle_points(R: float, h: float = 0.1, center=(0, 0)) -> np.ndarray:
    n = int(np.ceil(2 * np.pi * R / h))
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.column_stack([center[0] + R * np.cos(t), center[1] + R * np.sin(t)])


def disk_points(R: float, h: float = 0.1) -> np.ndarray:
    g = np.arange(-R, R + h / 2, h)
    return np.array([(x, y) for x in g for y in g if x * x + y * y <= R * R + 1e-9])


SHAPES = {   # name -> (points, (beta_0, beta_1) we expect)
    "circle, R = 1":        (circle_points(1), (1, 1)),
    "circle, R = 2":        (circle_points(2), (1, 1)),
    "disk":                 (disk_points(1), (1, 0)),
    "two touching circles": (np.unique(np.round(np.vstack([circle_points(1, center=(-1, 0)),
                                                           circle_points(1, center=(1, 0))]), 9), axis=0), (1, 2)),
    "two separate circles": (np.vstack([circle_points(1, center=(-1.5, 0)),
                                        circle_points(1, center=(1.5, 0))]), (2, 2)),
}


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
EXPECTED_GROUPS = {(1, 0): "CEFGHIJKLMNSTUVWXYZ", (1, 1): "ADOPQR", (1, 2): "B"}

# ---------------------------------------------------------------------------
# Printing and plotting
# ---------------------------------------------------------------------------


def fmt(chain: Chain) -> str:
    """Pretty-print a chain: ([(0, 4), (2, 4)], [1, -2]) -> '[0,4] - 2[2,4]'."""
    simplices, coeffs = chain
    if len(simplices) == 0:
        return "0"
    terms = [("" if abs(c) == 1 else str(abs(c))) + "[" + ",".join(map(str, s)) + "]"
             for s, c in zip(simplices, coeffs)]
    out = ("-" if coeffs[0] < 0 else "") + terms[0]
    for t, c in zip(terms[1:], coeffs[1:]):
        out += (" - " if c < 0 else " + ") + t
    return out


def draw(points, complex_, ax=None, r=None, title=None, ms=30, lw=1.2, labels=None, alpha=0.6) -> plt.Axes:
    """Draw a complex (SimplexTree or list of simplices) with vertex i at points[i].
    labels=True writes the vertex numbers; a list of strings writes those instead."""
    simplices = [s for s, _ in complex_.get_simplices()] \
        if hasattr(complex_, "get_simplices") else [list(s) for s in complex_]
    points = np.asarray(points, dtype=float)
    if ax is None:
        _, ax = plt.subplots(figsize=(4, 4))
    if r is not None:
        for p in points:
            ax.add_patch(Circle(p, r, color="#C39BD3", alpha=0.3, lw=0))
    for s in simplices:
        if len(s) == 2:
            ax.plot(*points[s].T, color="black", lw=lw, zorder=2)
        elif len(s) == 3:
            ax.add_patch(Polygon(points[s], color="#7FB3D5", alpha=alpha, zorder=1))
    ax.scatter(*points.T, s=ms, color="black", zorder=3)
    if labels is True:
        labels = [str(i) for i in range(len(points))]
    if labels:
        for p, l in zip(points, labels):
            ax.annotate(l, p, xytext=(7, 5), textcoords="offset points", fontsize=11)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=10)
    return ax


def draw_chain(points, chain: Chain, ax, color="crimson") -> None:
    """Highlight the simplices of a chain on top of a drawing made with `draw`."""
    points = np.asarray(points, dtype=float)
    for s in chain[0]:
        P = points[list(s)]
        if len(s) == 1:
            ax.scatter(*P.T, s=150, color=color, zorder=4)
        elif len(s) == 2:
            ax.plot(*P.T, color=color, lw=4, zorder=3, solid_capstyle="round")
        else:
            ax.add_patch(Polygon(P, color=color, alpha=0.45, zorder=2))


def _setup_3d(ax, points: np.ndarray) -> None:
    """Equal scales on the three axes, a view from above and in front, and no axes."""
    lo, hi = points.min(axis=0), points.max(axis=0)
    ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
    ax.set_box_aspect(hi - lo)
    ax.view_init(elev=40, azim=-75)
    ax.set_axis_off()


def draw_3d(points: np.ndarray, st: gudhi.SimplexTree, ax, title=None) -> None:
    """Draw the triangles of a complex with 3D coordinates on a 3D axes, with their edges."""
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    faces = [points[list(t)] for t in simplices_of_dim(st, 2)]
    ax.add_collection3d(Poly3DCollection(faces, facecolors="#7FB3D5", edgecolors="black", linewidths=0.5,
                                         shade=True, lightsource=LightSource(azdeg=300, altdeg=65)))
    _setup_3d(ax, points)
    ax.set_title(title, fontsize=10)


def plot_shapes(info: dict | None = None, colors: dict | None = None) -> None:
    """One panel per shape of ZOO (shape 5 in 3D), titled with its name. `info` maps a shape's
    name to more lines for its title, and `colors` to the colour of the title."""
    info = info or {}
    colors = colors or {}
    fig = plt.figure(figsize=(3.3 * len(ZOO), 3.8))
    for k, (name, st) in enumerate(ZOO.items()):
        points = ZOO_COORDS[name]
        if points.shape[1] == 3:
            ax = fig.add_subplot(1, len(ZOO), k + 1, projection="3d")
            draw_3d(points, st, ax)
        else:
            ax = fig.add_subplot(1, len(ZOO), k + 1)
            draw(points, st, ax=ax)
            ax.margins(0.15)
            ax.set_axis_off()
        title = ZOO_LABELS.get(name, name) + ("\n" + info[name] if name in info else "")
        ax.set_title(title, fontsize=9, color=colors.get(name, "black"))
    plt.tight_layout(); plt.show()


def plot_double_torus() -> None:
    """A bigger 3D view of shape 5, the triangulated double torus stored in ZOO."""
    st = ZOO["shape 5"]
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(projection="3d")
    draw_3d(ZOO_COORDS["shape 5"], st, ax, title=f"shape 5 (double torus): {len(simplices_of_dim(st, 0))} vertices, "
            f"{len(simplices_of_dim(st, 1))} edges, {len(simplices_of_dim(st, 2))} triangles")
    plt.tight_layout(); plt.show()


def plot_clouds(clouds: dict, ncols=None, fn=None, size=3.0, xlim=None, ylim=None, suptitle=None) -> None:
    """Grid of point clouds. `fn(ax, key, X)` draws one panel (default: a scatter plot)."""
    ncols = ncols or len(clouds)
    nrows = int(np.ceil(len(clouds) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(size * ncols, size * nrows * 1.1), squeeze=False)
    for ax in axes.flat:
        ax.axis("off")
    for ax, (key, X) in zip(axes.flat, clouds.items()):
        if fn is None:
            ax.scatter(*X.T, s=4, color="black")
            ax.set_aspect("equal"); ax.set_title(f"{key} (n={len(X)})", fontsize=9)
        else:
            fn(ax, key, X)
        if xlim: ax.set_xlim(*xlim)
        if ylim: ax.set_ylim(*ylim)
    fig.suptitle(suptitle); plt.tight_layout(); plt.show()


def trace(fn: Callable, calls: list[tuple]) -> None:
    """Print what fn returns (or raises) on each tuple of arguments in `calls`."""
    for args in calls:
        shown = ", ".join(repr(a) if not isinstance(a, gudhi.SimplexTree) else "<SimplexTree>"
                          for a in args)
        try:
            out = repr(fn(*args))
        except Exception as e:
            out = f"raises {type(e).__name__}: {e}"
        print(f"{fn.__name__}({shown})\n    -> {out}")


# ---------------------------------------------------------------------------
# Checkers
# ---------------------------------------------------------------------------


def _as_chain(x) -> Chain:
    """Normalise a returned chain so lists vs tuples don't matter."""
    return [tuple(s) for s in x[0]], [int(c) for c in x[1]]


def run_checks(fn: Callable, cases: list, normalize=lambda x: x) -> None:
    """cases: list of (description, args, expected). `expected` may be an exception
    class, meaning `fn(*args)` must raise it."""
    passed = 0
    for desc, args, expected in cases:
        try:
            got = fn(*args)
        except NotImplementedError:
            print(f"not implemented yet: {fn.__name__}")
            return
        except Exception as e:
            ok = isinstance(expected, type) and isinstance(e, expected)
            got = f"raised {type(e).__name__}: {e}"
        else:
            try:
                ok = not isinstance(expected, type) and normalize(got) == expected
            except Exception:
                ok = False
        passed += ok
        print(f"{'ok  ' if ok else 'FAIL'} {desc}")
        if not ok:
            print(f"       got      {got}")
            print(f"       expected {expected.__name__ if isinstance(expected, type) else expected}")
    print(f"--> {passed}/{len(cases)} passed")


def check_boundary_simplex(fn) -> None:
    run_checks(fn, [
        ("d1 [0,4] = [0] + [4]",            ((0, 4), 1),       ([(0,), (4,)], [1, 1])),
        ("d2 [1,2,4] = [1,2] + [1,4] + [2,4]", ((1, 2, 4), 2),    ([(1, 2), (1, 4), (2, 4)], [1, 1, 1])),
        ("d0 [3] = 0",                      ((3,), 0),         ([], [])),
        ("d3 of a tetrahedron: 4 triangles", ((0, 1, 2, 3), 3),
         ([(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)], [1, 1, 1, 1])),
        ("an edge is not a 2-simplex",       ((0, 1), 2),       ValueError),
    ], normalize=_as_chain)


SLIDE_EXAMPLES = [   # Lecture 3, slide 12, adapted to K: (description, chain, its boundary)
    ("d1([0,4])",                     ([(0, 4)], [1]),                                   ([(0,), (4,)], [1, 1])),
    ("d1([0,4] + [1,4])",             ([(0, 4), (1, 4)], [1, 1]),                        ([(0,), (1,)], [1, 1])),
    ("d1([0,3] + [0,4] + [2,3] + [2,4])", ([(0, 3), (0, 4), (2, 3), (2, 4)], [1, 1, 1, 1]),  ([], [])),
    ("d2([1,2,4])",                   ([(1, 2, 4)], [1]),                                ([(1, 2), (1, 4), (2, 4)], [1, 1, 1])),
]


def check_boundary_chain(fn) -> None:
    run_checks(fn, [(d, (c,), e) for d, c, e in SLIDE_EXAMPLES] +
               [("d0([0] + [1]) = 0", (([(0,), (1,)], [1, 1]),), ([], [])),
                ("the zero chain",    (([], []),),               ([], []))],
               normalize=_as_chain)


def check_equivalence_axioms(S: set, are_related: Callable) -> None:
    """Test reflexivity, symmetry and transitivity on every element, pair and triple of S.
    Prints ok, or FAIL with a counterexample, for each axiom. Slow for big sets (n^3 triples)."""
    S = sorted(S, key=repr)
    counterexamples = {
        "reflexivity":  next((f"not {x!r} ~ {x!r}" for x in S if not are_related(x, x)), None),
        "symmetry":     next((f"{x!r} ~ {y!r}, but not {y!r} ~ {x!r}"
                              for x in S for y in S if are_related(x, y) and not are_related(y, x)), None),
        "transitivity": next((f"{x!r} ~ {y!r} and {y!r} ~ {z!r}, but not {x!r} ~ {z!r}"
                              for x in S for y in S if are_related(x, y)
                              for z in S if are_related(y, z) and not are_related(x, z)), None),
    }
    for axiom, bad in counterexamples.items():
        print(f"ok   {axiom}" if bad is None else f"FAIL {axiom}: {bad}")
    valid = all(bad is None for bad in counterexamples.values())
    print("--> an equivalence relation" if valid else "--> NOT an equivalence relation")


def _as_classes(classes) -> list[set]:
    """Normalise a list of classes so that their order doesn't matter (repeated classes still count)."""
    if not isinstance(classes, list) or not all(isinstance(c, (set, frozenset)) for c in classes):
        raise TypeError("expected a list of sets")
    return sorted((set(c) for c in classes), key=lambda c: sorted(map(repr, c)))


def check_equivalence_classes(fn) -> None:
    hamlet = {"to", "be", "or", "not", "that", "is", "the", "question"}
    cases = [
        ("slide 10: m ~ n when m - n is even",     (set(range(10)), lambda m, n: (m - n) % 2 == 0),
         [{0, 2, 4, 6, 8}, {1, 3, 5, 7, 9}]),
        ("m ~ n when m - n is a multiple of 3",    (set(range(-4, 5)), lambda m, n: (m - n) % 3 == 0),
         [{-3, 0, 3}, {-2, 1, 4}, {-4, -1, 2}]),
        ("equality: every element on its own",     ({"a", "b", "c"}, lambda x, y: x == y),  [{"a"}, {"b"}, {"c"}]),
        ("everything related: a single class",     ({1, 2, 3, 4}, lambda x, y: True),       [{1, 2, 3, 4}]),
        ("words of the same length",               (hamlet, lambda x, y: len(x) == len(y)),
         [{"to", "be", "or", "is"}, {"not", "the"}, {"that"}, {"question"}]),
        ("pairs with the same sum",                ({(0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0)},
                                                    lambda p, q: sum(p) == sum(q)),
         [{(0, 0)}, {(0, 1), (1, 0)}, {(0, 2), (1, 1), (2, 0)}]),
        ("a single element",                       ({42}, lambda x, y: x == y),             [{42}]),
        ("the empty set has no classes",           (set(), lambda x, y: True),              []),
    ]

    def leaves_S_alone(S, are_related):           # fn, but it fails if fn changes S (e.g. with S.pop())
        before = set(S)
        result = fn(S, are_related)
        if S != before:
            raise RuntimeError("S was modified: work on a copy, e.g. set(S)")
        return result
    leaves_S_alone.__name__ = fn.__name__
    run_checks(leaves_S_alone, [(d, args, _as_classes(e)) for d, args, e in cases], normalize=_as_classes)


def _as_entries(result) -> tuple:
    D, rows, cols = result
    D = np.asarray(D)
    return D.shape, {(tuple(rows[i]), tuple(cols[j])) for i, j in zip(*np.nonzero(D % 2))}


def check_boundary_matrix(fn) -> None:
    B1 = {((0,), (0, 3)), ((3,), (0, 3)), ((0,), (0, 4)), ((4,), (0, 4)), ((1,), (1, 2)), ((2,), (1, 2)),
          ((1,), (1, 4)), ((4,), (1, 4)), ((2,), (2, 3)), ((3,), (2, 3)), ((2,), (2, 4)), ((4,), (2, 4))}
    B2 = {((1, 2), (1, 2, 4)), ((1, 4), (1, 2, 4)), ((2, 4), (1, 2, 4))}
    run_checks(fn, [
        ("K, d1 (same as B1)",                        (K, 1),          ((5, 6), B1)),
        ("K, d2 (same as B2)",                        (K, 2),          ((6, 1), B2)),
        ("K, d0 : C0 -> 0 is 0 x 5",                  (K, 0),          ((0, 5), set())),
        ("K, d3 : 0 -> C2 is 1 x 0",                  (K, 3),          ((1, 0), set())),
        ("filled tetrahedron, d3",                    (TET, 3),
         ((4, 1), {(f, (0, 1, 2, 3)) for f in itertools.combinations(range(4), 3)})),
        ("hollow tetrahedron, d3 : 0 -> C2 is 4 x 0", (HOLLOW_TET, 3), ((4, 0), set())),
    ], normalize=_as_entries)


def check_is_cycle(fn) -> None:
    run_checks(fn, [
        ("[0,3] + [0,4] + [2,3] + [2,4], the square",    (([(0, 3), (0, 4), (2, 3), (2, 4)], [1, 1, 1, 1]),), True),
        ("[1,2] + [1,4] + [2,4], the triangle's edges", (([(1, 2), (1, 4), (2, 4)], [1, 1, 1]),),          True),
        ("[0,4] + [1,4] is a path, not a loop",        (([(0, 4), (1, 4)], [1, 1]),),                      False),
        ("[0]: every 0-chain is a cycle",            (([(0,)], [1]),),                                   True),
        ("[1,2,4]: its boundary is not 0",             (([(1, 2, 4)], [1]),),                              False),
        ("the zero chain",                           (([], []),),                                        True),
    ], normalize=bool)


def check_betti(fn) -> None:
    """Your betti_numbers against hand-computed answers and against GUDHI."""
    cases = [(desc, (st,), expected) for desc, st, expected in [
        ("a point",                      complex_from([(0,)]),      [1]),
        ("empty triangle: a circle",     EMPTY_TRIANGLE,            [1, 1]),
        ("filled triangle: a disk",      complex_from([(0, 1, 2)]), [1, 0, 0]),
        ("K (Lecture 7)",                K,                         [1, 1, 0]),
        ("two empty triangles",          complex_from([(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]), [2, 2]),
        ("hollow tetrahedron: a sphere", HOLLOW_TET,                [1, 0, 1]),
        ("filled tetrahedron",           TET,                       [1, 0, 0, 0]),
        ("torus (7 vertices)",           TORUS,                     [1, 2, 1]),
    ]]
    run_checks(fn, cases, normalize=list)
    print()
    run_checks(fn, [(d + " vs GUDHI", args, _gudhi_betti(args[0])) for d, args, _ in cases], normalize=list)


def check_classify(fn, r) -> None:
    run_checks(fn, [(label, (X, r), expected) for label, (X, expected) in SHAPES.items()], normalize=tuple)


def check_group_letters(fn, r) -> None:
    run_checks(fn, [("the alphabet, sorted by homology", (LETTERS, r), EXPECTED_GROUPS)])
