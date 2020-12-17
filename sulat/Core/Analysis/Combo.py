"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Analysis/Combo.py

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

import copy
import numpy as np

from .IO import MixInDataIO, Configurations, Correlator
from sulat.ExtensibleLibraries.Lib_Combos import ExLib_Combinations
from sulat.Utilities.ExLibFunction import ExLibFunction
from sulat.Utilities.Path import deep_search, get_by_path, set_by_path
from sulat.Utilities.StaticStrings import host_site


def optional_arg_value(arg, value):
    return value if arg is None else arg


def get_combination_arg(exlib, arg):
    """
    Pass a single string or function as the argument.
    """
    return exlib.lookup(arg)


configurations = 0
timeslices = 1


class MixInCombo(MixInDataIO):
    @ExLibFunction(combination=(ExLib_Combinations, get_combination_arg))
    def combine(self, combination, args=None, kwargs=None):
        """
        Produces a new DataStructure from input DataStructures. The logic in this function determines which type of
        DataStructure is present in the input arguments, and then calls the appropriate combination method for that
        type of DataStructure.

        :param combination: A function, function string-ID, or combination-formatted string.
        :param args: Input arguments to a combination function.
        :param kwargs: Input keyword arguments to a combination function.
        :return: A new DataStructure.
        """
        if isinstance(combination, str):
            nconfigs = 0
            for key in self.configurations:
                if f"{{{key}}}" in combination:
                    nconfigs = 1
                    break
            ncorrs = 0
            for key in self.correlators:
                if f"{{{key}}}" in combination:
                    ncorrs = 1
                    break
        else:
            args = optional_arg_value(args, [])
            kwargs = optional_arg_value(kwargs, {})
            config_arg_keys = findreplaceget_deep_datastructs(args, self.configurations, Configurations)
            config_kwarg_keys = findreplaceget_deep_datastructs(kwargs, self.configurations, Configurations)
            corrs_arg_keys = findreplaceget_deep_datastructs(args, self.correlators, Correlator)
            corrs_kwarg_keys = findreplaceget_deep_datastructs(kwargs, self.correlators, Correlator)

            nconfigs = len(config_arg_keys) + len(config_kwarg_keys)
            ncorrs = len(corrs_arg_keys) + len(corrs_kwarg_keys)

        if nconfigs and not ncorrs:
            return self.combine_configurations(combination, args, kwargs)
        elif ncorrs and not nconfigs:
            return self.combine_correlators(combination, args, kwargs)
        elif nconfigs and ncorrs:
            all_configs = [*[get_by_path(args, keyset) for keyset in config_arg_keys],
                           *[get_by_path(kwargs, keyset) for keyset in config_kwarg_keys]]
            all_corrs = [*[get_by_path(args, keyset) for keyset in corrs_arg_keys],
                         *[get_by_path(kwargs, keyset) for keyset in corrs_kwarg_keys]]
            raise ValueError("Both configurations and correlators detected in input arguments. Only pass configurations OR correlators.\n"
                             f"configurations: {', '.join([obj.__str__() for obj in all_configs])}\n"
                             f"correlators: {', '.join([obj.__str__() for obj in all_corrs])}")
        else:
            raise ValueError("No configurations or correlators detected in the input arguments.")

    @ExLibFunction(combination=(ExLib_Combinations, get_combination_arg))
    def combine_configurations(self, combination, args=None, kwargs=None):
        if type(combination) == str:
            if args is not None or kwargs is not None:
                raise ValueError(f"Combination \'{combination}\' is not a function or the string-ID of a built-in "
                                 f"function. Do not pass arguments or keyword arguments for string-evaluation mode.")
            return self.__parse_configurations_string(combination)
        args = optional_arg_value(args, [])
        kwargs = optional_arg_value(kwargs, {})

        arg_keys = findreplaceget_deep_datastructs(args, self.configurations, Configurations)
        kwarg_keys = findreplaceget_deep_datastructs(kwargs, self.configurations, Configurations)

        # Checks that the data structures all share the same shape, and returns parameters for that shape
        t, T, C = get_tTC(args, arg_keys, kwargs, kwarg_keys, lambda x: x.data)
        autofills = {'t': t, 'T': T, 'C': C}

        findreplace_deep_autofills(args, autofills)
        findreplace_deep_autofills(kwargs, autofills)

        data_args = apply_across_keys(arg_keys, args, lambda x: x.data)
        data_kwargs = apply_across_keys(kwarg_keys, kwargs, lambda x: x.data)
        data = combination(*data_args, **data_kwargs)
        del data_args, data_kwargs

        result = self.build_configurations(data)

        return result

    @ExLibFunction(combination=(ExLib_Combinations, get_combination_arg))
    def combine_correlators(self, combination, args=None, kwargs=None):
        if type(combination) == str:
            if args is not None or kwargs is not None:
                raise ValueError(f"Combination \'{combination}\' is not a function or the string-ID of a built-in "
                                 f"function. Do not pass arguments or keyword arguments for string-evaluation mode.")
            return self.__parse_correlator_string(combination)
        args = optional_arg_value(args, [])
        kwargs = optional_arg_value(kwargs, {})

        arg_keys = findreplaceget_deep_datastructs(args, self.correlators, Correlator)
        kwarg_keys = findreplaceget_deep_datastructs(kwargs, self.correlators, Correlator)

        # Checks that the data structures all share the same shape, and returns parameters for that shape
        t, T, C = get_tTC(args, arg_keys, kwargs, kwarg_keys, lambda x: x.submean)
        autofills = {'t': t, 'T': T, 'C': C}

        findreplace_deep_autofills(args, autofills)
        findreplace_deep_autofills(kwargs, autofills)

        mean_args = apply_across_keys(arg_keys, args, lambda x: np.atleast_2d(x.data_mean))
        mean_kwargs = apply_across_keys(kwarg_keys, kwargs, lambda x: np.atleast_2d(x.data_mean))
        mean = combination(*mean_args, **mean_kwargs)
        del mean_args, mean_kwargs

        submean_args = apply_across_keys(arg_keys, args, lambda x: x.submean)
        submean_kwargs = apply_across_keys(kwarg_keys, kwargs, lambda x: x.submean)
        submean = combination(*submean_args, **submean_kwargs)
        del submean_args, submean_kwargs

        result = self.add_correlator(mean, submean)

        return result

    def __parse_configurations_string(self, combination):
        datastructs = []
        database = self.configurations
        for datastruct in database:
            if f"{{{datastruct}}}" in combination:
                datastructs.append(datastruct)

        Ts = set()
        Cs = set()
        data_string = combination
        for datastruct in datastructs:
            Cs.add(self.configurations[datastruct].data.shape[0])
            Ts.add(self.configurations[datastruct].data.shape[1])
            data_string = data_string.replace(f"{{{datastruct}}}", f"self.configurations[\'{datastruct}\'].data")

        assert len(Ts) == 1, f"Configurations did not have the same number of timeslices: {list(Ts)}"
        assert len(Cs) == 1, f"Configurations did not have the same number of configurations: {list(Cs)}"

        T = list(Ts)[0]
        C = list(Cs)[0]
        t = np.arange(T)

        try:
            data = eval(data_string)
        except Exception as e:
            raise BadCombinationError(f"Error in combination string:\n {data_string}\n"
                                      f"Thrown error: {e}") from e

        return self.build_configurations(data)

    def __parse_correlator_string(self, combination):
        datastructs = []
        database = self.correlators
        Ts = set()
        Cs = set()
        for datastruct in database:
            if f"{{{datastruct}}}" in combination:
                Cs.add(self.correlators[datastruct].submean.shape[0])
                Ts.add(self.correlators[datastruct].submean.shape[1])
                datastructs.append(datastruct)

        assert len(Ts) == 1, f"Configurations did not have the same number of timeslices: {Ts}"
        assert len(Cs) == 1, f"Configurations did not have the same number of configurations: {Cs}"

        T = list(Ts)[0]
        C = list(Cs)[0]
        t = np.arange(T)

        mean_string = combination
        submean_string = combination
        for datastruct in datastructs:
            mean_string = mean_string.replace(f"{{{datastruct}}}", f"self.correlators[\'{datastruct}\'].data_mean")
            submean_string = submean_string.replace(f"{{{datastruct}}}", f"self.correlators[\'{datastruct}\'].submean")

        try:
            mean = eval(mean_string)
        except Exception as e:
            raise BadCombinationError(f"Error in combination string:\n {mean_string}\n"
                                      f"Thrown error: {e}") from e
        try:
            submean = eval(submean_string)
        except Exception as e:
            raise BadCombinationError(f"Error in combination string:\n {mean_string}\n"
                                      f"Thrown error: {e}") from e

        return self.add_correlator(mean, submean)


