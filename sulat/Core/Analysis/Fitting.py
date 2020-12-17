"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Analysis/Fitting.py

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

import itertools
import numpy as np

from .IO import MixInDataIO
from sulat.Core.Fitting.Fit import FitResult, generate_weights, normalise_fit_ranges, mk_fit_results
from sulat.Core.Fitting.Fit import prepare_functions_for_fitting, transform_args
from sulat.ExtensibleLibraries.Lib_FitFuncs import ExLib_FitFuncs
from sulat.ExtensibleLibraries.Lib_Minimisers import ExLib_Minimisers
from sulat.Utilities.ExLibFunction import ExLibFunction


def optional_arg_value(arg, value):
    return value if arg is None else arg


def get_fitfuncs(exlib, args):
    """
    Pass a list of functions and function names.
    """
    return [exlib.lookup(arg) for arg in args]


def get_minimiser(exlib, arg):
    """
    Pass a single string or function as the argument.
    """
    return exlib.lookup(arg)


class MixInFitting(MixInDataIO):
    @ExLibFunction(funcs=(ExLib_FitFuncs, get_fitfuncs),
                   fit_method=(ExLib_Minimisers, get_minimiser))
    def fit(self, corrs, funcs, fit_ranges, args, arg_identities, correlation, frozen=True, cov=None, subcovs=None,
            constants=None, fit_method=ExLib_Minimisers['LevenburgMarquardtScipy'], xs=None):
        constants = optional_arg_value(constants, {})
        assert len(corrs) == len(fit_ranges), f"Mismatch between the number of correlators ({(len(corrs))}) " \
                                              f"and the number of fit ranges ({len(fit_ranges)}): " \
                                              f"{corrs}, {fit_ranges}."
        assert len(corrs) == len(funcs), f"Mismatch between the number of correlators ({(len(corrs))}) " \
                                         f"and the number of fit functions ({len(funcs)}): " \
                                         f"{corrs}, {funcs}."

        fit_ranges = normalise_fit_ranges(fit_ranges)
        mean_data = [corr.mean[fit_range] for corr, fit_range in zip(corrs, fit_ranges)]
        submean_data = [corr.submean[:, fit_range] for corr, fit_range in zip(corrs, fit_ranges)]
        C, T = corrs[0].submean.shape
        weights, subweights = generate_weights(corrs, fit_ranges, correlation, frozen, cov, subcovs, C)

        wrapped_functions = prepare_functions_for_fitting(funcs)
        parameter_maps_mean, parameter_maps_bin, arg_location_maps, arg_idxs = transform_args(funcs, list(args.keys()),
                                                                                              constants, arg_identities, T,
                                                                                              C, self.correlators)

        xs = optional_arg_value(xs, [np.arange(T)[fr] for fr in fit_ranges])

        def fit_wrapper(fit_vector, weights, initial_conditions, parameter_map):
            return fit_method(fit_vector, initial_conditions, weights, wrapped_functions, xs, parameter_map,
                              arg_location_maps)

        central_parameters, bin_parameters = mk_fit_results(mean_data, submean_data, weights,
                                                            fit_wrapper, subweights,
                                                            C, np.array(list(args.values())),
                                                            parameter_maps_mean, parameter_maps_bin)

        return FitResult(args, corrs, funcs, central_parameters, bin_parameters, weights, subweights, fit_ranges, constants,
                         corrs[0].resampler, parameter_maps_mean, arg_location_maps, arg_identities)

    @ExLibFunction(funcs=(ExLib_FitFuncs, get_fitfuncs),
                   fit_method=(ExLib_Minimisers, get_minimiser))
    def fit_scan(self, corrs, funcs, fit_ranges, args, arg_identities, correlation, frozen=None, thinned=1, cov=None, subcovs=None,
                 constants=None, fit_method=ExLib_Minimisers['LevenburgMarquardtScipy'], xs=None,
                 min_fit=None, scan=None, max_low=None):
        scan = optional_arg_value(scan, [True] * len(fit_ranges))
        max_low = optional_arg_value(max_low, [None] * len(fit_ranges))
        min_fit = optional_arg_value(min_fit, [None] * len(fit_ranges))

        if not isinstance(min_fit, list):
            assert isinstance(min_fit, int), "min_fit must be an int or a list of ints."
            min_fit = [min_fit]*len(fit_ranges)
        else:
            assert len(fit_ranges) == len(min_fit), "A minimum fit value must be provided for each correlator."
        if not isinstance(max_low, list):
            assert isinstance(max_low, int), "min_fit must be an int or a list of ints."
            min_fit = [max_low]*len(fit_ranges)
        else:
            assert len(fit_ranges) == len(max_low), "A minimum fit value must be provided for each correlator."

        all_fit_ranges = []
        # Produce every combination of fit ranges...
        for fit_range, mfit, submax_low, doScan in zip(fit_ranges, min_fit, max_low, scan):
            if mfit == 1 or mfit is None or not doScan:
                all_fit_ranges.append([fit_range])
            else:
                lo, hi = fit_range
                if submax_low is None:
                    submax_low = hi
                all_fit_ranges.append([[il, ih] for il in range(lo, submax_low+1) for ih in range(il + mfit - 1, hi+1, thinned)])

        total_fits = np.prod([len(sublist) for sublist in all_fit_ranges])
        all_fit_ranges = itertools.product(*all_fit_ranges)
        fit_results = {}
        fit_num = 0
        fails = []
        for fit_range_combo in all_fit_ranges:
            fit_num += 1
            print(f"\rFitting {fit_num}/{total_fits}", end='')
            try:
                result = self.fit(corrs, funcs, fit_range_combo, args, arg_identities, correlation, frozen, cov, subcovs,
                                  constants, fit_method, xs)
                key = ', '.join([str(elem) for elem in fit_range_combo])
                fit_results[key] = result
            except np.linalg.LinAlgError as lae:
                fails.append(f"Fit range {fit_range_combo} failed: {lae}")
            if len(fails):
                print(f"{len(fails)} fits failed with the following exceptions:")
        return fit_results
