import math
import os
import subprocess
from typing import List

from .tunnel import DiscretizedTunnel, Vec3D


def calculate_dist_max(atoms: List[Vec3D]) -> float:
    dist_max = 0.0
    for i in range(0, len(atoms)):
        for j in range(i + 1, len(atoms)):
            dist = math.sqrt(
                pow(atoms[i][0] - atoms[j][0], 2.0) + pow(atoms[i][1] - atoms[j][1], 2.0) + pow(
                    atoms[i][2] - atoms[j][2], 2.0))
            if dist > dist_max:
                dist_max = dist
    dist_max *= 1.3  # approx of deformation
    dist_max += 3.0  # approx of max atom diameter
    return dist_max


def get_ligand_atoms(ligand_path: str) -> List[Vec3D]:
    atoms = []
    with open(ligand_path) as f:
        for line in f:
            words = line.strip().split()
            if words[0] == "ATOM":
                atoms.append(Vec3D(float(words[5]), float(words[6]), float(words[7])))
    return atoms


def generate_caverdock_config(ligand_path: str,
                              receptor_path: str,
                              tunnel: DiscretizedTunnel,
                              tunnel_path: str) -> str:
    atoms = get_ligand_atoms(ligand_path)
    dist_max = calculate_dist_max(atoms)

    # Set starting grid
    disk = tunnel.disks[0]
    box = [
        [disk.center[i] - disk.radius - dist_max for i in range(0, 3)],
        [disk.center[i] - disk.radius + dist_max for i in range(0, 3)]
    ]

    # Compute grid size according to tunnel
    for disk in tunnel.disks:
        for i in range(0, 3):
            if box[0][i] > disk.center[i] - disk.radius - dist_max:
                box[0][i] = disk.center[i] - disk.radius - dist_max
            if box[1][i] < disk.center[i] + disk.radius + dist_max:
                box[1][i] = disk.center[i] + disk.radius + dist_max

    center = [0, 0, 0]
    size = [0, 0, 0]
    for i in range(0, 3):
        size[i] = box[1][i] - box[0][i]
        center[i] = box[0][i] + size[i] / 2.0

    config = f"""
receptor = {os.path.abspath(receptor_path)}
ligand = {os.path.abspath(ligand_path)}
tunnel = {os.path.abspath(tunnel_path)}
center_x = {center[0]}
center_y = {center[1]}
center_z = {center[2]}
size_x = {int(size[0] + 0.5)}
size_y = {int(size[1] + 0.5)}
size_z = {int(size[2] + 0.5)}
exhaustiveness = 1
cpu = 1
""".strip()
    return config


class CaverDock:
    def __init__(self, binary: str):
        self.binary = os.path.abspath(binary)

    def run(self,
            directory: str,
            name: str,
            ligand: str,
            receptor: str,
            tunnel: DiscretizedTunnel,
            mpi_processes=None,
            calculate_ub=False):
        os.makedirs(directory, exist_ok=True)

        config_path = os.path.join(directory, f"{name}.config")
        tunnel_path = os.path.join(directory, f"{name}.dsd")

        tunnel.write_to_file(tunnel_path)
        with open(config_path, "w") as config_file:
            config = generate_caverdock_config(ligand, receptor, tunnel, tunnel_path)
            config_file.write(config)

        args = [
            self.binary,
            "--config", config_path,
            "--out", name,
            "--log", "caverdock.log"
        ]
        if not calculate_ub:
            args += ["--final_state", "LB"]
        if mpi_processes:
            args = ["mpirun", "-np", str(mpi_processes)] + args

        subprocess.run(args, cwd=directory, check=True)

        results = {"lb": os.path.join(directory, get_result_path(name, False))}
        if calculate_ub:
            results["ub"] = os.path.join(directory, get_result_path(name, True))

        return results


def get_result_path(name: str, upperbound: bool) -> str:
    end = "ub" if upperbound else "lb"
    return f"{name}-{end}.pdbqt"
