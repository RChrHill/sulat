# sulat
`sulat` is a numpy-based, extensible Python data analysis library for Lattice QCD. It covers core analysis procedures including resampling, data manipulation, fitting, and plotting, with support for plugins. It is optimally used in a dual Editor/IPython Console environment, such as [Spyder](https://www.spyder-ide.org/) or [Pycharm](https://www.jetbrains.com/pycharm/), but is still fully-featured in a plain Editor or IPython environment.

## Requirements
- Python >= 3.6
- Numpy >= 1.17
- Matplotlib
- Scipy

## Roadmap
Features to be re-implemented:
- Re-implement latex report output
- Re-implement metadata-driven batch analysis code
- Re-implement autoplots for fitscan results

Additional features to be included:
- Add SETUP.py
- Interactive tutorials
- A proper API for writing plugins against
- Plotting support for data with more than one independent variable
- More rigorous support for storing and fitting data with more than one independent variable
