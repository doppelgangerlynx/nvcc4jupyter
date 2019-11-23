import os
import subprocess
import tempfile
import uuid

from IPython.core.magic import Magics, cell_magic, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from common import helper


compiler = '/usr/local/cuda/bin/nvcc'
nsight_excutable = '/usr/local/cuda/bin/nv-nsight-cu-cli'
ext = '.cu'


@magics_class
class NVCCPluginV3(Magics):

    def __init__(self, shell):
        super(NVCCPluginV3, self).__init__(shell)

        self.argparser = helper.get_argparser()
        # TODO: implement more...
    
    @staticmethod
    def compile(file_path, compile_args=[]):
        subprocess.check_output(
            [compiler] + compile_args + [file_path + ext, "-o", file_path + ".out", '-Wno-deprecated-gpu-targets'],
            stderr=subprocess.STDOUT
                )
    
    def nsight_run(self, file_path, timeit=False, custom_commands = []):
        if timeit:
            stmt = f"subprocess.check_output(['{nsight_excutable}',] + [" + ", ".join(custom_commands) + f"] + ['{file_path}.out'], stderr=subprocess.STDOUT)"
            print(stmt)
            output = self.shell.run_cell_magic(
                magic_name="timeit", line="-q -o import subprocess", cell=stmt)
        else:
            output = subprocess.check_output(
                [nsight_excutable,] +  custom_commands +[file_path + ".out",], stderr=subprocess.STDOUT)
            output = output.decode('utf8')
            
        helper.print_out(output)
        return None
    
    @cell_magic
    # change this to nsight function....
    def nv_nsight(self, line, cell):
        try:
            args = self.argparser.parse_args(line.split())
        except SystemExit as e:
            self.argparser.print_help()
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, str(uuid.uuid4()))
            with open(file_path + ext, "w") as f:
                f.write(cell)
            try:
                compile_args = []
                if args.compile_custom:
                    compile_args = args.compile_custom
                else:
                    compile_args = input("Please provide custom compile arguments: ").split()
                self.compile(file_path, compile_args)
                args_custom =[]
                if args.custom:
                    args_custom = args.custom
                output = self.nvprof_run(file_path, timeit=args.timeit, custom_commands = args_custom)
            except subprocess.CalledProcessError as e:
                helper.print_out(e.output.decode("utf8"))
                output = None
        return output