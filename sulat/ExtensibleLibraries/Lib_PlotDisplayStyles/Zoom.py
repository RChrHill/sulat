"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Lib_PlotDisplayStyles/Zoom.py

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


def zoom(ax, cut_fits, ppts, *args):
    x_data = []
    y_data = []

    for line in ax.lines:
        x_data.append(np.array(line.get_xdata()))
        y_data.append(np.array(line.get_ydata()))

    #for collection in ax.collections:
    #    for path in collection.get_paths():
    #        x_data.append(path.vertices[:, 0])
    #        y_data.append(path.vertices[:, 1])

    if len(args) == 1:
        left_buffer = right_buffer = float(args[0])/100
    elif len(args) > 1:
        left_buffer = float(args[0])/100
        right_buffer = float(args[1])/100
    else:
        left_buffer = right_buffer = .3

    min_fitrange = min([min(xs) for xs in cut_fits])
    max_fitrange = max([max(xs) for xs in cut_fits])
    range_length = max_fitrange-min_fitrange
    min_fitrange -= left_buffer*range_length
    max_fitrange += right_buffer*range_length

    min_y = min(
        min(
            ys[
                np.where(
                    np.logical_and(
                        x_data[i] > min_fitrange,
                        x_data[i] < max_fitrange
                    )
                )
            ]
        ) for i, ys in enumerate(y_data)
    )
    max_y = max(
        max(
            ys[
                np.where(
                    np.logical_and(
                        x_data[i] > min_fitrange,
                        x_data[i] < max_fitrange
                    )
                )
            ]
        ) for i, ys in enumerate(y_data)
    )
    y_range = max_y - min_y

    try:
        ax.set_xlim(min_fitrange, max_fitrange)
        ax.set_ylim(min_y - .1*y_range, max_y + .1*y_range)
    except ValueError:
        print("Axis limits NaN or inf, skipping")

    return


def logzoom(ax, cut_fits, ppts, *args):
    x_data = []
    y_data = []

    for line in ax.lines:
        x_data.append(np.array(line.get_xdata()))
        y_data.append(np.array(line.get_ydata()))

    #for collection in ax.collections:
    #    for path in collection.get_paths():
    #        x_data.append(path.vertices[:, 0])
    #        y_data.append(path.vertices[:, 1])

    if len(args) == 1:
        left_buffer = right_buffer = float(args[0])/100
    elif len(args) > 1:
        left_buffer = float(args[0])/100
        right_buffer = float(args[1])/100
    else:
        left_buffer = right_buffer = .3

    min_fitrange = min([min(xs) for xs in cut_fits])
    max_fitrange = max([max(xs) for xs in cut_fits])
    range_length = max_fitrange-min_fitrange
    min_fitrange -= left_buffer*range_length
    max_fitrange += right_buffer*range_length

    min_y = min(
        min(
            ys[
                np.where(
                    np.logical_and(
                        x_data[i] > min_fitrange,
                        x_data[i] < max_fitrange
                    )
                )
            ]
        ) for i, ys in enumerate(y_data)
    )
    max_y = max(
        max(
            ys[
                np.where(
                    np.logical_and(
                        x_data[i] > min_fitrange,
                        x_data[i] < max_fitrange
                    )
                )
            ]
        ) for i, ys in enumerate(y_data)
    )
    y_range = np.log10(max_y) - np.log10(min_y)

    try:
        ax.set_xlim(min_fitrange, max_fitrange)
        ax.set_ylim(10**(np.log10(min_y) - .1*(y_range)), 10**(np.log10(max_y) + .1*(y_range)))
    except ValueError:
        print("Axis limits NaN or inf, skipping")

    return


def zoom_part(ax, cut_fits, ppts, *args):
    x_data = []
    y_data = []

    if len(args) == 4:
        cut_fits= [[int(args[2]), int(args[3])]]

    for line in ax.lines:
        x_data.append(np.array(line.get_xdata()))
        y_data.append(np.array(line.get_ydata()))

    #for collection in ax.collections:
    #    for path in collection.get_paths():
    #        x_data.append(path.vertices[:, 0])
    #        y_data.append(path.vertices[:, 1])

    if len(args) == 1:
        left_buffer = right_buffer = float(args[0])/100
    elif len(args) > 1:
        left_buffer = float(args[0])/100
        right_buffer = float(args[1])/100
    else:
        left_buffer = right_buffer = .3

    min_fitrange = min([min(xs) for xs in cut_fits])
    max_fitrange = max([max(xs) for xs in cut_fits])
    range_length = max_fitrange-min_fitrange
    min_fitrange -= left_buffer*range_length
    max_fitrange += right_buffer*range_length

    min_y = min(
        min(
            ys[
                np.where(
                    np.logical_and(
                        x_data[i] > min_fitrange,
                        x_data[i] < max_fitrange
                    )
                )
            ]
        ) for i, ys in enumerate(y_data)
    )
    max_y = max(
        max(
            ys[
                np.where(
                    np.logical_and(
                        x_data[i] > min_fitrange,
                        x_data[i] < max_fitrange
                    )
                )
            ]
        ) for i, ys in enumerate(y_data)
    )
    y_range = max_y - min_y

    ax.set_xlim(min_fitrange, max_fitrange)
    try:
        ax.set_ylim(min_y - .1*y_range, max_y + .1*y_range)
    except ValueError:
        print("Skipping set")

    return


def max_zoom(ax, cut_fits, ppts, *args):
    return zoom(ax, cut_fits, ppts, 0)


def cut_to_source(ax, cut_fits, ppts, *args):
    src = int(args[0])

    y_data = []
    for line in ax.lines:
        y_data.append(line.get_ydata()[:src])
    #for collection in ax.collections:
    #    for path in collection.get_paths():
    #        y_data.append(path.vertices[:, 1][:src])

    min_y = min([min(ys) for ys in y_data])
    max_y = max([max(ys) for ys in y_data])
    y_range = max_y - min_y

    try:
        ax.set_ylim(0, max_y + .1*y_range)
    except ValueError:
        print("Attempted to cut to source, ran into NaN or Inf error, ignoring")
    ax.set_xlim(0, src)


def cut_to_source_dyn(ax, cut_fits, ppts, *args):
    src = int(args[0])

    y_data = []
    for line in ax.lines:
        y_data.append(line.get_ydata()[:src])

    min_y = min([min(ys) for ys in y_data])
    max_y = max([max(ys) for ys in y_data])
    y_range = max_y - min_y

    try:
        ax.set_ylim(min_y - .1*y_range, max_y + .1*y_range)
    except ValueError:
        print("Attempted to cut to source, ran into NaN or Inf error, ignoring")
    ax.set_xlim(0, src)


def cut_to_range(ax, cut_fits, ppts, *args):
    lo = int(args[0])
    hi = int(args[1])

    y_data = []
    for line in ax.lines:
        y_data.append(line.get_ydata()[lo:hi+1])
    #for collection in ax.collections:
    #    for path in collection.get_paths():
    #        y_data.append(path.vertices[:, 1][:src])

    min_y = min([min(ys) for ys in y_data])
    max_y = max([max(ys) for ys in y_data])
    y_range = max_y - min_y
    ax.set_ylim(min_y - .1*y_range, max_y + .1*y_range)

    ax.set_xlim(lo, hi)
