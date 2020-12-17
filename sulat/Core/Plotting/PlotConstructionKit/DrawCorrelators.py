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


def draw_correlator_as_errorbar(axis, xs, correlator, kwargs, x_combo=None, y_combo=None):
    mk_default(kwargs, 'color', 'black')
    mk_default(kwargs, 'linestyle', 'None')
    mk_default(kwargs, 'marker', 'o')
    mk_default(kwargs, 'markersize', 3)
    mk_default(kwargs, 'elinewidth', .5)
    mk_default(kwargs, 'capsize', 3)
    mk_default(kwargs, 'markerfacecolor', 'none')

    mean_data = correlator.mean
    std_data = correlator.std
    # Now apply the ratio
    if y_combo is not None:
        data_dict = {x: y for x, y in zip(xs, mean_data)}
        subdata_dict = {x: y for x, y in zip(xs, correlator.submean)}

        def data_getter(x):
            return np.array([data_dict[xval] for xval in x % len(xs)])

        def subdata_getter(x):
            return np.array([subdata_dict[xval] for xval in x % len(xs)])

        mean_data = y_combo(data_getter, xs)
        std_data = correlator.stats.std_definition(y_combo(subdata_getter, xs), mean_data)
    if x_combo is not None:
        xs = x_combo(xs)

    # Include provision for x_values being 2D so you can draw a rotated errorbar
    axis.errorbar(xs, mean_data, std_data, **kwargs)


def draw_correlator_as_samples(axis, xs, correlator, kwargs, x_combo=None, y_combo=None):
    mk_default(kwargs, 'color', 'black')
    mk_default(kwargs, 'linestyle', 'None')
    mk_default(kwargs, 'marker', 'o')
    #mk_default(kwargs, 'size', 1)
    mk_default(kwargs, 'alpha', .3)

    sub_data = correlator.submean
    if y_combo is not None:
        subdata_dict = {x: y for x, y in zip(xs, correlator.submean)}

        def subdata_getter(x):
            return np.array([subdata_dict[xval] for xval in x % len(xs)])

        sub_data = y_combo(subdata_getter, xs)
    if x_combo is not None:
        xs = x_combo(xs)

    # Allow samples to be plotted for 2D x values -- might work out-of-box
    axis.scatter(np.outer(xs, np.ones(sub_data.shape[1])), sub_data, **kwargs)
