"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Utilities/Evaluation.py

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


def lazy_readonly(func):
    internal_attribute = f"__value_of_{func.__name__}"

    @property
    def returned_property(self):
        if not hasattr(self, internal_attribute):
            setattr(self, internal_attribute, func(self))
        return getattr(self, internal_attribute)

    @returned_property.deleter
    def returned_property(self):
        if hasattr(self, internal_attribute):
            delattr(self, internal_attribute)

    return returned_property
