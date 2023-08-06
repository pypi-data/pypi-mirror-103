# -*- coding: utf-8 -*-
r"""
Abstract class for the calculation of a volume of a goldstone mode. Possible examples are rotational modes for Skyrmions
or Antiskyrmions without DMI or the skyrmion or saddlepoint translation modes.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union
from python3.magnetisations import MultiLayer

class IVolume(ABC):
    r"""
    abstract base class for goldstone mode volume calculations for a given STMfile.
    """

    @property
    @abstractmethod
    def STMfile(self) -> Path:
        r"""
        Returns:
             the path of the STM-file
        """

    @abstractmethod
    def __call__(self) -> List[float]:
        r"""
        Returns:
            the goldstone mode volume for all layers in the spin configuration in the STMfile with increasing z-
            component
        """

    @property
    @abstractmethod
    def ML(self) -> MultiLayer:
        r"""
        Returns:
            The magnetization read from the STM file. If the system is a monolayer the SL is accesible through the
            ML.layer[0] attribute.
        """
