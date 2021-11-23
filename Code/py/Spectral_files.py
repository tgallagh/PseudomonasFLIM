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
image_stack=tiff.imread(os.listdir()[0]) # read in first file in directory
#image_stack=np.squeeze(image_stack)


image_stack.shape # shape of file
spec = np.sum(image_stack[0,0,:,:,:],2) 
spec1=np.sum(spec,1)  # contains sum intensity for each channel (1-32)
#plt.plot(wavelen,spec1[0:32])  
#plt.show()

# for loop

spec_df=pd.DataFrame()

spec_df=pd.DataFrame()
for file in os.listdir():
    image_stack=tiff.imread(file)
    spec = np.sum(image_stack[0,0,:,:,:],2) 
    spec1=np.sum(spec,1)[0:32] # 32 channels (last channel is Transmission)
    spec1=pd.DataFrame(spec1)
    spec1.insert(0, "FileName", file)
    spec_df=spec1.append(spec_df)

#spec_df.FileName.astype("category")
spec_df.insert(0,"Sample",spec_df.FileName)


spec_df.Sample=spec_df.Sample.replace("TCEP.*", "",regex=True)
spec_df.insert(1,"TCEP_conc", spec_df.Sample)
spec_df.TCEP_conc=spec_df.TCEP_conc.replace(".*_", "", regex=True)
spec_df=spec_df.rename(columns={0:"Intensity"})

spec_df.insert(4, "Wavelength",pd.Series(wavelen))


fig=sns.lineplot(x="Wavelength", y="Intensity", hue="TCEP_conc", data=spec_df)
plt.ylabel("Fluorescence emission")
plt.show(fig)
fig.savefig('/Volumes/GoogleDrive/My Drive/PseudomonasImaging/tcep_gradients.pdf', dpi=300)





