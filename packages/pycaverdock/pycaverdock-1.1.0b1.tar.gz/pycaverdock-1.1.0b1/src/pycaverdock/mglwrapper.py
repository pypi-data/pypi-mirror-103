import os
import subprocess

from dataclasses import dataclass

from .utils import change_cwd, check_path_exists, ensure_dir

PYTHON_SH_PATH = "bin/pythonsh"
SCRIPTS_DIR = "MGLToolsPckgs/AutoDockTools/Utilities24"
PREPARE_RECEPTOR_PATH = os.path.join(SCRIPTS_DIR, "prepare_receptor4.py")
PREPARE_LIGAND_PATH = os.path.join(SCRIPTS_DIR, "prepare_ligand4.py")


@dataclass
class Ligand:
    path: str


@dataclass
class Receptor:
    path: str


class MglWrapper:
    def __init__(self, mgltools_root: str):
        self.mgltools_root = os.path.abspath(mgltools_root)
        check_path_exists(os.path.join(self.mgltools_root, "bin"),
                          "Expected MGLTools directory at")

    def prepare_receptor(self, receptor: str, output_path: str) -> Receptor:
        check_path_exists(receptor, "Expected receptor file at")

        input_path = os.path.abspath(receptor)
        ensure_dir(output_path)

        self.exec([
            self.mgl_path(PYTHON_SH_PATH),
            self.mgl_path(PREPARE_RECEPTOR_PATH),
            "-r", input_path,
            "-o", output_path
        ])
        return Receptor(output_path)

    def prepare_ligand(self, ligand: str, output_path: str) -> Ligand:
        check_path_exists(ligand, "Expected ligand file at")

        input_path = os.path.abspath(ligand)
        ensure_dir(output_path)

        # Workaround for bug in prepare_ligand4.py, it only works with relative paths
        with change_cwd(os.path.dirname(input_path)):
            self.exec([
                self.mgl_path(PYTHON_SH_PATH),
                self.mgl_path(PREPARE_LIGAND_PATH),
                "-l", input_path,
                "-o", output_path
            ])
        return Ligand(output_path)

    def mgl_path(self, path: str) -> str:
        return os.path.join(self.mgltools_root, path)

    def exec(self, args):
        return subprocess.run(args, check=True)
