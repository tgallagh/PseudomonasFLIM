#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 16:08:36 2021

@author: sltg
"""

import os
import pandas as pd

import utils.flimfiles as flim


df_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Processed/df_biofilm_flim.csv'
dir_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/FLIM/biofilm/'

df = pd.DataFrame()

for root, dirs, files in os.walk(dir_path):
    for file in files:
        if 'R64' in file or 'r64' in file:
            full_path = root + '/' + file
            temp_df = flim.get_ref(full_path)
            if 'phzko_ASM' in root:
                temp_df['condition'] = 'phzko_ASM'
            elif 'phzko_M9s' in root:
                temp_df['condition'] = 'phzko_M9suc'
            elif 'WT_ASM' in root:
                temp_df['condition'] = 'WT_ASM'
            else:
                temp_df['condition'] = 'WT_M9suc'
                
            if 'plate1' in root:
                temp_df['plate'] = 'plate1'
            elif 'plate2' in root:
                temp_df['plate'] = 'plate2'
            elif 'plate3' in root:
                temp_df['plate'] = 'plate3'
                
            df = df.append(temp_df)
        
        
  
df.to_csv(df_path)
