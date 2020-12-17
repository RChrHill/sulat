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

import matplotlib.pyplot as plt
from sulat.Utilities.CommandCatchers import CommandCatcher
from .PlotConstructionKit.DrawCorrelators import draw_correlator_as_errorbar
from .PlotConstructionKit.DrawCorrelators import draw_correlator_as_samples
from .PlotConstructionKit.DrawFits import draw_subfit
import copy

from sulat.ExtensibleLibraries.Lib_PlotDisplayStyles import ExLib_PlotDisplayStyles
from sulat.ExtensibleLibraries.Lib_PlotOverlays import ExLib_PlotOverlays


class PlotClass:
    def __init__(self):
        self._fig = None
        self._ax = None
        self.command_queue = []
        self.is_open = False

        self._fig_catcher = CommandCatcher(self._fig, self.command_queue)
        self._ax_catcher = CommandCatcher(self._ax, self.command_queue)

        self.save_location = None

    @property
    def fig(self):
        return self._fig if self.is_open else self._fig_catcher

    @property
    def ax(self):
        return self._ax if self.is_open else self._ax_catcher

    def open(self):
        if self.is_open:
            self.close()
        self._fig, self._ax = plt.subplots()
        self._fig_catcher.obj_ref = self._fig
        self._ax_catcher.obj_ref = self._ax
        self.redraw()
        self.is_open = True

    def close(self):
        self._fig.clear()
        plt.close(self._fig)
        self._fig = None
        self._ax = None
        self._fig_catcher.obj_ref = None
        self._ax_catcher.obj_ref = None
        self.is_open = False

    def redraw(self):
        self._ax.clear()
        for command in self.command_queue:
            command()

    def save(self, fmt='pdf'):
        if self.save_location is None:
            raise Exception("Save location not set. Plot could not be saved.")
        elif self._fig is None:
            self.open()
            self._fig.savefig('.'.join([self.save_location, fmt]))
            self.close()
        else:
            self._fig.savefig('.'.join([self.save_location, fmt]))

    def add_data(self, x_values, correlator, kwargs=None, x_ratio=None, y_ratio=None):
        if kwargs is None:
            kwargs = {}
        else:
            kwargs = copy.deepcopy(kwargs)
        self.command_queue.append(lambda: draw_correlator_as_errorbar(self._ax, x_values, correlator, kwargs, x_ratio, y_ratio))

    def add_data_samples(self, x_values, correlator, kwargs=None, x_ratio=None, y_ratio=None):
        if kwargs is None:
            kwargs = {}
        else:
            kwargs = copy.deepcopy(kwargs)
        self.command_queue.append(lambda: draw_correlator_as_samples(self._ax, x_values, correlator, kwargs, x_ratio, y_ratio))

    def add_fit(self, x_values, subfit, kwargs=None, x_ratio=None, y_ratio=None):
        if kwargs is None:
            kwargs = {}
        else:
            kwargs = copy.deepcopy(kwargs)
        self.command_queue.append(lambda: draw_subfit(self._ax, x_values, subfit, kwargs, x_ratio, y_ratio))

    def add_display_style(self, style, *args):
        self.command_queue.append(lambda: ExLib_PlotDisplayStyles[style](self._ax, *args))

    def add_overlay(self, style, *args):
        self.command_queue.append(lambda: ExLib_PlotOverlays[style](self._ax, *args))
