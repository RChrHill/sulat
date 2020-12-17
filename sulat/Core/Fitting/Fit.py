"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Fitting/Fit.py

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

from sulat.Core.Fitting.JointCovariance import joint_weights_matrix, cov2weights
from sulat.ExtensibleLibraries.Lib_Minimisers.Resources import p_value


class FitResult:
    def __init__(self, args, corrs, funcs, mean_results, submean_results, weights, subweights, fit_ranges, constants,
                 resampler, parameter_map, arg_slots, arg_identities):
        mean, goodness_of_fit, residuals = mean_results[0]
        submean, submean_goodness_of_fit, subresiduals = submean_results

        arg_means = {key: arg_mean for key, arg_mean in zip(args, mean)}
        arg_submeans = {key: submean[:, i] for i, key in enumerate(args)}
        arg_cov, _, stds = resampler.covvarstd(mean, submean)
        arg_stds = {key: arg_std for key, arg_std in zip(args, stds)}

        pvalue, chisqdof, Ndof = goodness_of_fit

        subresults = []
        numRead = 0
        for argids, corr, func, fitrange, pmap in zip(arg_identities, corrs, funcs, fit_ranges, parameter_map):
            numAdd = len(fitrange)
            subarg_means = {key: arg_means[key] for key in argids if key not in constants}
            subarg_submeans = {key: arg_submeans[key] for key in argids if key not in constants}
            subarg_stds = {arg_stds[key] for key in args if key not in constants}

            subarg_slots = {list(subarg_means.keys()).index(key): argids.index(key) for key in argids}

            subfit_result = SubFitResult(argids, subarg_means, subarg_submeans, subarg_stds, fitrange, constants, resampler,
                                         corr, func, pmap, subarg_slots,
                                         residuals[numRead:numRead+numAdd],
                                         [sp[numRead:numRead+numAdd] for sp in subresiduals])
            numRead += numAdd
            subresults.append(subfit_result)

        self.mean = arg_means
        self.submean = arg_submeans
        self.std = arg_stds
        self.res_cov = arg_cov
        self.fit_ranges = fit_ranges
        self.constants = constants
        self.weights = weights
        self.subweights = subweights

        self.chi_sq_per_dof = chisqdof
        self.subchi_sq_per_dof = [sbm[1] for sbm in submean_goodness_of_fit]
        self.Ndof = Ndof
        self.pvalue = pvalue
        self.subpvalue = [sbm[0] for sbm in submean_goodness_of_fit]

        self.residuals = residuals
        self.subresiduals = subresiduals

        self.subresults = subresults

    @property
    def attributes(self):
        return list(self.__dict__.keys())


class SubFitResult:
    def __init__(self, args, mean, submean, std, fit_range, constants, resampler, corr, func,
                 parameter_map, arg_slots, residuals, subresiduals):

        Ndof = len(residuals) - len(mean)
        if Ndof > 0:
            chi_sq = np.sum(residuals**2)
            sub_chi_sq = [np.sum(sp**2) for sp in subresiduals]
            pvalue = p_value(Ndof, chi_sq)
            subpvalues = [p_value(Ndof, subchi) for subchi in sub_chi_sq]
            chi_sq_per_dof = chi_sq / Ndof
            subchi_sq_per_dof = [subchi / Ndof for subchi in sub_chi_sq]
        else:
            chi_sq_per_dof, subchi_sq_per_dof, pvalue, subpvalues = None, None, None, None

        arg_cov = resampler.cov_definition(np.array(list(mean.values())),
                                           np.array(list(submean.values())).T)

        self.corr = corr

        self.mean = mean
        self.submean = submean
        self.std = std
        self.res_cov = arg_cov
        self.fit_ranges = fit_range
        self.constants = {key: constants[key] for key in args if key in constants}

        self.chi_sq_per_dof = chi_sq_per_dof
        self.subchi_sq_per_dof = subchi_sq_per_dof
        self.Ndof = Ndof
        self.pvalue = pvalue
        self.subpvalue = subpvalues

        self.residuals = residuals
        self.subresiduals = subresiduals

        self.fit_info = FitFunctionInformation(func, parameter_map, arg_slots)

    @property
    def attributes(self):
        return list(self.__dict__.keys())

    def fit(self, xs, args):
        return self.fit_info.wrapped_func(xs, args, self.fit_info.parameter_map, self.fit_info.fit_arg_slots)

    def fit_central(self, xs):
        return self.fit(xs, np.array(list(self.mean.values())))


class FitFunctionInformation:
    def __init__(self, function, parameter_map, fit_arg_slots):
        self.function = function
        self.parameter_map = parameter_map
        self.fit_arg_slots = fit_arg_slots

    @property
    def wrapped_func(self):
        return prepare_functions_for_fitting([self.function])[0]


def generate_weights(corrs, fit_ranges, correlation, frozen, cov, subcovs, C):
    if cov is None:
        weights, subweights = joint_weights_matrix(corrs, fit_ranges, correlation, frozen)
    elif frozen:
        weights = cov2weights(cov)
        subweights = [weights for _ in range(C)]
    elif subcovs is None:
        raise ValueError("Attempted to do an unfrozen fit with a custom covariance matrix, "
                         "but no subcovs were provided.")
    else:
        weights = cov2weights(cov)
        subweights = [cov2weights(subcov) for subcov in subcovs]

    return weights, subweights


