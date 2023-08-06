# -*- coding: utf-8 -*-
r"""
Class responsible for calculating in plane translational volumes of spin lattices.
"""
from typing import List

from python3.magnetisations import MultiLayer
from python3.propertyfunctions import zero_mode_partitionfunction
from STMutilities.goldstone.ivolume import IVolume
from pathlib import Path


class CTranslationVol(IVolume):
    r"""
    Class responsible for calculating in plane translational volumes of spin lattices. The inner methods used are taken
    from the userlib-spinD
    """

    def __init__(self, STMfile: Path) -> None:
        r"""
        Initializes the calculation of the translation volume

        Args:
            STMfile(Path): path to file with STM spin configuration
        """
        self._STMfile = STMfile
        self._ML = MultiLayer(path=str(self.STMfile))

    @property
    def STMfile(self) -> Path:
        r"""
        Returns:
             the path of the STM-file
        """
        return self._STMfile

    def __call__(self) -> List[float]:
        r"""
        Calls the zero_mode_partitionfunction from the userlib-spinD

        Returns:
            the translation mode volumes for each layer
        """
        vols = []
        for layer in self._ML.Layer:
            vols.append(zero_mode_partitionfunction(SL=layer,mode='translation'))
        return vols
    
    @property
    def ML(self) -> MultiLayer:
        r"""
        Returns:
            The magnetization read from the STM file. If the system is a monolayer the SL is accesible through the
            ML.layer[0] attribute.
        """
        return self._ML
