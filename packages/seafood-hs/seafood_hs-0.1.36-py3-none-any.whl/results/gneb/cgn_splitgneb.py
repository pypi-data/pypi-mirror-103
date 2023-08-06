# -*- coding: utf-8 -*-
r"""
Gets and summarizes the results of a split gneb calculation.
"""
import pandas as pd
import numpy as np
from results.igetresults import IResults
from pathlib import Path
from typing import Union, List, Tuple, Dict
from python3.magnetisations import SpinLattice, MultiLayer
from python3.shell_commands import *
from scipy.signal import argrelextrema
import os


class CGNSplitGneb(IResults):
    r"""
    Summarizes the results of a split GNEB calculation
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
        if nlayer != 2:
            raise NotImplementedError('other number of layers than 2 is not implemented')
        self.nlayer = nlayer
        self.signaturename = signaturename
        self.signaturevalue = signaturevalue
        self.removeenergydensity = remove_energy_density
        self.i_en_path_im = (calc_dir / 'im' / 'en_path.out').is_file()
        self.i_en_path_mf = (calc_dir / 'mf' / 'en_path.out').is_file()
        self.i_en_dens_im = (calc_dir / 'im' / 'energy_density_end.dat').is_file()
        self.i_en_dens_mf = (calc_dir / 'mf' / 'energy_density_end.dat').is_file()
        self.i_forcemep_im = (calc_dir / 'im' / 'force_mep.txt').is_file()
        self.i_forcemep_mf = (calc_dir / 'mf' / 'force_mep.txt').is_file()

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
        if self.i_forcemep_im:
            for line in reversed(open(str(self.calc_dir / 'im' / 'force_mep.txt')).readlines()):
                L_im = line.split()
                break
            steps_im = int(L_im[0])
            force_im = float(L_im[1])
        else:
            steps_im = None
            force_im = None
        if self.i_forcemep_mf:
            for line in reversed(open(str(self.calc_dir / 'mf' / 'force_mep.txt')).readlines()):
                L_mf = line.split()
                break
                steps_mf = int(L_mf[0])
                force_mf = float(L_mf[1])
        else:
            steps_mf = None
            force_mf = None
        return {'steps_im': steps_im, 'force_im': force_im,
                'steps_mf': steps_mf, 'force_mf': force_mf}


    def endensity(self):
        r"""
        Reads the energy_density_end.dat file if the energy density file exists

        Returns:
            a dictionary containing the sum of the energy contributions for each layer for each image of the path
        """
        if not all[self.i_en_dens_im, self.i_en_dens_mf]:
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
        df = pd.read_csv(self.calc_dir / 'im' / 'energy_density_end.dat', sep=r'\s+', index_col=False)
        df.columns = ['x', 'y', 'z', 'ex_intra', 'ex_inter', 'dmi', 'ani', 'zee', 'dip', 'biq', 'four', 'tot']
        z_layer = df.z.unique()

        imnr_im, imnr_mf = [], []
        for f in os.listdir(str(self.calc_dir / 'im')):
            if str(f).startswith('energy_density_end'):
                pass
            elif str(f).startswith('energy_density_'):
                imnr_im.append(int(str(f)[15:-4]))
        for f in os.listdir(str(self.calc_dir / 'mf')):
            if str(f).startswith('energy_density_end'):
                pass
            elif str(f).startswith('energy_density_'):
                imnr_mf.append(int(str(f)[15:-4]))

        endict = {}
        for (idx, zl) in enumerate(z_layer):
            ex_intra_im, ex_inter_im, dmi_im, ani_im, zee_im, dip_im, biq_im, four_im, tot_im = [], [], [], [],\
                                                                                                [], [], [], [], []
            for nr in imnr_im:
                df = pd.read_csv(self.calc_dir / 'im' / f'energy_density_{nr}.dat', sep=r'\s+', index_col=False)
                df.columns = ['x', 'y', 'z', 'ex_intra', 'ex_inter', 'dmi', 'ani', 'zee', 'dip', 'biq', 'four', 'tot']
                dfl = df[df['z'] == zl]
                ex_intra_im.append(dfl.ex_intra.sum())
                ex_inter_im.append(dfl.ex_inter.sum())
                dmi_im.append(dfl.dmi.sum())
                ani_im.append(dfl.ani.sum())
                zee_im.append(dfl.zee.sum())
                dip_im.append(dfl.dip.sum())
                biq_im.append(dfl.biq.sum())
                four_im.append(dfl.four.sum())
                tot_im.append(dfl.tot.sum())
            ex_intra_mf, ex_inter_mf, dmi_mf, ani_mf, zee_mf, dip_mf, biq_mf, four_mf, tot_mf = [], [], [], [], \
                                                                                                [], [], [], [], []
            for nr in imnr_mf:
                df = pd.read_csv(self.calc_dir / 'mf' / f'energy_density_{nr}.dat', sep=r'\s+', index_col=False)
                df.columns = ['x', 'y', 'z', 'ex_intra', 'ex_inter', 'dmi', 'ani', 'zee', 'dip', 'biq', 'four', 'tot']
                dfl = df[df['z'] == zl]
                ex_intra_mf.append(dfl.ex_intra.sum())
                ex_inter_mf.append(dfl.ex_inter.sum())
                dmi_mf.append(dfl.dmi.sum())
                ani_mf.append(dfl.ani.sum())
                zee_mf.append(dfl.zee.sum())
                dip_mf.append(dfl.dip.sum())
                biq_mf.append(dfl.biq.sum())
                four_mf.append(dfl.four.sum())
                tot_mf.append(dfl.tot.sum())

            ex_intra_im = np.array(ex_intra_im) - ex_intra_im[0]
            ex_inter_im = np.array(ex_inter_im) - ex_inter_im[0]
            dmi_im = np.array(dmi_im) - dmi_im[0]
            ani_im = np.array(ani_im) - ani_im[0]
            zee_im = np.array(zee_im) - zee_im[0]
            dip_im = np.array(dip_im) - dip_im[0]
            biq_im = np.array(biq_im) - biq_im[0]
            four_im = np.array(four_im) - four_im[0]
            tot_im = np.array(tot_im) - tot_im[0]

            ex_intra_mf = np.array(ex_intra_mf) - ex_intra_mf[0] + ex_intra_im[-1]
            ex_inter_mf = np.array(ex_inter_mf) - ex_inter_mf[0] + ex_inter_im[-1]
            dmi_mf = np.array(dmi_mf) - dmi_mf[0] + dmi_im[-1]
            ani_mf = np.array(ani_mf) - ani_mf[0] + ani_im[-1]
            zee_mf = np.array(zee_mf) - zee_mf[0] + zee_im[-1]
            dip_mf = np.array(dip_mf) - dip_mf[0] + dip_im[-1]
            biq_mf = np.array(biq_mf) - biq_mf[0] + biq_im[-1]
            four_mf = np.array(four_mf) - four_mf[0] + four_im[-1]
            tot_mf = np.array(tot_mf) - tot_mf[0] + tot_im[-1]


            endict[f'ex_intra_lay{idx}'] = np.concatenate((ex_intra_im, ex_intra_mf))
            endict[f'ex_inter_lay{idx}'] = np.concatenate((ex_inter_im, ex_inter_mf))
            endict[f'dmi_lay{idx}'] = np.concatenate((dmi_im, dmi_mf))
            endict[f'ani_lay{idx}'] = np.concatenate((ani_im, ani_mf))
            endict[f'zee_lay{idx}'] = np.concatenate((zee_im, zee_mf))
            endict[f'dip_lay{idx}'] = np.concatenate((dip_im, dip_mf))
            endict[f'biq_lay{idx}'] = np.concatenate((biq_im, biq_mf))
            endict[f'four_lay{idx}'] = np.concatenate((four_im, four_mf))
            endict[f'tot_lay{idx}'] = np.concatenate((tot_im, tot_mf))

        if self.removeenergydensity:
            remove_element(self.calc_dir / 'im' / 'energy_density_end.dat')
            remove_element(self.calc_dir / 'mf' / 'energy_density_end.dat')
            for nr in imnr_im:
                remove_element(self.calc_dir / 'im' / f'energy_density_{nr}.dat')
            for nr in imnr_mf:
                remove_element(self.calc_dir / 'mf' / f'energy_density_{nr}.dat')

        return endict

    def enpathout(self) -> Dict[str, Union[np.ndarray, int, None]]:
        r"""
        Inspects en_path.out of all parts of the path

        Returns:
            A nested dict: R, E, dE connected at the intermediate minimum
        """
        if not all[self.i_en_path_im,self.i_en_path_mf]:
            return {'R': None, 'E': None, 'dE': None}
        df_im = pd.read_csv(self.calc_dir / 'im' / 'en_path.out', sep=r'\s+', usecols=[0, 1, 2], names=['R', 'E', 'dE'],
                            index_col=False)
        df_mf = pd.read_csv(self.calc_dir / 'mf' / 'en_path.out', sep=r'\s+', usecols=[0, 1, 2], names=['R', 'E', 'dE'],
                            index_col=False)

        r_im = df_im['R'].to_numpy()
        r_mf = df_mf['R'].to_numpy()
        r_mf = r_mf + r_im[-1]
        r = np.concatenate((r_im, r_mf))
        dE = np.concatenate((df_im['dE'].to_numpy(), df_mf['dE'].to_numpy()))
        E_im = df_im['E'].to_numpy()
        E_mf = df_mf['E'].to_numpy()
        E_mf = E_mf + E_im[-1]
        E = np.concatenate((E_im, E_mf))

        r_imsp = r_im[E_im == np.max(E_im)]
        E_imsp = np.max(E_im)
        r_mfsp = r_mf[E_im == np.max(E_mf)]
        E_mfsp = np.max(E_mf)
        return {'R': r, 'E': E, 'dE': dE, 'R_imsp': r_imsp, 'E_imsp': E_imsp, 'R_mfsp': r_mfsp, 'E_mfsp': E_mfsp}
