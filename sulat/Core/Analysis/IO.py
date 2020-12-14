"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Analysis/IO.py

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

from .AnalysisBase import AnalysisBase, Configurations, Correlator
from sulat.ExtensibleLibraries.Lib_Combos import ExLib_Combinations
from sulat.ExtensibleLibraries.Lib_FileFormatReaders import ExLib_FileFormatReaders
from sulat.Utilities.ExLibFunction import ExLibFunction
from sulat.Utilities.TypeChecking import is_nonstr_collection


def optional_arg_value(arg, value):
    return value if arg is None else arg


def get_build_configurations_transforms(ExLib, args):
    """
    Pass arguments as either a Collection of single-argument compatible functions and function names, e.g.
    ['fold', 'flip', ...]
    or as a dictionary with arguments given as a list of values, or a dictionary of keyword arguments, e.g.
    {'fold': [1, 0], 'flip': []}
    or
    {'fold': {'cutoff': 1, 'backshift': 0}, 'flip': []}.
    The first parameter of these functions is auto-filled with the input data and cannot be passed values.
    """
    if issubclass(type(args), dict):
        retval = []
        for key, params in args.items():
            param_type = type(params)
            if param_type == tuple or param_type == list:
                retval.append(lambda data: ExLib.lookup(key)(data, *params))
            elif param_type == dict:
                retval.append(lambda data: ExLib.lookup(key)(data, **params))
            else:
                raise ValueError(f"Arguments for parameter {key} was not a tuple, list, or dict: type {param_type} and value {params}.")
        return retval
    elif is_nonstr_collection(args):
        return [ExLib.lookup(arg) for arg in args]
    else:
        raise TypeError(f"Lookup value {args} is neither a dictionary nor a non-string collection.")


class MixInDataIO(AnalysisBase):
    ################################
    # Importers for non-sulat data #
    ################################
    @ExLibFunction(transforms=(ExLib_Combinations, get_build_configurations_transforms))
    def build_configurations(self, data, transforms=None):
        transforms = optional_arg_value(transforms, [])
        data = copy.deepcopy(data)
        for transform in transforms:
            data = transform(data)
        return Configurations(data)

    @ExLibFunction(format=ExLib_FileFormatReaders,
                   transforms=(ExLib_Combinations, get_build_configurations_transforms))
    def import_configurations(self, filepath, format, transforms=None):
        data = self.import_file(filepath, format)
        return self.build_configurations(data, transforms)

    def export_configurations(self):
        raise NotImplementedError

    def configs_to_correlator(self, configurations):
        return Correlator(configurations.mean, self.resampler.resample(configurations.data), self.resampler)

    def add_correlator(self, mean, submean):
        return Correlator(mean, submean, self.resampler)

    @ExLibFunction(transforms=(ExLib_Combinations, get_build_configurations_transforms))
    def build_correlator(self, data, transforms=None):
        transforms = optional_arg_value(transforms, [])
        data = copy.deepcopy(data)
        for transform in transforms:
            data = transform(data)
        configs = Configurations(data)

        return self.configs_to_correlator(configs)

    @ExLibFunction(format=ExLib_FileFormatReaders,
                   transforms=(ExLib_Combinations, get_build_configurations_transforms))
    def import_correlator(self, filepath, format, transforms=None):
        data = self.import_file(filepath, format)
        return self.build_correlator(data, transforms)

    ########################################
    # Importers & exporters for sulat data #
    ########################################

    #####################
    # Utility functions #
    #####################
    def import_file(self, filepath, format):
        return format(filepath)
