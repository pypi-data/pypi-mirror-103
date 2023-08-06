# -*- coding: utf-8 -*-
r"""
Gets and summarizes the results of a minimization executed with spindyanmic of the spinD code for a system with a
skyrmion.
"""
import pandas as pd
import numpy as np
from results.igetresults import IResults
from pathlib import Path
from typing import Union, List, Tuple, Dict
from python3.magnetisations import SpinLattice, MultiLayer


class CSDSkyrmion(IResults):
    r"""
    This class can be called in folder after a minimization of a skyrmionic system with the SpinD code. This system can
    be a monolayer or a multilayer.
    """

    def __init__(self, calc_dir: Path = Path.cwd(), nlayer: int = 1) -> None:
        r"""
        Initializes the result-summarizing process.

        Args:
            calc_dir(Path): directory of the spinD calculation. Default is the current working directory.
            nlayer(int): number of layers for the system.
        """
        self.calc_dir = calc_dir
        self.nlayer = nlayer
        self.i_en_dens = (calc_dir / 'energy_density_end.dat').is_file()
        self.i_conv = (calc_dir / 'convergence.dat').is_file()
        self.i_job = (calc_dir / 'job.out').is_file()
        self.i_stmend = (calc_dir / 'SpinSTM_end.dat').is_file()
        self.i_stmi = (calc_dir / 'SpinSTMi.dat').is_file()

        if not any([self.i_en_dens, self.i_conv, self.i_job, self.i_stmend, self.i_stmi]):
            print('None of the following files is present: energy_density_end.dat, convergence.dat, job.out')
            print('SpinSTM_end.dat, SpinSTMi.dat -> finished.')

    def __call__(self) -> pd.DataFrame:
        r"""

        """
        computationtime = self.computationtime()
        laststep, totalenergy, torque = self.convergencefile()
        skprofile_i, skprofile_f = self.skyrmions()
        print(computationtime)
        print(laststep)
        print(totalenergy)
        print(torque)
        print(skprofile_i)
        print(skprofile_f)

    def skyrmions(self) -> Tuple[Dict[str, Union[float, None]], Dict[str, Union[float, None]]]:
        r"""
        Calculates the skyrmion profiles for each layer for the SpinSTMi file and the SpinSTM_end file.
        """
        if self.i_stmi:
            stmiresult = self.skyrmionprofile(self.calc_dir / 'SpinSTMi.dat')
        else:
            stmiresult = {}
            for n in range(self.nlayer):
                stmiresult[f'sk{n}_rad'] = None
                stmiresult[f'sk{n}_R0x'] = None
                stmiresult[f'sk{n}_R0y'] = None
                stmiresult[f'sk{n}_c'] = None
                stmiresult[f'sk{n}_w'] = None
        if self.i_stmend:
            stmendresult = self.skyrmionprofile(self.calc_dir / 'SpinSTM_end.dat')
        else:
            stmendresult = {}
            for n in range(self.nlayer):
                stmendresult[f'sk{n}_rad'] = None
                stmendresult[f'sk{n}_R0x'] = None
                stmendresult[f'sk{n}_R0y'] = None
                stmendresult[f'sk{n}_c'] = None
                stmendresult[f'sk{n}_w'] = None
        return stmiresult, stmendresult

    def skyrmionprofile(self, file: Path) -> Dict[str, float]:
        r"""
        Reads the spin lattice from a SpinSTM file, evaluates the skyr. profile with the use of the userlib-spinD-lib.

        Args:
            file(Path): SpinSTM-file

        Returns:
            The dict with the following keys:
            skj_rad : radius of sk in the j - layer
            skj_R0x : x-component of the center of sk in the j - layer
            skj_R0y : y-component of the center of sk in the j - layer
            skj_c : c-param of the profile of sk in the j - layer
            skj_w : c-param of the profile of sk in the j - layer
        """
        ML = MultiLayer(path=str(file), number_layers=self.nlayer)
        for lay in ML.Layer:
            lay.getSkradius()
            profiles = {}
        for layidx in range(self.nlayer):
            if ML.Layer[layidx].sk_radius is None:
                profiles[f'sk{layidx}_rad'] = None
                profiles[f'sk{layidx}_R0x'] = None
                profiles[f'sk{layidx}_R0y'] = None
                profiles[f'sk{layidx}_c'] = None
                profiles[f'sk{layidx}_w'] = None
            else:
                profiles[f'sk{layidx}_rad'] = ML.Layer[layidx].sk_radius
                profiles[f'sk{layidx}_R0x'] = ML.Layer[layidx].sk_popt[0]
                profiles[f'sk{layidx}_R0y'] = ML.Layer[layidx].sk_popt[1]
                profiles[f'sk{layidx}_c'] = ML.Layer[layidx].sk_popt[2]
                profiles[f'sk{layidx}_w'] = ML.Layer[layidx].sk_popt[3]
        return profiles

    def convergencefile(self) -> Union[Tuple[float, float, float], Tuple[None, None, None]]:
        r"""
        Reads the convergence file of the calculation if it exists.

        Returns:
            the number of steps necessary for convergence, the total energy and the last torque. If the file doesn't
            exist it returns None for all three of them
        """
        if not self.i_conv:
            return None, None, None
        for line in reversed(open(str(self.calc_dir / 'convergence.dat')).readlines()):
            L = line.split()
            break
        return int(L[0]), float(L[1]), float(L[2])

    def computationtime(self) -> Union[float, None]:
        r"""
        Checks the computation time of the calculation

        Returns:
            either the computation time written in job.out or None if job.out doesn't exist or the specific line is
            not present in job.out
        """
        if not self.i_job:
            return None
        line_exi = False
        with open(str(self.calc_dir / 'job.out')) as f:
            for line in f:
                if line.lstrip().startswith('computation time:'):
                    line_exi = True
                    return float(line.split()[2])
        if not line_exi:
            return None
