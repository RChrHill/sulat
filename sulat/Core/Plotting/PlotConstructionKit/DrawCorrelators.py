"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Plotting/PlotConstructionKit/DrawCorrelators.py

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

from sulat.Core.Plotting.PlotConstructionKit.Utilities import mk_default
import numpy as np


def draw_correlator_as_errorbar(axis, x_values, correlator, kwargs, x_ratio=None, y_ratio=None):
    mk_default(kwargs, 'color', 'black')
    mk_default(kwargs, 'linestyle', 'None')
    mk_default(kwargs, 'marker', 'o')
    mk_default(kwargs, 'markersize', 3)
    mk_default(kwargs, 'elinewidth', .5)
    mk_default(kwargs, 'capsize', 3)
    mk_default(kwargs, 'markerfacecolor', 'none')

    mean_data = correlator.stats.mean
    std_data = correlator.stats.std
    # Now apply the ratio
    if y_ratio is not None:
        data_dict = {x: y for x, y in zip(x_values, mean_data)}
        subdata_dict = {x: y for x, y in zip(x_values, correlator.stats.sub)}

        def data_getter(x):
            return np.array([data_dict[xval] for xval in x % len(x_values)])

        def subdata_getter(x):
            return np.array([subdata_dict[xval] for xval in x % len(x_values)])

        mean_data = y_ratio(data_getter, x_values)
        std_data = correlator.stats.Std(y_ratio(subdata_getter, x_values), mean_data)
    if x_ratio is not None:
        x_values = x_ratio(x_values)

    # Include provision for x_values being 2D so you can draw a rotated errorbar
    axis.errorbar(x_values, mean_data, std_data, **kwargs)


def draw_correlator_as_samples(axis, x_values, correlator, kwargs, x_ratio=None, y_ratio=None):
    mk_default(kwargs, 'color', 'black')
    mk_default(kwargs, 'linestyle', 'None')
    mk_default(kwargs, 'marker', 'o')
    #mk_default(kwargs, 'size', 1)
    mk_default(kwargs, 'alpha', .3)

    sub_data = correlator.stats.sub
    if y_ratio is not None:
        subdata_dict = {x: y for x, y in zip(x_values, correlator.stats.sub)}

        def subdata_getter(x):
            return np.array([subdata_dict[xval] for xval in x % len(x_values)])

        sub_data = y_ratio(subdata_getter, x_values)
    if x_ratio is not None:
        x_values = x_ratio(x_values)

    # Allow samples to be plotted for 2D x values -- might work out-of-box
    axis.scatter(np.outer(x_values, np.ones(sub_data.shape[1])), sub_data, **kwargs)
