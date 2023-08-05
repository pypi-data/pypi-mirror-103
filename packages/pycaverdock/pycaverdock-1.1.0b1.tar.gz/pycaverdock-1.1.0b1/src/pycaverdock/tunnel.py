import copy
import math
import multiprocessing
from typing import List, Tuple

from dataclasses import dataclass
from discretizer.digger import DigOpts, dig_tunnel
from discretizer.io import load_tunnel_from_pdb
from discretizer.tunnel import Tunnel

from .utils import check_path_exists


@dataclass
class Vec3D:
    x: float
    y: float
    z: float

    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def __getitem__(self, index):
        return self.to_tuple()[index]

    def copy(self):
        return copy.copy(self)


@dataclass
class Disk:
    center: Vec3D
    normal: Vec3D
    radius: float

    def copy(self) -> "Disk":
        return Disk(self.center.copy(), self.normal.copy(), self.radius)


@dataclass
class DiscretizedTunnel:
    disks: List[Disk]

    @staticmethod
    def load_from_file(path: str) -> "DiscretizedTunnel":
        disks = []
        with open(path) as f:
            for line in f:
                items = [float(v) for v in line.strip().split()]
                disks.append(
                    Disk(center=Vec3D(*items[:3]), normal=Vec3D(*items[3:6]), radius=items[6]))

        return DiscretizedTunnel(disks=disks)

    def reverse(self) -> "DiscretizedTunnel":
        return DiscretizedTunnel(disks=[d.copy() for d in self.disks[::-1]])

    def write_to_file(self, path: str):
        with open(path, "w") as f:
            self.write(f)

    def write(self, stream):
        for disk in self.disks:
            stream.write("{} {} {} {} {} {} {}\n".format(
                disk.center.x, disk.center.y, disk.center.z,
                disk.normal.x, disk.normal.y, disk.normal.z,
                disk.radius)
            )

    def __add__(self, other: "DiscretizedTunnel") -> "DiscretizedTunnel":
        assert isinstance(other, DiscretizedTunnel)
        return DiscretizedTunnel(disks=[d.copy() for d in self.disks + other.disks])


def load_tunnel(path: str) -> Tunnel:
    check_path_exists(path, "Expected tunnel file at")
    return load_tunnel_from_pdb(path)


def discretize_tunnel(tunnel: Tunnel, delta: float = 0.3,
                      threads: int = None) -> DiscretizedTunnel:
    threads = threads or multiprocessing.cpu_count()
    disks = []
    # NOTE: filename is None as it is unused
    for disk in dig_tunnel(tunnel, DigOpts(delta, str(None), threads)):
        disks.append(Disk(Vec3D(*disk.center), Vec3D(*disk.normal), disk.radius))
    return DiscretizedTunnel(disks)


def extend_tunnel(tunnel: DiscretizedTunnel, distance: float = 2, step=0.2) -> DiscretizedTunnel:
    last_disk = tunnel.disks[-1]
    normal = last_disk.normal.copy()
    center = last_disk.center.copy()

    fit = 1 / math.sqrt(normal[0] * normal[0] + normal[1] * normal[1] + normal[2] * normal[2])

    disks = []
    i = step
    while i <= distance:
        center = Vec3D(
            center[0] + (normal[0] * fit * i),
            center[1] + (normal[1] * fit * i),
            center[2] + (normal[2] * fit * i)
        )
        disks.append(Disk(center, normal, last_disk.radius))
        i += step
    return DiscretizedTunnel(disks)
