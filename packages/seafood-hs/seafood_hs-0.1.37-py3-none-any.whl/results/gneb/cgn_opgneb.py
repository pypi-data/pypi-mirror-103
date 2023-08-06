# -*- coding: utf-8 -*-
r"""
Gets and summarizes the results of a gneb calculation with a single saddlepoint.
"""
import pandas as pd
import numpy as np
from results.igetresults import IResults
from pathlib import Path
from typing import Union, Dict
from python3.shell_commands import *
import os


class CGNOpGneb(IResults):
    r"""
    Summarizes the results of a GNEB calculation with only one SP
    """

    def __init__(self, calc_dir: Path = Path.cwd(), nlayer: int = 1, signaturename: str = 'signature',
                 signaturevalue: Union[float, str] = 0, remove_energy_density: bool = False) -> None:
        r"""
        Initializes the result-summarizing process.

        Args:
            calc_dir(Path): directory of the spinD calculation. Default is the current working directory.

            nlayer(int): number of layers for the system.

            signaturename(str): if multiple calculations are evaluated with the goal to connect the dataframes then you
            can define a signaturename which the column names which describes what quantity changes from calc. to calc.
            It can be for example magnetic field or interlayer exchange

            signaturevalue(float, str): The value for the current calculation

            remove_energy_density(bool): remove energy density files after summarizing them. The default is False.
        """
        self.calc_dir = calc_dir
        self.nlayer = nlayer
        self.signaturename = signaturename
        self.signaturevalue = signaturevalue
        self.removeenergydensity = remove_energy_density
        self.i_en_path = (calc_dir / 'en_path.out').is_file()
        self.i_en_dens = (calc_dir / 'energy_density_end.dat').is_file()
        self.i_forcemep = (calc_dir / 'force_mep.txt').is_file()

    def __call__(self) -> pd.DataFrame:
        r"""
        Calls the summarize process
        """
        d = {self.signaturename: self.signaturevalue}
        d.update(self.forcemep())
        d.update(self.enpathout())
        d.update(self.endensity())
        return pd.DataFrame([d], index=[self.signaturevalue])

    def forcemep(self) -> Dict[str, Union[float,int]]:
        r"""
        Returns:
            the steps necessary for the convergence
            the final force of the gneb calculation. Can be used as measure for convergence
        """
        if self.i_forcemep:
            for line in reversed(open(str(self.calc_dir / 'force_mep.txt')).readlines()):
                L = line.split()
                break
            steps = int(L[0])
            force = float(L[1])
        else:
            steps = None
            force = None
        return {'steps': steps, 'force': force}


    def endensity(self):
        r"""
        Reads the energy_density_end.dat file if the energy density file exists

        Returns:
            a dictionary containing the sum of the energy contributions for each layer for each image of the path
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

        imnr= []
        for f in os.listdir(str(self.calc_dir)):
            if str(f).startswith('energy_density_end'):
                pass
            elif str(f).startswith('energy_density_'):
                imnr.append(int(str(f)[15:-4]))

        endict = {}
        for (idx, zl) in enumerate(z_layer):
            ex_intra, ex_inter, dmi, ani, zee, dip, biq, four, tot = [], [], [], [], [], [], [], [], []
            for nr in imnr:
                df = pd.read_csv(self.calc_dir / f'energy_density_{nr}.dat', sep=r'\s+', index_col=False)
                df.columns = ['x', 'y', 'z', 'ex_intra', 'ex_inter', 'dmi', 'ani', 'zee', 'dip', 'biq', 'four', 'tot']
                dfl = df[df['z'] == zl]
                ex_intra.append(dfl.ex_intra.sum())
                ex_inter.append(dfl.ex_inter.sum())
                dmi.append(dfl.dmi.sum())
                ani.append(dfl.ani.sum())
                zee.append(dfl.zee.sum())
                dip.append(dfl.dip.sum())
                biq.append(dfl.biq.sum())
                four.append(dfl.four.sum())
                tot.append(dfl.tot.sum())

            ex_intra = np.array(ex_intra) - ex_intra[0]
            ex_inter = np.array(ex_inter) - ex_inter[0]
            dmi = np.array(dmi) - dmi[0]
            ani = np.array(ani) - ani[0]
            zee = np.array(zee) - zee[0]
            dip = np.array(dip) - dip[0]
            biq = np.array(biq) - biq[0]
            four = np.array(four) - four[0]
            tot = np.array(tot) - tot[0]

            endict[f'ex_intra_lay{idx}'] = ex_intra
            endict[f'ex_inter_lay{idx}'] = ex_inter
            endict[f'dmi_lay{idx}'] = dmi
            endict[f'ani_lay{idx}'] = ani
            endict[f'zee_lay{idx}'] = zee
            endict[f'dip_lay{idx}'] = dip
            endict[f'biq_lay{idx}'] = biq
            endict[f'four_lay{idx}'] = four
            endict[f'tot_lay{idx}'] = tot

        if self.removeenergydensity:
            remove_element(self.calc_dir / 'energy_density_end.dat')
            for nr in imnr:
                remove_element(self.calc_dir / f'energy_density_{nr}.dat')
        return endict

    def enpathout(self) -> Dict[str, Union[np.ndarray, int, None]]:
        r"""
        Inspects en_path.out of all parts of the path

        Returns:
            A nested dict: R, E, dE as well as the saddlepoint
        """
        if not self.i_en_path:
            return {'R': None, 'E': None, 'dE': None}
        df = pd.read_csv(self.calc_dir / 'en_path.out', sep=r'\s+', usecols=[0, 1, 2], names=['R', 'E', 'dE'],
                            index_col=False)

        r = df['R'].to_numpy()
        dE = df['dE'].to_numpy()
        E = df['E'].to_numpy()

        r_sp = r[E == np.max(E)]
        E_sp = np.max(E)
        return {'R': r, 'E': E, 'dE': dE, 'R_sp': r_sp, 'E_sp': E_sp}