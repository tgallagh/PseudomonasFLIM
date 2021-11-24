#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 11:17:32 2021

@author: sltg

functions for working with LSM files

"""


import numpy as np 
import os
import pandas as pd
import tifffile as tiff



def get_lsm(path):
    """
    Read in .lsm as a df

    Parameters
    ----------
    path : <str>
        Path to lsm

    Returns
    -------
    df <pandas df> 

    """
    if os.path.exists(path):
        df = tiff.imread(path)
    else:
        raise Exception(f"Does not exist: {path}")


def channels(df):
    """
    Get number of channels from lsm df

    Parameters
    ----------
    df : <str>
        df of spectral lsm

    Returns
    -------
    <int> number of channels

    """
    if len(df.shape) == 5:
        channels = df.shape[2]
    else:
        raise Exception('Number of dimensions unexpected for spectral lsm!')
    