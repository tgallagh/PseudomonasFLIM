#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 12:44:33 2021

@author: sltg
"""

import utils.lsmfiles as lsmfiles
import os
import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt   
import pandas as pd 
import seaborn as sns


# grab lsm files
# 
dyes_dir = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Spectral/Dyes/OhPhz/'
output_dir = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Output/Exploratory/'
semrock_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Microscope/emission_filters/semrock_filter.csv'

spec_df = pd.DataFrame()
for file in os.listdir(dyes_dir):
    if 'lsm' in file:
        path = dyes_dir + file
        df = lsmfiles.get_lsm(path)
        spectra, wavelen = lsmfiles.channels(path)
        df = lsmfiles.frame_sum(df)
        df = lsmfiles.scale(df, wavelen)
        df.insert(0, "FileName", file)
        spec_df = spec_df.append(df)
        

# this is the diver emission filter bandwidth 
semrock_filter=pd.read_csv(semrock_path)
semrock_filter.insert(2, "Normalized", semrock_filter.Intensity/sum(semrock_filter.Intensity))
semrock_filter=semrock_filter.drop(columns="Wavelength")
semrock_filter.insert(0, "Wavelength", wavelen)
semrock_filter.Wavelength.astype("int")


# Set figure size with matplotlib
current_palette = sns.color_palette("Paired", 10)
plt.figure(figsize=(10,6))
plt.stackplot(semrock_filter["Wavelength"], semrock_filter["Normalized"], alpha=0.3, colors=["#999999"])
sns.lineplot(x="Wavelength", y="Normalized", hue="FileName", data=spec_df)
plt.savefig(output_dir+'ohphz.pdf', dpi=300)

current_palette = sns.color_palette("Paired", 10)
plt.figure(figsize=(10,6))
plt.stackplot(semrock_filter["Wavelength"], semrock_filter["Normalized"]*1000000, alpha=0.3, colors=["#999999"])
sns.lineplot(x="Wavelength", y="Intensity", hue="FileName", data=spec_df)
plt.savefig(output_dir+'ohphz_raw.pdf', dpi=300)

