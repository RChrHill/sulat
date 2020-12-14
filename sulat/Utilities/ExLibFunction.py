"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Utilities/ExLibFunction.py

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


import functools
from sulat.ExtensibleLibraries.Resources import ExtensibleLibrary
from sulat.Utilities.StaticStrings import host_site
from sulat.Utilities.Printing import prettyprint_docstring


def ExLibFunction(**ExLibParamDict):
    def ExLibUserFactory(func):
        class ExLibUser:
            __name__ = func.__name__
            __module__ = func.__module__
            __doc__ = func.__doc__

            def __init__(self, init_func):
                self.__func = init_func

                # Assigns each function parameter to the Extensible Library
                CleanedExLibParamDict = {param: ((entry, lambda x: entry.lookup(x)) if isinstance(entry, ExtensibleLibrary) else entry)
                                         for param, entry in ExLibParamDict.items()}
                
                # In addition to setting this up for function 'args', this also checks if the function parameters exist in the signature
                self.__arg_mappings = {}
                for param, ExLibInfo in CleanedExLibParamDict.items():
                    try:
                        self.__arg_mappings[self.__func.__code__.co_varnames.index(param)] = ExLibInfo
                    except ValueError as ve:
                        raise ValueError(f"Bad decoration: \'{param}\' is not an argument. This is a critical internal error. Please raise an issue on {host_site}.") from ve
                self.__kwarg_mappings = CleanedExLibParamDict
                self.context = tuple()

            def __get__(self, instance, owner):
                self.context = (instance,)
                return self

            @functools.wraps(func)
            def __call__(self, *args, **kwargs):
                # Not the most efficient way of doing this, but preserves TypeErrors thrown on _func from bad arg passes
                args = [*self.context, *args]
                for idx, arg in enumerate(args):
                    if idx in self.__arg_mappings:
                        exlib, lookup_func = self.__arg_mappings[idx]
                        args[idx] = lookup_func(exlib, arg)
                for param, kwarg in kwargs.items():
                    if param in self.__kwarg_mappings:
                        exlib, lookup_func = self.__kwarg_mappings[param]
                        kwargs[param] = lookup_func(exlib, kwarg)

                return self.__func(*args, **kwargs)

            @property
            def registered_libraries(self):
                return list(self.__kwarg_mappings.keys())

            def options(self, param, *conditions):
                if param in self.__kwarg_mappings:
                    lib_to_search, mapping_func = self.__kwarg_mappings[param]

                    selected_funcs = [(nm, lib_to_search[nm])
                                      for nm in lib_to_search if all((cond(nm) for cond in conditions))]

                    mapfunc_doc = mapping_func.__doc__
                    if mapfunc_doc is None:
                        print(f"No information provided for the value of \'{param}\'. Please raise an issue on {host_site}.")
                    else:
                        print(prettyprint_docstring(mapfunc_doc))
                    for i, (nm, exlib_func) in enumerate(selected_funcs):
                        exlib_func_args = ', '.join(exlib_func.__code__.co_varnames[:exlib_func.__code__.co_argcount])
                        print(f"{i+1}. {nm}({exlib_func_args})")
                else:
                    print(f"Parameter \'{param}\' of \'{self.__func.__name__}\' does not use ExtensibleLibraries.")

            def get_option_info(self, param, option):
                docstring = self.__kwarg_mappings[param][0][option].__doc__
                if docstring is None:
                    print(f"Extensible Library function \'{option}\' has no docstring.")
                else:
                    print(prettyprint_docstring(docstring))

        return ExLibUser(func)

    return ExLibUserFactory
