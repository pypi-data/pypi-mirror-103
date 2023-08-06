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

    def __init__(self, calc_dir: Path = Path.cwd(), nlayer: int = 1, signaturename: str = 'signature',
                 signaturevalue: Union[float, str] = 0) -> None:
        r"""
        Initializes the result-summarizing process.

        Args:
            calc_dir(Path): directory of the spinD calculation. Default is the current working directory.

            nlayer(int): number of layers for the system.

            signaturename(str): if multiple calculations are evaluated with the goal to connect the dataframes then you
            can define a signaturename which the column names which describes what quantity changes from calc. to calc.
            It can be for example magnetic field or interlayer exchange

            signaturevalue(float, str): The value for the current calculation
        """
        self.calc_dir = calc_dir
        self.nlayer = nlayer
        self.signaturename = signaturename
        self.signaturevalue = signaturevalue
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
        Returns:
            the DataFrame with the information from the spindynamics calculation
        """
        laststep, totalenergy, torque = self.convergencefile()
        skprofile_i, skprofile_f = self.skyrmions()
        densities = self.energydensity()

        d = {self.signaturename: self.signaturevalue,
             't_computation': self.computationtime(),
             'steps': laststep,
             'en_per_UC': totalenergy,
             'torque': torque}
        d.update(skprofile_i)
        d.update(skprofile_f)
        d.update(densities)
        return pd.DataFrame(d, index=[self.signaturevalue])

    def energydensity(self) -> Dict[str, Union[None,float]]:
        r"""
        Reads the energy_density_end.dat file if the energy density file exists

        Returns:
            a dictionary containing the sum of the nergy contributions for each layer
        """
        if not self.i_en_dens:
            endict = {}
            for idx in range(self.nlayer):
                endict[f'ex_intra_lay{idx}'] = None
                endict[f'ex_inter_lay{idx}'] = None
                endict[f'dmi_lay{idx}'] = None
                endict[f'ani_lay{idx}'] = None
                endict[f'zee_lay{idx}'] = None
                endict[f'dip_lay{idx}'] = None
                endict[f'biq_lay{idx}'] = None
                endict[f'four_lay{idx}'] = None
                endict[f'tot_lay{idx}'] = None
            return endict
        df = pd.read_csv(self.calc_dir / 'energy_density_end.dat', sep=r'\s+', index_col=False)
        df.columns = ['x', 'y', 'z', 'ex_intra', 'ex_inter', 'dmi', 'ani', 'zee', 'dip', 'biq', 'four', 'tot']
        z_layer = df.z.unique()
        endict = {}
        for (idx, zl) in enumerate(z_layer):
            dfl = df[df['z'] == zl]
            endict[f'ex_intra_lay{idx}'] = dfl.ex_intra.sum()
            endict[f'ex_inter_lay{idx}'] = dfl.ex_inter.sum()
            endict[f'dmi_lay{idx}'] = dfl.dmi.sum()
            endict[f'ani_lay{idx}'] = dfl.ani.sum()
            endict[f'zee_lay{idx}'] = dfl.zee.sum()
            endict[f'dip_lay{idx}'] = dfl.dip.sum()
            endict[f'biq_lay{idx}'] = dfl.biq.sum()
            endict[f'four_lay{idx}'] = dfl.four.sum()
            endict[f'tot_lay{idx}'] = dfl.tot.sum()
        return endict

    def skyrmions(self) -> Tuple[Dict[str, Union[float, None]], Dict[str, Union[float, None]]]:
        r"""
        Calculates the skyrmion profiles for each layer for the SpinSTMi file and the SpinSTM_end file.
        """
        if self.i_stmi:
            stmiresult = self.skyrmionprofile(self.calc_dir / 'SpinSTMi.dat')
        else:
            stmiresult = {}
            for n in range(self.nlayer):
                stmiresult[f'rad_lay{n}'] = None
                stmiresult[f'R0x_lay{n}'] = None
                stmiresult[f'R0y_lay{n}'] = None
                stmiresult[f'c_lay{n}'] = None
                stmiresult[f'w_lay{n}'] = None
        if self.i_stmend:
            stmendresult = self.skyrmionprofile(self.calc_dir / 'SpinSTM_end.dat')
        else:
            stmendresult = {}
            for n in range(self.nlayer):
                stmendresult[f'rad_lay{n}'] = None
                stmendresult[f'R0x_lay{n}'] = None
                stmendresult[f'R0y_lay{n}'] = None
                stmendresult[f'c_lay{n}'] = None
                stmendresult[f'w_lay{n}'] = None
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
        for n in range(self.nlayer):
            if ML.Layer[n].sk_radius is None:
                profiles[f'rad_lay{n}'] = None
                profiles[f'R0x_lay{n}'] = None
                profiles[f'R0y_lay{n}'] = None
                profiles[f'c_lay{n}'] = None
                profiles[f'w_lay{n}'] = None
            else:
                profiles[f'rad_lay{n}'] = ML.Layer[n].sk_radius
                profiles[f'R0x_lay{n}'] = ML.Layer[n].sk_popt[0]
                profiles[f'R0y_lay{n}'] = ML.Layer[n].sk_popt[1]
                profiles[f'c_lay{n}'] = ML.Layer[n].sk_popt[2]
                profiles[f'w_lay{n}'] = ML.Layer[n].sk_popt[3]
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
