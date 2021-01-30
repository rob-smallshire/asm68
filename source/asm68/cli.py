"""
Asm68.

A Motorola 6809 and Hitachi 6309 assembler implemented as an
internal domain-specific language hosted in Python 3.

Usage:
  asm68 <module-filepath> <bin-filepath>
"""
import sys
from traceback import extract_tb, print_exception
import logging

import click
from exit_codes import ExitCode

from asm68.version import __version__, program_name
from asm68 import api
from asm68.util import take_after


log_levels = tuple(logging._levelToName.values())


@click.group()
@click.option(
    "--verbosity",
    default="WARNING",
    help="The logging level to use.",
    type=click.Choice(log_levels, case_sensitive=True),
)


@click.version_option(
    version=__version__,
    prog_name="asm68"
)
def cli(verbosity):
    logging_level = getattr(logging, verbosity)
    logging.basicConfig(level=logging_level)


@cli.command(name="asm")
@click.argument("source", type=click.Path(exists=True, path_type=str))
@click.option("--output", type=click.File('wb'))
@click.option("--format", type=click.Choice(["hex", "srec", "bin"]), help="Output file format", default="bin")
@click.option("--repeat", type=int, help="Number of copies in the binary output file", default=1)
def asm(source, output, format, repeat):
    try:
        api.asm(source, output, output_format=format, repeat=repeat)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return ExitCode.OS_FILE
    except api.TooManyPassesError as too_many_passes_error:
        click.secho("Too many assembler passes required", fg="red")
        click.secho("Unresolved labels: {}".format(", ".join(too_many_passes_error.unresolved_label_names))),
        click.secho("Unreferenced labels: {}".format(", ".join(too_many_passes_error.unreferenced_label_names)))
        sys.exit(ExitCode.DATA_ERR)
    except api.ModuleLoadError as module_load_error:
        e = module_load_error.exception
        tb = e.__traceback__
        tb_entries = extract_tb(tb)
        num_truncated_tb_entries = sum(1 for _ in take_after(
            lambda entry: source in entry.filename,
            tb_entries))
        click.secho("Error in module to be assembled: {}".format(source), fg="red")
        print_exception(type(e), e, tb, limit=-num_truncated_tb_entries, file=sys.stderr, chain=False)
        sys.exit(ExitCode.DATA_ERR)

    sys.exit(ExitCode.OK)


if __name__ == "__main__":
    cli(prog_name=program_name)
