"""
Asm68.

A Motorola 6809 and Hitachi 6309 assembler implemented as an
internal domain-specific language hosted in Python 3.

Usage:
  asm68 <module-filepath>
"""
import os
import sys
import importlib.util
from traceback import extract_tb, print_exception

from docopt import docopt
from exit_codes import ExitCode

import asm68
from asm68.assembler import assemble
from asm68.asmdsl import statements


def import_module_from_file(module_filepath):
    """Import a module given a filepath to a *.py file.

    Args:
        module_filepath: The filepath to a Python module which must
            contain a global attribute called `asm` which is an
            AsmDsl object.

    Returns:
        The module object.

    Raises:
        FileNotFoundError: If the specified module could not be found.
    """
    module_dir, module_file = os.path.split(module_filepath)
    module_name, module_ext = os.path.splitext(module_file)
    spec = importlib.util.spec_from_file_location(module_name, module_filepath)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def take_after(predicate, iterable):
    found = False
    for item in iterable:
        found = found or predicate(item)
        if found:
            yield item


def main(argv=None):
    args = docopt(__doc__, argv=argv, version=asm68.__version__)
    module_filepath = args['<module-filepath>']
    try:
        m = import_module_from_file(module_filepath)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return ExitCode.OS_FILE
    except Exception as e:
        tb = e.__traceback__
        tb_entries = extract_tb(tb)
        num_truncated_tb_entries = sum(1 for _ in take_after(
            lambda entry: module_filepath in entry.filename,
            tb_entries))
        print("Error in module to be assembled: {}".format(module_filepath), file=sys.stderr)
        print_exception(type(e), e, tb, limit=-num_truncated_tb_entries, file=sys.stderr, chain=False)
        return ExitCode.DATA_ERR

    code_blocks = assemble(statements(m.asm))
    for address, code in code_blocks.items():
        hex_assembly = ' '.join(format(b, '02X') for b in code)
        print("{:04X}: {}".format(address, hex_assembly))
        print()
    return ExitCode.OK
