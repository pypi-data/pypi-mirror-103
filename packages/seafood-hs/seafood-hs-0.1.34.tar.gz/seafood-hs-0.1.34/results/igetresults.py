# -*- coding: utf-8 -*-
r"""
Abstract class for getting results
"""
from abc import ABC, abstractmethod
import pandas as pd


class IResults(ABC):
    r"""
    abstract class for getting results of spinD calculations
    """

    @abstractmethod
    def __call__(self) -> pd.DataFrame:
        r"""
        calls the result-getting process
        """
