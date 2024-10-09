# Overview

This repository contains supplementary materials for the following conference paper:

Valdemar Švábenský, Jan Vykopal, Martin Horák, Martin Hofbauer, and Pavel Čeleda.\
**From Paper to Platform: Evolution of a Novel Learning Environment for Tabletop Exercises**\
In Proceedings of the 29th Conference on Innovation and Technology in Computer Science Education (ITiCSE 2024).\
https://doi.org/10.1145/3649217.3653639

Preprint: https://arxiv.org/abs/2404.10988

For further information about the INJECT Exercise Platform, please see https://inject.muni.cz

# Contents of the repository

Folder structure (ordered chronologically, not alphabetically):

* `logs-*`: Source data logged from TTXs in the INJECT platform.
	* `logs-2022`: Data from Run 2 reported in the paper.
	* `logs-2023-dry-run`: Data from a test run before Run 3 (not reported in the paper).
	* `logs-2023`: Data from Run 3 reported in the paper.
* `analysis`: A set of Python scripts to analyze the data in `logs-*` folders.
	* See the readme inside the folder for more details.
* `data-*`: Statistical output of the `analysis` scripts.
	* `data-2022`: Output obtained by analyzing `logs-2022`.
	* `data-2023`: Output obtained by analyzing `logs-2023`.
* `plots-*`: Graphical output of the `analysis` scripts.
	* `plots-2022`: Output obtained by analyzing `logs-2022`.
	* `plots-2023`: Output obtained by analyzing `logs-2023`.

# How to cite

If you use or build upon the materials, please use the BibTeX entry below to cite the original paper (not only this web link).

```bibtex
@inproceedings{Svabensky2024from,
    author    = {\v{S}v\'{a}bensk\'{y}, Valdemar and Vykopal, Jan and Hor\'{a}k, Martin and Hofbauer, Martin and \v{C}eleda, Pavel},
    title     = {{From Paper to Platform: Evolution of a Novel Learning Environment for Tabletop Exercises}},
    booktitle = {Proceedings of the 29th Conference on Innovation and Technology in Computer Science Education},
    series    = {ITiCSE '24},
    publisher = {Association for Computing Machinery},
    address   = {New York, NY, USA},
    year      = {2024},
    pages     = {213--219},
    numpages  = {7},
    isbn      = {979-8-4007-0600-4},
    url       = {https://doi.org/10.1145/3649217.3653639},
    doi       = {10.1145/3649217.3653639},
}
```
