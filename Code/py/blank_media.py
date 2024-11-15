#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 16:08:36 2021

@author: sltg
"""

import os
import pandas as pd
import sys

flim_path = "/Users/sltg/Documents/GitHub/PseudomonasFLIM/Code/py/"
sys.path.append(flim_path)

import utils.flimfiles as flim



df_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Processed/df_blank_media_flim.csv'
dir_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/FLIM/blank_media/'

df = pd.DataFrame()

for root, dirs, files in os.walk(dir_path):
    for file in files:
        if 'R64' in file or 'r64' in file:
            full_path = root + '/' + file
            temp_df = flim.get_ref(full_path)
            if 'ASM' in root:
                temp_df['condition'] = 'blank_ASM'
            elif 'M9' in root:
                temp_df['condition'] = 'blank_M9'
                
            df = pd.concat( [temp_df, df] )
        
        
  
df.to_csv(df_path)
