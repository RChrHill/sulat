"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Utilities/Path.py

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


from functools import reduce

from .TypeChecking import is_nonstr_collection
import operator


#########################
# DEEP ACCESS FUNCTIONS #
#########################
def get_by_path(root, items):
    """
    Access a nested object in root by item sequence.
    Credit: Martijn Pieters
    Source: https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys
    """
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    """
    Set a value in a nested object in root by item sequence.
    Credit: Martijn Pieters
    Source: https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys
    """
    get_by_path(root, items[:-1])[items[-1]] = value


def dict_list_agnostic_items(searchable):
    return searchable if isinstance(searchable, dict) else range(len(searchable))


def deep_search(searchable, condition):
    keys = []
    if is_nonstr_collection(searchable):
        for idx in dict_list_agnostic_items(searchable):
            subsearchable = searchable[idx]
            # Check if it meets the criteria. If so, terminate this iteration here and continue to the next.
            if condition(subsearchable):
                keys.append([idx])
                continue
            # Else, if we're not at the bottom of a nest yet, figure out which items further down in the hierarchy meet
            # the criteria.
            if is_nonstr_collection(subsearchable):
                subkeys = deep_search(subsearchable, condition)
                subkeys = [[idx] + item for item in subkeys]
                keys.extend(subkeys)
    return keys
