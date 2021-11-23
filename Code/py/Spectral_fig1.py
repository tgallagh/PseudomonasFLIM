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

wavelen=np.linspace(410,695,32)  # make list of wavelengths for channels 1-32
os.chdir("/Volumes/GoogleDrive/My Drive/PseudomonasImaging/Data/Spectral/Flourophores")

# for loop
background=tiff.imread("/Volumes/GoogleDrive/My Drive/PseudomonasImaging/Data/Spectral/TCEP_gradients/Blank_blank1mMTCEPblank_20p_68fov_spectral_63xOil_740nm_410-695_9nmstep_4usdwell_bidi16bitlinesum.lsm")
background = np.sum(background[0,0,:,:,:],2)
background=np.sum(background,1)[0:32]
background=pd.DataFrame(background)
background=background.rename(columns={0:"Intensity"})
background.insert(1, "Normalized", background.Intensity/sum(background.Intensity))



spec_df=pd.DataFrame()
spec_df=pd.DataFrame()
for file in os.listdir():
    image_stack=tiff.imread(file)
    spec = np.sum(image_stack[0,0,:,:,:],2) 
    spec1=np.sum(spec,1)[0:32] # 32 channels (last channel is Transmission)
    spec1=pd.DataFrame(spec1)
    spec1.insert(0, "FileName", file)
    spec1=spec1.rename(columns={0:"Intensity"})
    spec1.insert(2, "Normalized", spec1.Intensity/max(spec1.Intensity))
    spec_df=spec1.append(spec_df)

#spec_df.FileName.astype("category")
spec_df.insert(0,"Sample",spec_df.FileName)
spec_df.Sample[spec_df.Sample.str.contains("PCH")]="Pyochelin"
spec_df.Sample[spec_df.Sample.str.contains("NADH")]="Free NADH"
spec_df.Sample[spec_df.Sample.str.contains("PYO")]="Reduced Pyocyanin"
spec_df.Sample[spec_df.Sample.str.contains("CPX")]="CPX"
spec_df.Sample[spec_df.Sample.str.contains("FAD")]="FAD"
spec_df.Sample[spec_df.Sample.str.contains("PVD")]="Pyoverdine"

semrock_filter=pd.read_csv("/Volumes/GoogleDrive/My Drive/PseudomonasImaging/Data/Spectral/semrock_filter.csv")
semrock_filter.insert(2, "Normalized", semrock_filter.Intensity/max(semrock_filter.Intensity))
semrock_filter=semrock_filter.drop(columns="Wavelength")
semrock_filter.insert(0, "Wavelength", wavelen)
spec_df.insert(4, "Wavelength",pd.Series(wavelen))
semrock_filter.Wavelength.astype("int")



# Set figure size with matplotlib
current_palette = sns.color_palette("Paired", 5)
plt.figure(figsize=(10,6))

plt.stackplot(semrock_filter["Wavelength"], semrock_filter["Normalized"], alpha=0.3, colors=["#999999"])
sns.lineplot(x="Wavelength", y="Normalized", hue="Sample", style="Sample", data=spec_df[spec_df.Sample!="Pyochelin"])

 



