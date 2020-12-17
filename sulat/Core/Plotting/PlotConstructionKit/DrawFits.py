"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Plotting/PlotConstructionKit/DrawFits.py

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
from .CalculateFit import make_fit_ydata


def draw_fit_central(axis, x_data, y_data, kwargs):
    # Plot the best fit line
    mk_default(kwargs, 'linewidth', 0.5)
    mk_default(kwargs, 'color', 'tab:blue')

    axis.plot(x_data, y_data, **kwargs)


def draw_fit_error(axis, x_data, y_data, errors, kwargs):
    mk_default(kwargs, 'linewidth', 0.5)
    mk_default(kwargs, 'color', 'tab:blue')
    mk_default(kwargs, 'alpha', 0.3)

    bot_data = y_data - errors
    top_data = y_data + errors

    axis.fill_between(x_data, bot_data, top_data, **kwargs)


def draw_subfit(axis, x_data, subfit, kwargs, x_ratio, y_ratio):
    centrals, errors = make_fit_ydata(x_data, subfit, y_ratio)

    if x_ratio is not None:
        x_data = x_ratio(x_data)

    draw_fit_central(axis, x_data, centrals, kwargs)
    draw_fit_error(axis, x_data, centrals, errors, kwargs)
