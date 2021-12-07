#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 14:18:13 2021

@author: sltg
"""
import os


import lfdfiles
import numpy as np
import pandas as pd



def get_ref(path):
    """
    Grab g1, s1 and g2, s2 from .R64 file 

    Parameters
    ----------
    path : <str>
        full path to ref file

    Returns
    -------
    <pandas df>

    """
    
    """
    SimFCS R64 files contain referenced fluorescence lifetime images.
    The data are stored as a zlib deflate compressed stream of one int32
    (defining the image size in x and y dimensions) and five square float32
    images:
    0) dc - intensity
    1) ph1 - phase of 1st harmonic
    2) md1 - modulation of 1st harmonic
    3) ph2 - phase of 2nd harmonic
    4) md2 - modulation of 2nd harmonic
    Phase values are in degrees, the modulation values are normalized.
    Phase and modulation values may be NaN.
    """
    
    
    if os.path.splitext(path)[1].lower() == '.r64':
        with lfdfiles.SimfcsR64(path) as f:
            dc = f.asarray()[0, 2:253, 2:253]        
            s1=f.asarray()[2,2:253,2:253]*np.sin(np.radians(f.asarray()[1,2:253,2:253]))
            g1=f.asarray()[2,2:253,2:253]*np.cos(np.radians(f.asarray()[1,2:253,2:253]))
            s2=f.asarray()[4,2:253,2:253]*np.sin(np.radians(f.asarray()[3,2:253,2:253]))
            g2=f.asarray()[4,2:253,2:253]*np.cos(np.radians(f.asarray()[3,2:253,2:253]))
            df = pd.DataFrame() 
            df['s1']= s1.flatten()
            df['g1'] = g1.flatten()
            df['s2'] = s2.flatten()
            df['g2'] = g2.flatten()
            df['dc'] = dc.flatten()
            df.insert(0, "FileName", path)
            
            return df
          
            
          
def plot_phasor(s, g):
    """
    Make a phasor plot 
    
    ----------
    s : TYPE
        DESCRIPTION.
    g : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    H=np.histogram2d(s,g,bins=256,range=[[0,1],[0,1]])
    fig,ax=plt.subplots()
    plt.pcolormesh(H[1], H[2], np.log(H[0]),zorder=0)
    circ=plt.Circle((0.5,0),radius=0.5,color='black',fill=False,zorder=10)
    plt.gcf().gca().add_artist(circ)
    plt.show()
