#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:34:57 2020

@author: Tara
"""

# make plots of zeiss LSM files containing spectral 32-channel images

# libraries

import os
import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt   
import pandas as pd 
import seaborn as sns

os.chdir('/Users/sltg/Documents/GitHub/PseudomonasFLIM/Code/py')


import utils.lsmfiles as lsmfiles

# grab lsm files
# 
dyes_dir = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Spectral/Dyes/'
output_dir = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Output/Exploratory'
semrock_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Microscope/emission_filters/semrock_filter.csv'
df_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Processed/df_fig2_spectra.csv'
df_sem_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Processed/df_fig2_semrock.csv'

spec_df = pd.DataFrame()
for file in os.listdir(dyes_dir):
    if 'lsm' in file:
        path = dyes_dir + file
        print(path)
        df = lsmfiles.get_lsm(path)
        spectra, wavelen = lsmfiles.channels(path)
        df = lsmfiles.frame_sum(df)
        df = lsmfiles.scale(df, wavelen)
        df.insert(0, "FileName", file)
        spec_df = pd.concat( [spec_df, df] )
        

#spec_df.FileName.astype("category")
spec_df.insert(0,"Sample",spec_df.FileName)
spec_df.Sample[spec_df.Sample.str.contains("PCH")]="PCH"
spec_df.Sample[spec_df.Sample.str.contains("NADH")]="Free NADH"
spec_df.Sample[spec_df.Sample.str.contains("PYO")]="Reduced PYO"
spec_df.Sample[spec_df.Sample.str.contains("CPX")]="CPX"
spec_df.Sample[spec_df.Sample.str.contains("FAD")]="FAD"
spec_df.Sample[spec_df.Sample.str.contains("PVD")]="PVD"
spec_df.Sample[spec_df.Sample.str.contains("OHPhz")]="Reduced OHPhz"

# this is the diver emission filter bandwidth 
semrock_filter=pd.read_csv(semrock_path)
semrock_filter.insert(2, "Normalized", semrock_filter.Intensity/max(semrock_filter.Intensity))
semrock_filter=semrock_filter.drop(columns="Wavelength")
semrock_filter.insert(0, "Wavelength", wavelen)
semrock_filter.Wavelength.astype("int")


# Set figure size with matplotlib
current_palette = sns.color_palette("Paired", 10)
plt.figure(figsize=(10,6))
plt.stackplot(semrock_filter["Wavelength"], semrock_filter["Normalized"], alpha=0.3, colors=["#999999"])
sns.lineplot(x="Wavelength", y="Normalized", hue="Sample", data=spec_df[spec_df.Sample!="Pyochelin"])
#plt.savefig(output_dir+'fig2.pdf', dpi=300)

# output dataframe for generating plots in R
spec_df.to_csv(df_path)
semrock_filter.to_csv(df_sem_path)

# get pca data
pca_dir = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Spectral/Dyes/PCA/'
pca_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Processed/df_pca_spectra.csv'


spec_df = pd.DataFrame()
for file in os.listdir(pca_dir):
    if 'lsm' in file:
        path = pca_dir + file
        df = lsmfiles.get_lsm(path)
        spectra, wavelen = lsmfiles.channels(path)
        df = lsmfiles.frame_sum(df)
        df = lsmfiles.scale(df, wavelen)
        df.insert(0, "FileName", file)
        spec_df = pd.concat( [spec_df, df] )
        

spec_df.insert(0,"Sample",spec_df.FileName)
spec_df.Sample[spec_df.Sample.str.contains("PCA")]="PCA"

spec_df.to_csv(pca_path)


# get pcn data
pcn_dir = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Spectral/Dyes/PCN/'
pcn_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Processed/df_pcn_spectra.csv'


spec_df = pd.DataFrame()
for file in os.listdir(pcn_dir):
    if 'lsm' in file:
        path = pcn_dir + file
        df = lsmfiles.get_lsm(path)
        spectra, wavelen = lsmfiles.channels(path)
        df = lsmfiles.frame_sum(df)
        df = lsmfiles.scale(df, wavelen)
        df.insert(0, "FileName", file)
        spec_df = pd.concat( [spec_df, df] )
   

spec_df.insert(0,"Sample",spec_df.FileName)
spec_df.Sample[spec_df.Sample.str.contains("PCN")]="PCN"

spec_df.to_csv(pcn_path)



 ### get oh phz data
 
ohphz_dir = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Spectral/Dyes/OhPhz/'
ohphz_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Processed/df_ohphz_spectra.csv'

spec_df = pd.DataFrame()
for file in os.listdir(ohphz_dir):
    if 'lsm' in file:
        path = ohphz_dir + file
        df = lsmfiles.get_lsm(path)
        spectra, wavelen = lsmfiles.channels(path)
        df = lsmfiles.frame_sum(df)
        df = lsmfiles.scale(df, wavelen)
        df.insert(0, "FileName", file)
        spec_df = pd.concat( [spec_df, df] )
        
spec_df.to_csv(ohphz_path)



# get electrochemical red data

ec_dir = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Spectral/pyo_electrode/'
ec_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Processed/df_pyo_electrode_spectra.csv'


spec_df = pd.DataFrame()
for file in os.listdir(ec_dir):
    if 'lsm' in file:
        path = ec_dir + file
        df = lsmfiles.get_lsm(path)
        spectra, wavelen = lsmfiles.channels(path)
        df = lsmfiles.frame_sum(df)
        df = lsmfiles.scale(df, wavelen)
        df.insert(0, "FileName", file)
        spec_df = pd.concat( [spec_df, df] )
   

spec_df.insert(0,"Sample",spec_df.FileName)
spec_df.Sample[spec_df.Sample.str.contains("electrochemicallyred")]="Electrochemical Red"
spec_df.Sample[spec_df.Sample.str.contains("TCEP")]="TCEP"

spec_df.to_csv(ec_path)
        
# TCEP data


tcep_dir = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Spectral/pyo_tcep_gradients/'
tcep_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Processed/df_pyo_tcep_spectra.csv'


spec_df = pd.DataFrame()
for file in os.listdir(tcep_dir):
    if 'lsm' in file:
        path = tcep_dir + file
        df = lsmfiles.get_lsm(path)
        spectra, wavelen = lsmfiles.channels(path)
        df = lsmfiles.frame_sum(df)
        df = lsmfiles.scale(df, wavelen)
        df.insert(0, "FileName", file)
        spec_df = pd.concat( [spec_df, df] )
   

spec_df.insert(0,"Sample",spec_df.FileName)

spec_df.to_csv(tcep_path)