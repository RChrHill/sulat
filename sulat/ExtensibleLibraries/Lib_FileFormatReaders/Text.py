"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Lib_FileFormatReaders/Text.py

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


from itertools import zip_longest
import numpy as np


fulllist_ordering = 'TCV'


def columnar(filepath, ordering):
    """
    Imports space-separated data arranged in three columns. One column must indicate the configuration, one column
    must indicate the timeslice, and the third must indicate the value.
    :param filepath: The path to the file
    :param import_args: For columnar, args should be a string permutation of the letters TCV
    :return: A list of lists, with each inner list looking like [timeslice_number, configuration_number, value]
    """
    full_list = []
    assert len(ordering) == 3, "Pass the data format as \'columnar:args\', where args specifies the order of the " \
                                  "three column identities (e.g. args=CTV - configs, timeslices, values)"
    columns = [char for char in ordering]
    file_columns = {char: columns.index(char) for char in columns}
    with open(filepath, "r") as f:
        for line in f:
            strip = line.strip(" \n").split(" ")
            full_list.append([float(strip[file_columns[char]]) for char in fulllist_ordering])

    data = np.array(full_list)
    shape = np.max(data[:2, :]).astype(np.int) + 1
    return data[:, 2].reshape(shape, order='C')


def block(filepath, ordering):
    """
    Imports space-separated data arranged in two columns and split into ampersand-separated 'blocks'. The columns must
    indicate any two of configurations, timeslices, or value; the block number must indicate the remaining parameter.
    :param filepath: The path to the file
    :param import_args: For block, args should be a string permutation of the letters TCV
    :return: A list of lists, with each inner list looking like [timeslice_number, configuration_number, value]
    """
    full_list = []
    assert len(ordering) == 3, "Pass the data format as \'block:args\', where args specifies the order of the " \
                                  "three column identities (e.g. args=CTV - configs, timeslices, values)"

    columns = [char for char in ordering]
    with open(filepath, "r") as f:

        # First find the length of a block
        block_delimiter = '0'
        comments = ('#', '&')
        found_two_delims = False
        block_len = []
        block_offset = 0
        num_comments = 0
        line_number = 0
        line = f.readline()
        while line:
            if found_two_delims and line[0] in comments:
                num_comments += 1
            if line[0] == block_delimiter:
                block_len.append(line_number)
                if found_two_delims:
                    break
                found_two_delims = True
                block_offset = f.tell() - len(line)
            line_number += 1
            line = f.readline()

        block_len = block_len[1] - block_len[0] - num_comments
        file_columns = {char: columns.index(char) for char in columns}
        f.seek(block_offset)  # Reset the file pointer to the start of the data

        for block_number, block in enumerate(zip_longest(*[f] * (block_len + num_comments))):
            block = block[:block_len]
            for line in block:
                line = (block_number, *line.split())
                full_list.append([float(line[file_columns[char]]) for char in fulllist_ordering])

    data = np.array(full_list)
    shape = np.max(data[:, :2], axis=0).astype(np.int) + 1

    return data[:, 2].reshape(shape, order='C')
