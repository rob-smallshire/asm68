import sys

from .version import program_name
from .cli import cli

sys.exit(cli(prog_name=program_name))