class BadCombinationError(Exception):
    pass


def assert_data_is_same_shape(params, keys, get_shape_func):
    all_configs = []
    all_timeslices = []
    for keyset in keys:
        data = get_by_path(params, keyset)
        C, T = get_shape_func(data).shape

        all_configs.append(C)
        all_timeslices.append(T)

    if len(all_configs) > 0:
        assert len(set(all_configs)) == 1, f"Not all datastructures have the same number of measurements: {set(all_configs)}"
        assert len(set(all_configs)) == 1, f"Not all datastructures have the same number of timeslices: {set(all_timeslices)}"
    else:
        all_configs = [None]
        all_timeslices = [None]

    return all_configs[0], all_timeslices[0]


def get_tTC(args, arg_keys, kwargs, kwarg_keys, get_shape_func):
    C1, T1 = assert_data_is_same_shape(args, arg_keys, get_shape_func)
    C2, T2 = assert_data_is_same_shape(kwargs, kwarg_keys, get_shape_func)

    if C1 is None and C2 is None:
        raise ValueError("No Data Structures were detected in the input arguments.")
    elif C1 is None:
        C = C2
    elif C2 is None:
        C = C1
    else:
        assert C1 == C2, f"Not all datastructures have the same number of timeslices: [{C1}, {C2}]"
        C = C1
    if T1 is None and T2 is None:
        raise ValueError("No timeslice information present but measurement information is present. "
                         f"This is a critical internal error. Please raise an issue on {host_site}.")
    elif T1 is None:
        T = T2
    elif T2 is None:
        T = T1
    else:
        assert T1 == T2, f"Not all datastructures have the same number of measurements: [{T1}, {T2}]"
        T = T1

    t = np.arange(T)

    return t, T, C


