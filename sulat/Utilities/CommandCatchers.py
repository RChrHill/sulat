"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Utilities/CommandCatchers.py

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

from .Path import get_by_path, set_by_path, deep_search


class CommandCatcher:
    def __init__(self, obj_ref, parent_command_queue):
        self.command_queue_ref = parent_command_queue
        self.obj_ref = obj_ref

    def __getattr__(self, item):
        self.command_queue_ref.append(lambda: getattr(self.obj_ref, item))
        return CallCatcher(item, len(self.command_queue_ref) - 1, self.command_queue_ref)


class CallCatcher:
    def __init__(self, name, idx, parent_command_queue):
        self.name = name
        self.idx = idx
        self.command_queue_ref = parent_command_queue

    def __call__(self, *args, **kwargs):
        args = list(args)

        caughtcommand_idxs = deep_search(args, lambda x: isinstance(x, CaughtCommand))
        caughtcommand_keys = deep_search(kwargs, lambda x: isinstance(x, CaughtCommand))

        for idx, obj in zip(caughtcommand_idxs, self.command_queue_ref[self.idx + 1:]):
            set_by_path(args, idx, obj)
        for key, obj in zip(caughtcommand_keys, self.command_queue_ref[self.idx + 1 + len(caughtcommand_idxs):]):
            set_by_path(kwargs, key, obj)

        # Now clean up any returned CallCatcher objects that were not called
        # The index of a command ensures that this only runs when exiting scope
        callcatcher_idxs = deep_search(args, lambda x: isinstance(x, CallCatcher))
        callcatcher_keys = deep_search(kwargs, lambda x: isinstance(x, CallCatcher))

        lambda_type = type(lambda: None)
        callcatcher_ids = [self.idx + 1 + i for i, x in enumerate(self.command_queue_ref[self.idx + 1:]) if
                           type(x) == lambda_type]

        for idx, cc_id in zip(callcatcher_idxs, callcatcher_ids):
            set_by_path(args, idx, self.command_queue_ref[cc_id])
        for key, cc_id in zip(callcatcher_keys, callcatcher_ids[len(callcatcher_idxs):]):
            set_by_path(kwargs, key, self.command_queue_ref[cc_id])

        function_ref = self.command_queue_ref[self.idx]
        caught_command = CaughtCommand(self.name, args, kwargs, function_ref)
        self.command_queue_ref[self.idx] = caught_command

        for _ in reversed(range(self.idx + 1, len(self.command_queue_ref))):
            self.command_queue_ref.pop(-1)  # Could equally pass _,
                                            # but lists are optimised for 1st and final index removal

        return caught_command


class CaughtCommand:
    def __init__(self, attr, args, kwargs, attr_getter):
        self.attr = attr
        self.args = args
        self.kwargs = kwargs
        self.attr_getter = attr_getter

    def __call__(self):
        args = [arg for arg in self.args]
        for idx in deep_search(args, callable):
            result = get_by_path(self.args, idx)()
            set_by_path(args, idx, result)
        kwargs = {name: self.kwargs[name] for name in self.kwargs}
        for key in deep_search(kwargs, callable):
            result = get_by_path(self.kwargs, key)()
            set_by_path(kwargs, key, result)
        return self.attr_getter()(*args, **kwargs)

    def __repr__(self):
        arg_repr = []
        arg_repr.extend([str(arg) for arg in self.args])
        arg_repr.extend(['='.join((key, str(self.kwargs[key]))) for key in self.kwargs])
        if len(arg_repr) == 0:
            arg_string = ''
        else:
            arg_string = f"({', '.join(arg_repr)})"
        return f"CaughtCommand <obj>.{self.attr}{arg_string}"
