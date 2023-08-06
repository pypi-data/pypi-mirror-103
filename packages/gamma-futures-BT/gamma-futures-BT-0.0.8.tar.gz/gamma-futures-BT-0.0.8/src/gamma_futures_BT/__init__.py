#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import talib as ta
import numpy as np
import math
import os
from datetime import datetime
import json


    
def entry_populator(time, E1_entry, curr_High, curr_Low, direction, yest_atr, btsl, stsl, noTrade):
    global atr_mult, open_positions, pyramid_level, add_atr, capital_at_risk
    long_pos = open_positions[open_positions.type == "Long"].pyramid.max()
    short_pos = open_positions[open_positions.type == "Short"].pyramid.max()
    counter_trades = 0
    if direction == "Long":
        if math.isnan(long_pos):
            long_pos = 0
            long_df = [0] * pyramid_level
            for iter in range(pyramid_level):
                long_df[iter] = E1_entry + yest_atr * iter * add_atr
        else:
            long_df = [0] * pyramid_level
            for iter in range(pyramid_level):
                try:
                    long_df[iter] =                         open_positions[(open_positions.type == "Long") &                                        (open_positions.pyramid == (iter+1))].entry_price.values[0]
                except:
                    long_df[iter] = long_df[iter-1] + yest_atr * add_atr
        
        
        for iter_i in range(long_pos, pyramid_level):
            if long_df[iter_i] < curr_High:
                counter_trades += 1
                if noTrade == False:
                    msl = long_df[iter_i] - atr_mult * yest_atr
                    quantity = (capital_at_risk / (long_df[iter_i] - max(msl, btsl))) // lot_size

                    open_positions =                         open_positions.append(pd.DataFrame([(iter_i+1, "Long", long_df[iter_i], time, quantity, msl)],                             columns=["pyramid", "type", "entry_price", "entry_time", "quantity", "MSL"]))
                    open_positions.reset_index(inplace = True, drop = True)
                    open_positions.loc[open_positions[open_positions.type == "Long"].index, 'MSL'] = msl
        return long_df, counter_trades
        
    if direction == "Short":
        if math.isnan(short_pos):
            short_pos = 0
            short_df = [0] * pyramid_level
            for iter in range(pyramid_level):
                short_df[iter] = E1_entry - yest_atr * iter * add_atr
        else:
            short_df = [0] * pyramid_level
            for iter in range(pyramid_level):
                try:
                    short_df[iter] =                         open_positions[(open_positions.type == "Short") &                                        (open_positions.pyramid == (iter+1))].entry_price.values[0]
                except:
                    short_df[iter] = short_df[iter-1] - yest_atr * add_atr
                    

        for iter_i in range(short_pos, pyramid_level):
            if short_df[iter_i] > curr_Low:
                counter_trades += 1
                if noTrade == False:
                    msl = short_df[iter_i] + atr_mult * yest_atr
                    quantity = (capital_at_risk / (min(msl, stsl) - short_df[iter_i])) // lot_size
                    
                    open_positions =                         open_positions.append(pd.DataFrame([(iter_i+1, "Short", short_df[iter_i], time, quantity, msl)],                             columns=["pyramid", "type", "entry_price", "entry_time", "quantity", "MSL"]))
                    open_positions.reset_index(inplace = True, drop = True)
                    open_positions.loc[open_positions[open_positions.type == "Short"].index, 'MSL'] = msl
                
        return short_df, counter_trades


def check_position(time, curr_high, curr_low, btsl, stsl):
    global trade_book, open_positions
    long_existing = open_positions[open_positions.type == "Long"].index
    short_existing = open_positions[open_positions.type == "Short"].index
#     print(long_existing, short_existing)
    for iter_i in long_existing:
        fsl = max(btsl, open_positions.loc[iter_i].MSL)
        if curr_low < fsl:
            pnl = fsl - open_positions.loc[iter_i].entry_price
            pnl_t = pnl * open_positions.loc[iter_i].quantity
            trade_book =                 trade_book.append(pd.DataFrame([(open_positions.loc[iter_i].pyramid,                                                  "Long",                                                  open_positions.loc[iter_i].entry_price,                                                  open_positions.loc[iter_i].entry_time,                                                  fsl,                                                 time,                                                 open_positions.loc[iter_i].quantity,                                                 pnl,pnl_t)],                             columns=["pyramid", "type", "entry_price", "entry_time",                                      "exit_price", "exit_time", "quantity", "pnl", "pnl_t"]))
#             print(time, "Exit long", open_positions.loc[iter_i].pyramid)
            open_positions.drop(index=iter_i, inplace=True)
    
    for iter_i in short_existing:
        fsl = min(stsl, open_positions.loc[iter_i].MSL)
        if curr_high > fsl:
            pnl = -fsl + open_positions.loc[iter_i].entry_price
            pnl_t = pnl * open_positions.loc[iter_i].quantity
            trade_book =                 trade_book.append(pd.DataFrame([(open_positions.loc[iter_i].pyramid,                                                  "Short",                                                  open_positions.loc[iter_i].entry_price,                                                  open_positions.loc[iter_i].entry_time,                                                  fsl,                                                 time,                                                 open_positions.loc[iter_i].quantity,                                                 pnl, pnl_t)],                             columns=["pyramid", "type", "entry_price", "entry_time",                                      "exit_price", "exit_time", "quantity", "pnl", "pnl_t"]))
#             print(time, "Exit short", open_positions.loc[iter_i].pyramid)
            open_positions.drop(index=iter_i, inplace=True)

    open_positions.reset_index(inplace = True, drop = True)
