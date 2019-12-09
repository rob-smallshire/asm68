import os
import importlib.util
import logging

from asmdsl import statements
from assembler import assemble

logger = logging.getLogger(__name__)

def asm(source_filepath, output_file, output_format, multiplicity):
    """
    Args:
        source_filepath: A string path to the source file.
        
        output_file: A file-like object to which the output will be written.
    
        output_format: "bin", "hex" or "srec"
        
        multiplicity: The number of times binary data will be copied into
            the output file. Useful for 'doubling-up' binary images for
            putting, say, a 16 K image into a 32 K EPROM.
    
    Raises:
        FileNotFoundError: If the source_filepath could not be found.
        ModuleLoadError: If the module could not be loaded.
    """
    try:
        m = import_module_from_file(source_filepath)
    except Exception as e:
        raise ModuleLoadError(
            source_filepath,
            e
        )
    code_blocks = assemble(statements(m.asm))
    for address, code in code_blocks.items():
        hex_assembly = ' '.join(format(b, '02X') for b in code)
        logger.debug("{:04X}: {}".format(address, hex_assembly))
        logger.info("code length: {} bytes".format(len(code)))
        
    export_code_blocks(output_file, code_blocks, output_format, multiplicity)    


class ModuleLoadError(Exception):
    
    def __init__(self, module_filepath, exception):
        super.__init__(f"Could not load module: {str(module_filepath)}")
        self.filepath = module_filepath
        self.exception = exception


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

def export_code_blocks(output_file, code_blocks, output_format, multiplicity):
    try:
        exporter = EXPORTERS[output_format]
    except KeyError:
        raise ValueError(f"Unsupported export format {output_format}")
    
    exporter(output_file, code_blocks, multiplicity)


def export_bin(output_file, code_blocks, multiplicity=1):
    if multiplicity < 1:
        raise ValueError(f"Multiplicity {multiplicity} is less than one")
    if len(code_blocks) != 1:
        raise ValueError("Can only export bin for single code block")
    address, code = next(iter(code_blocks.items()))
    for _ in range(multiplicity):
        output_file.write(code)
    logging.info(f"Wrote {len(code) * multiplicity} bytes")

EXPORTERS = {
    "bin": export_bin,
    # "hex": export_hex,
    # "srec": export_srec,
}
