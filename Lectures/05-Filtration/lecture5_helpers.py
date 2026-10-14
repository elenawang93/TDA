"""Helpers for the Lecture 5 (simplicial maps and filtrations) notebook: letters for vertices,
example complexes and plotting. Feel free to read it.
"""
import gudhi
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

# ---------------------------------------------------------------------------
# Vertex names: letters in the notebook, integers inside a SimplexTree
# ---------------------------------------------------------------------------


def letter2int(letter: str) -> int:
    """'A' -> 0, 'B' -> 1, 'C' -> 2, ..."""
    return ord(letter) - ord("A")


def int2letter(i: int) -> str:
    """0 -> 'A', 1 -> 'B', 2 -> 'C', ..."""
    return chr(ord("A") + i)


# ---------------------------------------------------------------------------
# Example complexes
# ---------------------------------------------------------------------------


def complex_from(maximal_simplices: list[str]) -> gudhi.SimplexTree:
    """SimplexTree with the given simplices, written as strings of letters like "ACD", and all their faces."""
    st = gudhi.SimplexTree()
    for s in maximal_simplices:
        st.insert([letter2int(v) for v in s])
    return st


# slide 16: K sits inside L
K = complex_from(["ACD", "AE", "BE", "BC"])
K_COORDS = np.array([[0.00, 0.32], [0.71, 0.71], [0.43, 0.21], [0.14, 0.00], [0.31, 0.65]])
L = complex_from(["ACD", "BCE", "AE", "BF", "FG", "CG"])
L_COORDS = np.array([[0.00, 0.32], [0.72, 0.71], [0.44, 0.21], [0.16, 0.00], [0.32, 0.65], [1.00, 0.49], [0.82, 0.06]])

# slides 5, 6, 9 and 13: seven vertices A..G and up to five edges
GRAPH_COORDS = np.array([[0.00, 0.27], [0.11, 0.58], [0.45, 0.65], [0.78, 0.52], [0.64, 0.00], [0.24, 0.07], [1.00, 0.27]])

# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

_PALETTE = plt.get_cmap("tab10").colors


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


def plot_map(K, K_coords, L, L_coords, f: dict[str, str], title=None) -> None:
    """K on the left, each vertex in the colour of its image. L on the right, with the image of
    every simplex of K in red where f sends it, whether or not that simplex is in L. A simplex
    that lands on a single vertex shows as a red ring around that vertex. f maps letters to letters."""
    f = {letter2int(a): letter2int(b) for a, b in f.items()}
    fig, (ax_K, ax_L) = plt.subplots(1, 2, figsize=(8, 3.6))
    draw(K_coords, K, ax=ax_K, labels=True, title="K")
    draw(L_coords, L, ax=ax_L, labels=True, title="L, and the image of K in red", alpha=0.3)
    for v in range(len(K_coords)):
        ax_K.scatter(*K_coords[v], s=120, color=_PALETTE[f[v] % 10], zorder=4)
    for w in range(len(L_coords)):
        ax_L.scatter(*L_coords[w], s=120, color=_PALETTE[w % 10], zorder=4)
    for s, _ in K.get_simplices():
        image = sorted(set(f[v] for v in s))
        if len(image) == 1 and len(s) > 1:
            ax_L.scatter(*L_coords[image[0]], s=420, facecolors="none", edgecolors="crimson", lw=3, zorder=5)
        elif len(image) == 2:
            ax_L.plot(*L_coords[image].T, color="crimson", lw=4, alpha=0.7, zorder=3, solid_capstyle="round")
        elif len(image) == 3:
            ax_L.add_patch(Polygon(L_coords[image], color="crimson", alpha=0.35, zorder=2))
    fig.suptitle(title, fontsize=11)
    plt.tight_layout(); plt.show()


def plot_filtration(st: gudhi.SimplexTree, coords, ncols: int = 6) -> None:
    """One panel per filtration value a_1 < a_2 < ...: the simplices with value <= a_i, i.e. K_i.
    Vertices that are not in K_i yet are grey circles. Simplices in K_i with a face that is not
    in K_i yet are red: they break monotonicity, and K_i is not a complex."""
    values = sorted(set(v for _, v in st.get_simplices()))
    coords = np.asarray(coords, dtype=float)
    ncols = min(ncols, len(values))
    nrows = int(np.ceil(len(values) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(2.7 * ncols, 2.5 * nrows), squeeze=False)
    for ax in axes.flat:
        ax.set_axis_off()
    for i, a in enumerate(values):
        ax = axes.flat[i]
        ax.scatter(*coords.T, s=40, facecolors="none", edgecolors="#BBBBBB", zorder=0)
        for v in range(len(coords)):
            if not st.find([v]) or st.filtration([v]) > a:       # not in K_i yet: grey name
                ax.annotate(int2letter(v), coords[v], xytext=(6, 4), textcoords="offset points", fontsize=11, color="#AAAAAA")
        present = [s for s, v in st.get_simplices() if v <= a]
        draw(coords, present, ax=ax, labels=True)
        for s in present:
            if any(face_value > a for _, face_value in st.get_boundaries(s)):   # a face is missing from K_i
                if len(s) == 2:
                    ax.plot(*coords[s].T, color="crimson", lw=3, zorder=4)
                elif len(s) == 3:
                    ax.add_patch(Polygon(coords[s], color="crimson", alpha=0.5, zorder=2))
        ax.set_title(f"$K_{{{i + 1}}}$: values $\\leq$ {a:.3g}", fontsize=10)
    plt.tight_layout(); plt.show()
