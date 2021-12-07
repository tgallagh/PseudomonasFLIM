#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 14:15:33 2021

@author: sltg
"""

import os
import pandas as pd

import utils.flimfiles as flim




df_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/Processed/df_fig2_flim.csv'
dir_path = '/Users/sltg/Documents/GitHub/PseudomonasFLIM/Data/FLIM/references/'


df = pd.DataFrame()
for file in os.listdir(dir_path):
    if 'R64' or 'r64' in file:
        path = dir_path + file
        temp_df = flim.get_ref(path)
        df = df.append(temp_df)
        
        
df.to_csv(df_path)
