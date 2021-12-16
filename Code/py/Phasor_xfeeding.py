#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 16:08:36 2021

@author: sltg
"""

import os
import pandas as pd

import utils.flimfiles as flim




df_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Processed/df_xfeed_flim.csv'
dir_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/FLIM/single_cell/cross-feeding'

df = pd.DataFrame()

for root, dirs, files in os.walk(dir_path):
    for file in files:
        if 'R64' in file or 'r64' in file:
            full_path = root + '/' + file
            temp_df = flim.get_ref(full_path)
            if 'aerobic' in root:
                temp_df['oxygen_level'] = 'aerobic'
            elif 'hypoxic' in root:
                temp_df['oxygen_level'] = 'hypoxic'
            else:
                temp_df['oxygen_level'] = 'hypoxic'
                
            if '24h' in root:
                temp_df['time'] = '24h'
            elif '72h' in root:
                temp_df['time'] = '72h'
            else:
                temp_df['time'] = ''
                
            df = df.append(temp_df)
        
        
  
df.to_csv(df_path)
