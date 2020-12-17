"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Lib_PlotOverlays/RangeDisplay.py

Author: Nils Asmussen <https://github.com/nils-asmussen>
Author: Ryan Hill <https://github.com/RChrHill>
Author: James Richings <https://github.com/JPRichings>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def shade_nofit_area(ax, *args):
    fit = args[0]
    max_transparency = 0.4
    num_fits = len(fit.fit_ranges)
                                                   # t = 1 - (1-alpha)^n, alpha = 1 - (1-t)^(1/n)
    alpha = 1 - (1-max_transparency)**(1/num_fits) # determine transparency per plot that blends to total transparency

    for fit_range in fit.fit_ranges:
        ax.axvspan(0, fit_range[0] , color='black', alpha=alpha)
        ax.axvspan(fit_range[1], fit.T, color='black', alpha=alpha)
    return


def shade_fit_area(ax, *args):
    fit = args[0]
    max_transparency = 0.4
    num_fits = len(fit.fit_ranges)
                                                            # t = 1 - (1-alpha)^n, alpha = 1 - (1-t)^(1/n)
    alpha = 1 - (1 - max_transparency) ** (1 / num_fits)    # determine transparency per plot that blends to total transparency

    for fit_range in fit.fit_ranges:
        ax.axvspan(fit_range[0], fit_range[1], color='black', alpha=alpha)
    return
