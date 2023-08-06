# -*- coding: utf-8 -*-
r"""
Gets and summarizes the results of a minimization executed with spindyanmic of the spinD code for a system with a
skyrmion.
"""
import pandas as pd
from results.igetresults import IResults
from pathlib import Path
from typing import Union, List, Tuple, Dict


class CSDSkyrmion(IResults):
    r"""
    This class can be called in folder after a minimization of a skyrmionic system with the SpinD code. This system can
    be a monolayer or a multilayer.
    """

    def __init__(self, calc_dir: Path = Path.cwd()) -> None:
        r"""
        Initializes the result-summarizing process.

        Args:
            calc_dir(Path): directory of the spinD calculation. Default is the current working directory.
        """
        self.calc_dir = calc_dir
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
        print(computationtime)
        print(laststep)
        print(totalenergy)
        print(torque)

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
