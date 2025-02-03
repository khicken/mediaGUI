# mediaGUI
## Data preprocessor intended for SLEAP/DLC
Cross-platform tool (GUI) to concatenate and speed up video(s).

Packaged in Conda, call it in the CLI.

If replicating the repo to build, run:
- `conda env create -f environment.yml`
- `conda activate mediagui`

To update dependencies:
- `conda env export > environment.yml`

To list all the conda environments:
- `conda info --envs`

To remove environment and its dependencies:
- `conda remove -n <envname> --all`