def findreplaceget_deep_datastructs(params, dct, cls):
    """
    Searches an arbitrarily nested collection of lists and dicts "params" to:
    1st: Find which strings in "params" are keys in "dct" bounded by curly braces
    2nd: Replace discovered keys in "params" with the corresponding values in "dct"
    3rd: Get the indices of objects in "params" that are of type "cls"

    :param params: A list or dict, potentially containing further lists and dicts, to be parsed.
    :param dct: The database to search for string-ids of a datastruct in.
    :param cls: The class to check the type of a datastruct against.
    :return: A list of tuple-indices that, when used in "get_by_path", will return objects of type "cls" from "params".
    """
    keys = deep_search(params, lambda x: (x[0] == '{' and x[-1] == '}' and x[1:-1] in dct)
                                         if issubclass(type(x), str) else False)
    for keyset in keys:
        nm = get_by_path(params, keyset)
        set_by_path(params, keyset, dct[nm[1:-1]])
    keys_objs = deep_search(params, lambda x: issubclass(type(x), cls))
    return keys_objs


def findreplace_deep_autofills(params, autofills):
    """
    Searches an arbitrarily nested collection of lists and dicts "params" to:
    1st: Find which strings in "params" are keys in "autofills" bounded by curly braces
    2nd: Replace discovered keys in "params" with the corresponding values in "autofills"

    :param params: A list or dict, potentially containing further lists and dicts, to be parsed.
    :param autofills: The dictionary of parameters that have dynamic values based on the input data structures.
    :return: A list of tuple-indices that, when used in "get_by_path", will return objects of type "cls" from "params".
    """
    keys = deep_search(params, lambda x: (x[0] == '{' and x[-1] == '}' and x[1:-1] in autofills)
                                         if issubclass(type(x), str) else False)
    for keyset in keys:
        nm = get_by_path(params, keyset)
        set_by_path(params, keyset, autofills[nm[1:-1]])


def apply_across_keys(keysets, params, func):
    """
    Gets the values in "params" specified by the sets of keys in "keysets", and replaced those values with the output
    of "func" applied to those values.
    The return value is a deep copy - "params" is not affected by this operation.
    :param keysets: A list of keys to access members of a nested collection.
    :param params: An arbitrarily nested list or dict.
    :param func: A function to be applied to values from "params".
    :return: A modified deep copy of "params".
    """
    param_copy = copy.deepcopy(params)
    for keyset in keysets:
        datastruct = get_by_path(param_copy, keyset)
        set_by_path(param_copy, keyset, func(datastruct))
    return param_copy
