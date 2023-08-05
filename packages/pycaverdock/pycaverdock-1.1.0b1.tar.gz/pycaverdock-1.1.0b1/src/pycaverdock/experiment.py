import hashlib
import json
import logging
import os
import shutil
from io import StringIO

import pylru
from dataclasses import dataclass

from .caverdock import CaverDock, get_result_path
from .mglwrapper import Ligand, MglWrapper, Receptor
from .tunnel import DiscretizedTunnel, discretize_tunnel, load_tunnel
from .utils import check_path_exists, get_basename


@dataclass
class InputFile:
    path: str


class Workdir:
    def __init__(self, directory: str, memory_cache_size=1000):
        self.directory = os.path.abspath(directory)
        self.cache_directory = os.path.join(self.directory, "cache")
        os.makedirs(self.cache_directory, exist_ok=True)
        self.cache = pylru.lrucache(memory_cache_size)

    def resolve_entry(self, load_fn, compute_fn, args):
        key = self.create_key(args)
        entry_path = self.entry_path(key)
        if self.has_entry(key):
            resolved = self.cache.get(key)
            if resolved is not None:
                return resolved
            return load_fn(entry_path)
        value = compute_fn(entry_path)
        self.cache[key] = value
        return value

    def entry_path(self, key: str) -> str:
        return os.path.join(self.cache_directory, key)

    def has_entry(self, key: str) -> bool:
        return os.path.isfile(self.entry_path(key)) or key in self.cache

    def create_key(self, args: dict) -> str:
        args = dict(args)
        for (key, value) in args.items():
            if isinstance(value, InputFile):
                check_path_exists(value.path, f"File {value.path} not found")
                args[key] = hash_file(value.path)

        hash = hashlib.md5()
        hash.update(json.dumps(args, indent=False).encode())
        return hash.hexdigest()


class Experiment:
    def __init__(self, workdir: Workdir, name: str, mgl: MglWrapper, caverdock: CaverDock):
        self.workdir = workdir
        self.name = name
        self.mgl = mgl
        self.caverdock = caverdock

        self.directory = os.path.join(workdir.directory, "experiments", self.name)
        os.makedirs(self.directory, exist_ok=True)
        self.input_dir = os.path.join(self.directory, "inputs")
        os.makedirs(self.input_dir, exist_ok=True)
        self.intermediate_dir = os.path.join(self.directory, "intermediate")
        os.makedirs(self.intermediate_dir, exist_ok=True)
        self.result_dir = os.path.join(self.directory, "results")
        os.makedirs(self.result_dir, exist_ok=True)
        self.caverdock_directory = os.path.join(self.intermediate_dir, "caverdock")
        os.makedirs(self.caverdock_directory, exist_ok=True)

    def store_input_file(self, file: str, overwrite=True):
        basename = os.path.basename(file)
        path = os.path.join(self.input_dir, basename)
        if not overwrite and os.path.isfile(path):
            logging.warning(
                f"Input with name {basename} for experiment {self.name} already exists")
        shutil.copyfile(file, path)

    def intermediate_path(self, file: str):
        return os.path.join(self.intermediate_dir, file)

    def result_path(self, file: str):
        return os.path.join(self.result_dir, file)

    def prepare_ligand(self, ligand_path: str) -> Ligand:
        args = dict(ligand=InputFile(ligand_path))

        def compute(output_path: str):
            return self.mgl.prepare_ligand(ligand_path, output_path)

        def load(input_path: str):
            return Ligand(input_path)

        return self.workdir.resolve_entry(load, compute, args)

    def prepare_receptor(self, receptor_path: str) -> Receptor:
        args = dict(receptor=InputFile(receptor_path))

        def compute(output_path: str):
            return self.mgl.prepare_receptor(receptor_path, output_path)

        def load(input_path: str):
            return Receptor(input_path)

        return self.workdir.resolve_entry(load, compute, args)

    def discretized_tunnel(self, tunnel_path: str, delta: float) -> DiscretizedTunnel:
        args = dict(
            tunnel=InputFile(tunnel_path),
            delta=delta
        )

        def compute(output_path: str):
            tunnel = discretize_tunnel(load_tunnel(tunnel_path), delta=delta)
            tunnel.write_to_file(output_path)
            return tunnel

        def load(input_path: str):
            return DiscretizedTunnel.load_from_file(input_path)

        tunnel = self.workdir.resolve_entry(load, compute, args)
        name = f"{get_basename(tunnel_path)}-discretized.dsd"
        tunnel.write_to_file(self.intermediate_path(name))
        return tunnel

    def caverdock_trajectory(self,
                             ligand: Ligand,
                             receptor: Receptor,
                             tunnel: DiscretizedTunnel,
                             upperbound: bool):
        # TODO: multiple caverdock runs inside a single experiment?
        name = "caverdock"
        args = dict(
            ligand=InputFile(ligand.path),
            receptor=InputFile(receptor.path),
            tunnel=hash_discretized_tunnel(tunnel),
            upperbound=upperbound
        )

        def compute(output_path: str):
            self.caverdock.run(self.caverdock_directory,
                               name,
                               ligand.path,
                               receptor.path,
                               tunnel,
                               calculate_ub=upperbound,
                               mpi_processes=2)  # TODO
            data = {
                "lb": os.path.join(self.caverdock_directory,
                                   get_result_path(name, upperbound=False)),
                "ub": os.path.join(self.caverdock_directory,
                                   get_result_path(name, upperbound=True))
            }
            compress_files(data, output_path)
            return data

        def load(input_path: str):
            unpack_path = os.path.join(self.caverdock_directory, "unpacked")
            os.makedirs(unpack_path, exist_ok=True)
            return decompress_files(input_path, unpack_path)

        return self.workdir.resolve_entry(load, compute, args)


def compress_files(file_map, output_path: str):
    data = {}
    for (tag, file_path) in file_map.items():
        if os.path.isfile(file_path):
            with open(file_path) as f:
                data[tag] = f.read()  # TODO: store compressed and in binary form
        else:
            data[tag] = None
    with open(output_path, "w") as f:
        json.dump(data, f)


def decompress_files(input_path: str, unpack_dir: str) -> dict:
    data = {}
    with open(input_path) as f:
        stored = json.load(f)
        for (key, value) in stored.items():
            if value is not None:
                path = os.path.join(unpack_dir, key)
                with open(path, "w") as f:
                    f.write(value)
                data[key] = path
            else:
                data[key] = None
    return data


def hash_file(path: str) -> str:
    hash = hashlib.md5()

    with open(path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            hash.update(data)
    return hash.hexdigest()


def hash_discretized_tunnel(tunnel: DiscretizedTunnel) -> str:
    state = hashlib.md5()

    io = StringIO()
    tunnel.write(io)

    io.seek(0)
    state.update(io.read().encode())
    return state.hexdigest()
