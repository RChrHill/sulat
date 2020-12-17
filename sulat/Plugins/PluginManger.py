"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Plugins/PluginManager.py

Author: Ryan Hill <https://github.com/RChrHill>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy ofAnalysisPlotting the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pkgutil
import os
from shutil import copy2
import sulat.Plugins.Plugins as PLG


def __return_root_dir():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).split("/")
    ROOT_DIR.append("Plugins")
    ROOT_DIR = "/".join(ROOT_DIR)

    return ROOT_DIR


__load_order_file = __return_root_dir() + "/Load_Order.txt"


def install_plugin(file):
    copy2(file, __return_root_dir())
    return


def uninstall_plugin(file):
    os.remove(__return_root_dir()+"/"+file)
    return


def modify_load_order():
    if not os.path.isfile(__load_order_file):
        with open(__load_order_file, 'w') as writer:
            for importer, modname, ispkg in pkgutil.iter_modules(PLG.__path__):
                writer.write(modname)
    with open(__load_order_file, 'r') as reader:
        load_order = reader.read().split("\n")

    print("Current Load Order:")
    for i, item in enumerate(load_order):
        print("<"+str(i)+">", item)
    print("Enter new load order:")

    print("Template:")
    print(" ".join(range(len(load_order))))

    new_load_order = input().split(' ')
    new_load_order = [int(idx) for idx in new_load_order]

    # Assert that new load order is valid
    # <Check that each entry in new load order is unique>
    assert len(new_load_order) == len(load_order)

    new_load_order = [load_order[idx] for idx in new_load_order]

    with open(__load_order_file, 'w') as writer:
        for item in new_load_order:
            writer.write(item)

    return


# Smush several plugins into a single file to keep load orders lightweight
def consolidate_plugins():
    return


# Turn consolidated plugin back into individual bits
def split_plugin():
    return


def _load_plugins():
    package = PLG

    if not os.path.isfile(__load_order_file):
        with open(__load_order_file, 'w') as writer:
            writer.write('')
    with open(__load_order_file, 'r') as reader:
        load_order = reader.read().split("\n")
    if load_order == ['']:
        load_order = []

    execute_sequence = [None]*len(load_order)
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        loc = [i for i in range(len(load_order)) if modname == load_order[i]]

        if len(loc) == 0:
            execute_sequence.append(importer)
            load_order.append(modname)
        else:
            execute_sequence[loc[0]] = importer
            load_order[loc[0]] = modname

    # Remove missing plugins from load order and execute sequence
    temp_load_order = [item for item in load_order]
    temp_execute_sequence = [item for item in execute_sequence]
    removals = 0
    for i in range(len(load_order)):
        if execute_sequence[i] == None:
            del temp_load_order[i-1*removals]
            del temp_execute_sequence[i-1*removals]
            removals += 1
    execute_sequence = temp_execute_sequence
    load_order = temp_load_order

    for i in range(len(execute_sequence)):
        importer = execute_sequence[i]
        modname = load_order[i]
        m = importer.find_module(modname).load_module(modname)
        m.execute()

    with open(__load_order_file, 'w') as writer:
        writer.writelines("\n".join(load_order))

    return
