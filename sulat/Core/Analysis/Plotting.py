"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Analysis/Plotting.py

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
import numpy as np

from sulat.Core.Analysis.AnalysisBase import AnalysisBase
from sulat.Core.Plotting.PlotClass import PlotClass
from sulat.ExtensibleLibraries.Lib_PlotDisplayStyles import ExLib_PlotDisplayStyles
from sulat.ExtensibleLibraries.Lib_PlotOverlays import ExLib_PlotOverlays
from sulat.ExtensibleLibraries.Lib_PlotCombos import ExLib_PlotCombos
from sulat.Utilities.ExLibFunction import ExLibFunction


def get_combo(exlib, arg):
    """
    Pass a single string or function as the argument.
    """
    return exlib.lookup(arg)


def get_plotmodules(exlib, args):
    """
    Pass a list of functions and function names.
    """
    return [exlib.lookup(arg) for arg in args]


def extend_kwargs(list_of_kwargs, new_kwargs, parameter_name=None):
    if isinstance(new_kwargs, dict):
        for i, kwarg_dict in enumerate(list_of_kwargs):
            list_of_kwargs[i] = {**kwarg_dict, **new_kwargs}
    elif isinstance(new_kwargs, list):
        for (i, kwarg_dict), new_subkwargs in zip(enumerate(list_of_kwargs), new_kwargs):
            assert isinstance(new_subkwargs, dict), f"{'list kwarg arguments' if parameter_name is None else parameter_name} must be a list of dicts and/or None."
            if new_subkwargs is not None:
                list_of_kwargs[i] = {**kwarg_dict, **new_subkwargs}
    elif new_kwargs is None:
        return
    else:
        assert False, f"{'Kwargs parameter' if parameter_name is None else parameter_name} must be a dictionary, list, or None."


def make_local_kwargs(kwargs, data_kwargs, fit_kwargs, correlators, subfits):
    local_data_kwargs = [{} for _ in correlators]
    local_fit_kwargs = [{} for _ in subfits]

    extend_kwargs(local_data_kwargs, kwargs, "kwargs")
    extend_kwargs(local_data_kwargs, data_kwargs, "data_kwargs")
    extend_kwargs(local_fit_kwargs, kwargs, "kwargs")
    extend_kwargs(local_fit_kwargs, fit_kwargs, "fit_kwargs")

    local_data_kwargs = [None if len(subkwargs) == 0 else subkwargs for subkwargs in local_data_kwargs]
    local_fit_kwargs = [None if len(subkwargs) == 0 else subkwargs for subkwargs in local_fit_kwargs]

    return local_data_kwargs, local_fit_kwargs


