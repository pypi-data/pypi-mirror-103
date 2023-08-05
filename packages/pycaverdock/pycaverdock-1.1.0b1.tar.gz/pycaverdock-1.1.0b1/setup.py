# coding=utf-8

from setuptools import find_packages, setup

DESCRIPTION="""CaverDock is a software tool for rapid analysis of transport processes in proteins. It models the transportation of a ligand - a substrate, a product, an inhibitor, a co-factor or a co-solvent - from outside environment into the protein active or binding site and vice versa.

The input for the calculation is a protein structure in PDB format and a ligand structure in the PDBQT format. The outputs are ligand’s trajectory and energetic profile. CaverDock implements a novel algorithm which is based on molecular docking and is able to produce contiguous ligand trajectory and estimation of a binding energy along the pathway.

The current version of CaverDock uses Caver for pathway identification and heavily modified Autodock Vina as a docking engine. The tool is much faster than molecular dynamic simulations (2-20 min per job), making it suitable even for virtual screening. The software is extremely easy to use as it requires in its minimalistic configuration the setup for AutoDock Vina and geometry of the tunnel.

This API wraps all calculation steps to Python functions and enables the users to construct customized high throughput analysis pipelines."""

with open("requirements.txt") as reqs:
    requirements = reqs.read().splitlines(keepends=False)

setup(
    name="pycaverdock",
    version="1.1.0b1",
    author="CaverDock team",
    author_email="caver@caver.cz",
    description="Python API for CaverDock",
    long_description=DESCRIPTION,
    keywords=["CaverDock", "protein", "tunnel", "docking", "ligand"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cd-energyprofile=pycaverdock.bin.energyprofile:main",
            "cd-extendtunnel=pycaverdock.bin.extendtunnel:main",
            "cd-prepareconf=pycaverdock.bin.prepareconf:main"
        ],
    }
)
