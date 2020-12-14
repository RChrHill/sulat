"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Resources.py

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


import inspect
import os
import pkgutil


class ExtensibleLibrary(dict):
    def __init__(self, file, package, predicates=None):
        functions = get_all_members(file, package, predicates)
        super().__init__(dict(functions))

    def search(self, *criteria):
        return [key for key in self if all(criterion in key for criterion in criteria)]

    def lookup(self, arg):
        return self.get(arg, arg)


def get_all_members(file, package, predicates=None):
    """
    Recursively gather all objects meeting the 'predicates' criteria stemming from the package 'module_head'.
    :param module_head: A module or package to be traversed.
    :param predicates: An iterable of single-argument boolean-valued functions that accept objects.
    :return: A dictionary of {function_name: function_value} pairs.
    """
    functions = {}
    pkg_path = [os.path.dirname(file)]
    for importer, modname, ispkg in pkgutil.iter_modules(pkg_path):
        if modname != "Resources":
            abs_import_path = f"{package}.{modname}"
            submodule = importer.find_module(abs_import_path).load_module(abs_import_path)
            functions.update(get_module_members(submodule, predicates))
            if ispkg:
                functions.update(get_all_members(submodule.__file__, submodule.__package__, predicates))
    return functions


def get_module_members(module, predicates=None):
    """
    Gather all objects meeting the 'predicates' criteria stemming from the package 'module_head'.
    :param module: A module.
    :param predicates: An iterable of single-argument boolean-valued functions that accept objects.
    :return: A dictionary of {function_name: function_value} pairs.
    """
    if predicates is None:
        predicates = (inspect.isfunction, inspect.isclass)

    complete_predicates = (lambda o: any((pred(o) for pred in predicates)),
                           lambda o: o.__module__ == module.__name__ if hasattr(o, '__module__') else False)

    functions = inspect.getmembers(module, lambda o: all((pred(o) for pred in complete_predicates)))

    return functions