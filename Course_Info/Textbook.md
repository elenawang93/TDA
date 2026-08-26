# Textbook

## Main textbook

- Tamal K. Dey and Yusu Wang, *Computational Topology for Data Analysis*, Cambridge University Press, 2022. The authors' pre-publication version is [free to download](https://www.cs.purdue.edu/homes/tamaldey/book/CTDAbook/CTDAbook.pdf). Readings marked **DW** on the [schedule](Schedule.md) refer to this book.

## Second reference

- Herbert Edelsbrunner and John Harer, *Computational Topology: An Introduction*, American Mathematical Society, 2010. Marked **EH** on the schedule. We use it for matrix reduction (IV.2), persistent homology (VII.1), and stability (VIII.2). Available [here](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/edelcomp.pdf).

## Background and further reading

Both free online. Dip into them when a definition in class goes by too fast.
 
- Allen Hatcher, *Algebraic Topology*, Cambridge University Press, 2002. [Free online](https://pi.math.cornell.edu/~hatcher/AT/ATpage.html). The full story behind homology.
- Robert Ghrist, *Elementary Applied Topology*, 2014. [Free online](https://www2.math.upenn.edu/~ghrist/notes.html). A short, picture-heavy tour of applied topology.

## Papers on the schedule

Listed by the lecture in which they appear. Everything here is either open access or on arXiv.

**Lecture 8 — stability and persistence modules**

- David Cohen-Steiner, Herbert Edelsbrunner, and John Harer. Stability of persistence diagrams. *Discrete & Computational Geometry* 37 (2007), 103–120. [doi:10.1007/s00454-006-1276-5](https://doi.org/10.1007/s00454-006-1276-5)
- David Cohen-Steiner, Herbert Edelsbrunner, and Dmitriy Morozov. Vines and vineyards by updating persistence in linear time. *SoCG 2006*. [pdf](https://www.mrzv.org/publications/vineyards/socg06/)

**Lecture 10 — Reeb graphs**

- Brian Bollen, Erin Chambers, Joshua A. Levine, and Elizabeth Munch. Reeb graph metrics from the ground up. [arXiv:2110.05631](https://arxiv.org/abs/2110.05631) (2021). A survey of the distances covered in class.

**Lecture 11 — Mapper**

- Gurjeet Singh, Facundo Mémoli, and Gunnar Carlsson. Topological methods for the analysis of high dimensional data sets and 3D object recognition. *Eurographics Symposium on Point-Based Graphics* (2007). [doi:10.2312/SPBG/SPBG07/091-100](https://doi.org/10.2312/SPBG/SPBG07/091-100) The original Mapper paper.
- Mathieu Carrière, Bertrand Michel, and Steve Oudot. Statistical analysis and parameter selection for Mapper. *Journal of Machine Learning Research* 19(12) (2018), 1–39. [pdf](http://jmlr.org/papers/v19/17-291.html)

**Lecture 12 — directional transforms**

- Elizabeth Munch. An invitation to the Euler characteristic transform. *The American Mathematical Monthly* (2025). [doi:10.1080/00029890.2024.2409616](https://doi.org/10.1080/00029890.2024.2409616), [arXiv:2310.10395](https://arxiv.org/abs/2310.10395). Start here.
- Katharine Turner, Sayan Mukherjee, and Doug M. Boyer. Persistent homology transform for modeling shapes and surfaces. *Information and Inference* 3(4) (2014), 310–344. [doi:10.1093/imaiai/iau011](https://doi.org/10.1093/imaiai/iau011)
- Justin Curry, Sayan Mukherjee, and Katharine Turner. How many directions determine a shape and other sufficiency results for two topological transforms. *Transactions of the AMS, Series B* 9 (2022), 1006–1043. [doi:10.1090/btran/122](https://doi.org/10.1090/btran/122)
- Abigail Hickok. Persistence diagram bundles: a multidimensional generalization of vineyards. [arXiv:2210.05124](https://arxiv.org/abs/2210.05124) (2022).
- Shreya Arya, Barbara Giunti, Abigail Hickok, Lida Kanari, Sarah McGuire, and Katharine Turner. Decomposing the persistent homology transform of star-shaped objects. [arXiv:2408.14995](https://arxiv.org/abs/2408.14995) (2024). Monodromy in the PHT.
- Jessi Cisewski-Kehe, Brittany Terese Fasy, Alexander McCleary, and Eli Quist. Tensor computation of Euler characteristic functions and transforms. *SoCG 2026*. [arXiv:2511.03909](https://arxiv.org/abs/2511.03909). Computing the ECT on a GPU; code in [pyECT](https://github.com/compTAG/pyECT).

**Lecture 13 — discrete Morse theory and multiparameter persistence**

- Robin Forman. A user's guide to discrete Morse theory. *Séminaire Lotharingien de Combinatoire* 48 (2002), B48c.
- Magnus Bakke Botnan and Michael Lesnick. An introduction to multiparameter persistence. [arXiv:2203.14289](https://arxiv.org/abs/2203.14289) (2022).
- Chad M. Topaz, Lori Ziegelmeier, and Tom Halverson. Topological data analysis of biological aggregation models. *PLoS ONE* 10(5) (2015), e0126383. [doi:10.1371/journal.pone.0126383](https://doi.org/10.1371/journal.pone.0126383) Introduces CROCKER plots.
- [RIVET](https://rivet.readthedocs.io), software for visualizing 2-parameter persistence.

## Classic papers and surveys

Good starting points for the final project, and for the history of the field.

- Herbert Edelsbrunner, David Letscher, and Afra Zomorodian. Topological persistence and simplification. *Discrete & Computational Geometry* 28 (2002), 511–533. [doi:10.1007/s00454-002-2885-2](https://doi.org/10.1007/s00454-002-2885-2) Where persistence starts.
- Afra Zomorodian and Gunnar Carlsson. Computing persistent homology. *Discrete & Computational Geometry* 33 (2005), 249–274. [doi:10.1007/s00454-004-1146-y](https://doi.org/10.1007/s00454-004-1146-y)
- Robert Ghrist. Barcodes: the persistent topology of data. *Bulletin of the AMS* 45(1) (2008), 61–75. [doi:10.1090/S0273-0979-07-01191-3](https://doi.org/10.1090/S0273-0979-07-01191-3)
- Gunnar Carlsson. Topology and data. *Bulletin of the AMS* 46(2) (2009), 255–308. [doi:10.1090/S0273-0979-09-01249-X](https://doi.org/10.1090/S0273-0979-09-01249-X)
- Frédéric Chazal and Bertrand Michel. An introduction to topological data analysis: fundamental and practical aspects for data scientists. *Frontiers in Artificial Intelligence* 4 (2021). [arXiv:1710.04019](https://arxiv.org/abs/1710.04019)
- Nina Otter, Mason A. Porter, Ulrike Tillmann, Peter Grindrod, and Heather A. Harrington. A roadmap for the computation of persistent homology. *EPJ Data Science* 6, 17 (2017). [arXiv:1506.08903](https://arxiv.org/abs/1506.08903) Compares the software below.
- Ulrich Bauer. Ripser: efficient computation of Vietoris–Rips persistence barcodes. *Journal of Applied and Computational Topology* 5 (2021), 391–423. [doi:10.1007/s41468-021-00071-5](https://doi.org/10.1007/s41468-021-00071-5)
- Peter Bubenik. Statistical topological data analysis using persistence landscapes. *Journal of Machine Learning Research* 16 (2015), 77–102. [pdf](http://jmlr.org/papers/v16/bubenik15a.html)
- Henry Adams et al. Persistence images: a stable vector representation of persistent homology. *Journal of Machine Learning Research* 18(8) (2017), 1–35. [pdf](http://jmlr.org/papers/v18/16-337.html)
- Felix Hensel, Michael Moor, and Bastian Rieck. A survey of topological machine learning methods. *Frontiers in Artificial Intelligence* 4 (2021). [doi:10.3389/frai.2021.681108](https://doi.org/10.3389/frai.2021.681108)

A longer list of suggested project papers, sorted by topic, will be posted on 10/7.

## Software

All of the in-class notebooks use Python. Install `numpy`, `matplotlib`, and `jupyter`, then add the TDA libraries as we reach them.

- [GUDHI](https://gudhi.inria.fr/) — the most complete library: simplicial complexes, persistence, alpha complexes, Mapper, vectorizations. The [representations tutorial](https://github.com/GUDHI/TDA-tutorial/blob/master/Tuto-GUDHI-representations.ipynb) accompanies Lecture 9.
- [Ripser](https://github.com/Ripser/ripser) — fastest Vietoris–Rips persistence; use it from Python through `ripser.py` in [scikit-tda](https://docs.scikit-tda.org/en/latest/), which also bundles `persim` (diagram distances and images) and `kepler-mapper`.
- [giotto-tda](https://github.com/giotto-ai/giotto-tda) — TDA as scikit-learn transformers, convenient for ML pipelines.
- [teaspoon](https://teaspoontda.github.io/teaspoon/) — time series and signal processing with TDA.
- [Topology ToolKit (TTK)](https://topology-tool-kit.github.io/) — Reeb graphs, merge trees, and Morse–Smale complexes for scientific visualization (ParaView plugin, Python bindings).
- [Mapper Interactive](https://mapperinteractive.github.io/) — Mapper in the browser.
- [RIVET](https://rivet.readthedocs.io) — 2-parameter persistence.
- [pyECT](https://github.com/compTAG/pyECT) — Euler characteristic transforms on the GPU.

## More resources

- [DONUT](https://donut.topology.rocks/) — a searchable database of applications of TDA; browse it when looking for a project topic.
- [AATRN](https://www.youtube.com/@aatrn1/playlists) — recorded talks from the Applied Algebraic Topology Research Network.