def normalise_fit_ranges(fit_ranges):
    retval = []
    for fit_range in fit_ranges:
        if len(fit_range) == 2:
            retval.append(np.arange(fit_range[0], fit_range[1] + 1))
        else:
            retval.append(np.array(fit_range, dtype=np.int))
    return retval


def fit_func_factory(func):
    def wrapped_func(xs, fit_parameters, prepared_map, fit_parameter_slots):
        for key in fit_parameter_slots:
            slot = fit_parameter_slots[key]
            prepared_map[slot] = fit_parameters[key]
        return func(xs, *prepared_map)
    return wrapped_func


def prepare_functions_for_fitting(funcs):
    wrapped_functions = []
    for i, func in enumerate(funcs):
        wrapped_functions.append(fit_func_factory(func))
    return wrapped_functions


def mk_automatic_constants(correlators_db, args, arg_identities, constants, T, C):
    vec_constants_mean = {}
    vec_constants_sub = {}
    unused_keys = [[key for key in corr_arg_ids if key not in args and key not in constants] for corr_arg_ids in arg_identities]
    unused_keys = set([itm for sublist in unused_keys for itm in sublist])
    if 'T' in unused_keys and 'T' not in constants:
        constants['T'] = T
        unused_keys.discard(T)
    if 'C' in unused_keys and 'C' not in constants:
        constants['C'] = C
        unused_keys.discard(C)
    for item in unused_keys:
        if item[0] == '{':
            key = item[1:-1]
            vec_constants_mean[item] = correlators_db[key].mean
            vec_constants_sub[item] = correlators_db[key].submean

    return constants, vec_constants_mean, vec_constants_sub


def transform_args(fit_functions, arg_names, const_dict, arg_identities, T, C, correlator_db):
    parameter_maps_mean = []
    parameter_maps_bin = []
    fit_parameter_slots = []
    param_idxs = []

    const_dict, vec_constants_mean, vec_constants_bin = mk_automatic_constants(correlator_db, arg_names, arg_identities, const_dict, T, C)

    for config in range(C):
        parameter_maps_bin.append([])
    for i, func in enumerate(fit_functions):
        arg_ids = arg_identities[i]
        parameter_maps_mean.append([None] * len(arg_ids))
        for config in range(C):
            parameter_maps_bin[config].append([None]*len(arg_ids))
        param_map = parameter_maps_mean[i]
        for j, item in enumerate(arg_ids):
            # Get the value from the constant dict if 'item' is a constant name, else get it from the vec constants
            transval = const_dict.get(item, None)
            if transval is None:
                transval = vec_constants_mean.get(item, None)
            param_map[j] = transval
            # Loop over configs to make the binned maps
            for config in range(C):
                # Get the value from the constant dict if 'item' is a constant name, else get it from the vec constants
                transval = const_dict.get(item, None)
                if transval is None:
                    transval = vec_constants_bin.get(item, None)
                    # If it's not a fitting argument, extract the correct config data from the vec constants
                    if transval is not None:
                        transval = transval[config]

                parameter_maps_bin[config][i][j] = transval
        missing_idxs = [j for j, x in enumerate(param_map) if x is None]
        fit_param_names = [arg_ids[j] for j in missing_idxs]
        fit_arg_locations = [arg_names.index(name) for name in fit_param_names]
        param_idxs.append(fit_arg_locations)
        fit_parameter_slots.append({param_idx: arg_idx for param_idx, arg_idx in zip(fit_arg_locations, missing_idxs)})
    return parameter_maps_mean, parameter_maps_bin, fit_parameter_slots, param_idxs


def mk_fit_results(mean_data, bin_data, mean_cov, fit_lambda, bin_cov, configs, initial_conditions, pmap_mn, pmap_bin, verbose=False):
    bin_parameters = [np.zeros((configs, len(initial_conditions)), dtype=np.float), [None]*configs, [None]*configs]
    mean_data = np.concatenate(mean_data)

    central_parameters = np.array([fit_lambda(mean_data, mean_cov, initial_conditions, pmap_mn)])
    if verbose:
        print("Progress...    ", end="")
        mk_progbar(0, configs+1)
    for ii in range(configs):
        if verbose:
            mk_progbar(ii+1, configs+1)
        subbin_data = np.concatenate([subbin[ii] for subbin in bin_data])
        bp = fit_lambda(subbin_data, bin_cov[ii], central_parameters[0][0], pmap_bin[ii])
        bin_parameters[0][ii] = bp[0]
        bin_parameters[1][ii] = bp[1]
        bin_parameters[2][ii] = bp[2]
    if verbose:
        print("\b\b\b", "100%", flush=True)

    return central_parameters, bin_parameters


def mk_progbar(cur, total):
    prog_percent = mk_progval(cur, total)
    if prog_percent != mk_progval(cur-1, total):
        prog_percent = str(prog_percent) + "%"
        print("\b" * (len(prog_percent) + 1), prog_percent, end="", flush=True)


def mk_progval(cur, total):
    return (100*cur) // total