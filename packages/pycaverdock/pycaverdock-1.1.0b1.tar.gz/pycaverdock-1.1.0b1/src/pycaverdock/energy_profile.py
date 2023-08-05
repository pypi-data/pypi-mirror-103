from collections import defaultdict

import pandas as pd
from dataclasses import dataclass

from .tunnel import DiscretizedTunnel


@dataclass
class EnergyProfile:
    frame: pd.DataFrame

    def write_to_dat(self, path: str):
        with open(path, "w") as f:
            self.write(f)

    def write(self, stream):
        for line in self.frame.itertuples():
            stream.write(
                f"{line.distance} {line.disk} {line.minE} {line.maxE} {line.radius} {line.lbE}\n")


def create_energy_profile(tunnel: DiscretizedTunnel, caverdock_trajectory: str,
                          start_disc=0) -> EnergyProfile:
    last = []
    dist = 0.0
    disk = 0
    minE = 1000000.0
    maxE = -1000000.0
    lbE = 0.0
    radius = 0.0

    data = defaultdict(list)

    def add_row(dist: float, disk: int, minE: float, maxE: float, radius: float, lbE: float):
        data["distance"].append(dist)
        data["disk"].append(disk - start_disc)
        data["minE"].append(minE)
        data["maxE"].append(maxE)
        data["radius"].append(radius)
        data["lbE"].append(lbE)

    with open(caverdock_trajectory) as trfile:
        trline = trfile.readline()
        "#distance disc min UB energy, max UB energy, radius, LB energy"
        for (index, tunnel_disk) in enumerate(tunnel.disks):
            if index < start_disc:
                disk += 1
            else:
                center = tunnel_disk.center
                normal = tunnel_disk.normal
                if not last:
                    last = center
                else:
                    # compute distance between plate of current disc and center of previous disc
                    d = - center[0] * normal[0] - center[1] * normal[1] - center[2] * normal[2]
                    t = -(normal[0] * last[0] + normal[1] * last[1] + normal[2] * last[
                        2] + d) / (
                                normal[0] * normal[0] + normal[1] * normal[1] + normal[2] *
                                normal[2])
                    dist += abs(t)
                    last = center
                # scan snapshots until other disk is reached
                while True:
                    if trline == "":
                        break
                    words = trline.split()
                    trline = trfile.readline()
                    if words[0] == "REMARK" and words[1] == "CAVERDOCK" and words[
                        2] == "RESULT:":
                        valE = float(words[3])
                    if words[0] == "REMARK" and words[1] == "CAVERDOCK" and words[
                        2] == "TUNNEL:":
                        if int(words[3]) > disk - start_disc:
                            add_row(dist, disk, minE, maxE, radius, lbE)
                            minE = valE
                            maxE = valE
                            valE = float(words[4])
                            radius = float(words[5])
                            lbE = float(words[4])
                            break
                        else:
                            maxE = max(maxE, valE)
                            minE = min(minE, valE)
                            radius = float(words[5])
                            lbE = float(words[4])
                disk += 1
        add_row(dist, disk, minE, maxE, radius, lbE)
    return EnergyProfile(pd.DataFrame(data))


def load_energy_profile(path: str) -> EnergyProfile:
    data = defaultdict(list)
    with open(path) as f:
        for line in f:
            distance, disk, minE, maxE, radius, lbE = line.strip().split()
            data["distance"].append(float(distance))
            data["disk"].append(int(disk))
            data["minE"].append(float(minE))
            data["maxE"].append(float(maxE))
            data["radius"].append(float(radius))
            data["lbE"].append(float(lbE))

    return EnergyProfile(pd.DataFrame(data))
