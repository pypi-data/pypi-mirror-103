# -*- coding: utf-8 -*-
r"""
Gets and summarizes the results of a short gneb calculation. Normally those calc. are not converged. They can be used
to identify intermediate minima in the path.
"""
import pandas as pd
import numpy as np
from results.igetresults import IResults
from pathlib import Path
from typing import Union, List, Tuple, Dict
from python3.magnetisations import SpinLattice, MultiLayer
from scipy.signal import argrelextrema

from otterplot.model.cotterplotter import COtterPlotter
import matplotlib.pyplot as plt

class IGNShortGneb(IResults):
    r"""

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
        self.i_en_path = (calc_dir / 'en_path.out').is_file()

    def __call__(self) -> pd.DataFrame:
        r"""
        """
        self.enpathout()

    def enpathout(self) -> None:
        r"""
        Inspects en_path.out. There are three quantities of interest. We can check the total energy for intermediate
        minima.
        """
        df = pd.read_csv(self.calc_dir / 'en_path.out', sep=r'\s+', usecols=[0,1,2], names=['R', 'E', 'dE'], index_col=False)
        R = df['R'].to_numpy()
        intermediate_imagenr = argrelextrema(R, np.less)[0] + 1

        otter=COtterPlotter(plotmode='paperPRB')
        ax=otter.axes[0]
        ax.plot(df['R'],df['E'],'ko',linestyle='none')
        ax.plot(df['R'].to_numpy()[intermediate_imagenr-1],df['E'].to_numpy()[intermediate_imagenr-1], marker='s',markerfacecolor='none')
        plt.show()