class MixInPlotting(AnalysisBase):
    def new_plot(self):
        return PlotClass()

    @ExLibFunction(x_combo=(ExLib_PlotCombos, get_combo),
                   y_combo=(ExLib_PlotCombos, get_combo),
                   display_styles=(ExLib_PlotDisplayStyles, get_plotmodules),
                   overlays=(ExLib_PlotOverlays, get_plotmodules))
    def autoplot_fit(self, fit, x_values=None, fit_x_limits=None, kwargs=None, data_kwargs=None, fit_kwargs=None,
                     x_combo=None, y_combo=None,
                     display_styles=None, overlays=None):
        return self.autoplot_fits([fit], x_values, fit_x_limits, kwargs, data_kwargs, fit_kwargs, x_combo, y_combo,
                                  display_styles, overlays)

    @ExLibFunction(x_combo=(ExLib_PlotCombos, get_combo),
                   y_combo=(ExLib_PlotCombos, get_combo),
                   display_styles=(ExLib_PlotDisplayStyles, get_plotmodules),
                   overlays=(ExLib_PlotOverlays, get_plotmodules))
    def autoplot_fits(self, fits, x_values=None, fit_x_limits=None, kwargs=None, data_kwargs=None, fit_kwargs=None,
                      x_combo=None, y_combo=None,
                      display_styles=None, overlays=None):
        corrs = []
        subfits = []
        for fit in fits:
            sub_fits = fit.subresults
            corrs.extend([sub_fit.corr for sub_fit in sub_fits])
            subfits.extend(sub_fits)
        return self.autoplot_corrs_subfits(corrs, subfits, x_values, fit_x_limits,
                                           kwargs, data_kwargs, fit_kwargs, x_combo, y_combo, display_styles, overlays)

    @ExLibFunction(x_combo=(ExLib_PlotCombos, get_combo),
                   y_combo=(ExLib_PlotCombos, get_combo),
                   display_styles=(ExLib_PlotDisplayStyles, get_plotmodules),
                   overlays=(ExLib_PlotOverlays, get_plotmodules))
    def autoplot_corrs(self, corrs, xs=None, fit_x_limits=None, kwargs=None, data_kwargs=None, fit_kwargs=None,
                       x_combo=None, y_combo=None, display_styles=None, overlays=None):
        return self.autoplot_corrs_subfits(self, corrs, [], xs, fit_x_limits, kwargs, data_kwargs, fit_kwargs,
                                           x_combo, y_combo, display_styles, overlays)

    @ExLibFunction(x_combo=(ExLib_PlotCombos, get_combo),
                   y_combo=(ExLib_PlotCombos, get_combo),
                   display_styles=(ExLib_PlotDisplayStyles, get_plotmodules),
                   overlays=(ExLib_PlotOverlays, get_plotmodules))
    def autoplot_subfits(self, subfits, xs=None, fit_x_limits=None, kwargs=None, data_kwargs=None, fit_kwargs=None,
                       x_combo=None, y_combo=None, display_styles=None, overlays=None):
        return self.autoplot_corrs_subfits(self, [], subfits, xs, fit_x_limits, kwargs, data_kwargs, fit_kwargs,
                                           x_combo, y_combo, display_styles, overlays)

    @ExLibFunction(x_combo=(ExLib_PlotCombos, get_combo),
                   y_combo=(ExLib_PlotCombos, get_combo),
                   display_styles=(ExLib_PlotDisplayStyles, get_plotmodules),
                   overlays=(ExLib_PlotOverlays, get_plotmodules))
    def autoplot_corrs_subfits(self, corrs, subfits, xs=None, fit_x_limits=None,
                               kwargs=None, data_kwargs=None, fit_kwargs=None, x_combo=None, y_combo=None,
                               display_styles=None, overlays=None):
        if fit_x_limits is None:
            fit_x_limits = [None]*len(corrs)
        assert callable(y_combo) or x_combo is None, f"y ratio '{y_combo}' is not callable --- " \
                                                          f"input '{y_combo }' not found in ExLib_PlotRatios and is " \
                                                          f"not callable."
        assert callable(x_combo) or x_combo is None, f"x ratio '{x_combo}' is not callable --- " \
                                                          f"input '{y_combo }' not found in ExLib_PlotRatios and is " \
                                                          f"not callable."

        local_data_kwargs, local_fit_kwargs = make_local_kwargs(kwargs, data_kwargs, fit_kwargs, corrs, subfits)

        plotobj = self.new_plot()
        for correlator, data_subkwargs in zip(corrs, local_data_kwargs):
            if xs is None:
                corr_x_values = np.arange(correlator.T)
            else:
                corr_x_values = xs
            plotobj.add_data(corr_x_values, correlator, data_subkwargs, x_combo, y_combo)
        for fit, fit_subkwargs, subfit_x_limits in zip(subfits, local_fit_kwargs, fit_x_limits):
            if subfit_x_limits is None:
                if xs is None:
                    T = corrs[0].submean.shape[1]
                    fit_x_values = np.linspace(0, T, 10*T)
                else:
                    fit_x_values = np.linspace(xs[0], xs[-1], 10 * len(xs))
            else:
                if subfit_x_limits == 'auto':
                    subfit_x_limits = fit.fit_ranges
                fit_x_values = np.linspace(subfit_x_limits[0], subfit_x_limits[-1], 1000)
            plotobj.add_fit(fit_x_values, fit, fit_subkwargs, x_combo, y_combo)

        if display_styles is not None:
            for inp in display_styles:
                inp_split = inp.split(SS.delim_args)
                if len(inp_split) == 1:
                    style_name = inp_split[0]
                    args = ''
                else:
                    style_name, args = inp_split
                plotobj.add_display_style(style_name, fit_x_limits, 1, *args.split(SS.delim_argsep))
        if overlays is not None:
            for inp in overlays:
                inp_split = inp.split(SS.delim_args)
                if len(inp_split) == 1:
                    overlay_name = inp_split[0]
                    args = ''
                else:
                    overlay_name, args = inp_split
                plotobj.add_overlay(overlay_name, *args.split(SS.delim_argsep))

        return plotobj