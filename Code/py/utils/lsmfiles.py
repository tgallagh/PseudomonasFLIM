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
        return df
    else:
        raise Exception(f"Does not exist: {path}")


def channels(path):
    """
    Get channels from lsm file

    Parameters
    ----------
    path : <str>
        path to lsm

    Returns
    -------
    channels: <list of strs> 
        channels obbject 
    wavelen: <list of ints> 
        spectral wavelengths

    """
    tif =  tiff.TiffFile(path)
    channels = tif.lsm_metadata['ChannelColors']['ColorNames']
    wavelen = list()
    for x in channels:
        try: 
            int(x)
            wavelen.append(int(x))
        except:
            pass
    return channels, wavelen
    
    
def frame_sum(df):
    """
    Get channels from lsm file

    Parameters
    ----------
    df : <numpy array>
        Df of lsm data
    
    channels: <list>
        list of ints of wavelengths 
        

    Returns
    -------
    df <numpy array>
        collapsed to get sum across entire image frame

    """
    # sum across
    #df = np.sum(df[0,0,:,:,:],2)
    df = np.sum(df[:,:,:],2)
    
    # sum down 
    df = np.sum(df, 1)
    return df 


def scale(df, wavelen):
    """
    scale spectral data to get fraction out of 1 
    
    
    Parameters
    ----------
    df : <numpy array>
        df of spectral data summed across frame
    
    channels: <list>
        list of channels from lsm

    Returns
    -------
    df <pandas df>
        normalized to 1 
    
    
    """
    # keep fl. measurements for wavelengths
    df = df[0:len(wavelen)]
    df = pd.DataFrame(df)
    df = df.rename(columns={0:"Intensity"})
    df.insert(1, "Normalized", df.Intensity/max(df.Intensity))
    df.insert(0, "Wavelength", wavelen)
    return df



    
    

    


