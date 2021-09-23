# -*- coding: utf-8 -*-

# Package import
from autotrader.lib.indicators import supertrend, candles_between_crosses
from finta import TA
import numpy as np

class SuperTrendScan:
    """
    Supertrend Signal Generator
    -----------------------------
    The code below was developed for detecting trends using the SuperTrend
    indicator. You can read more about it at:
        https://kieran-mackle.github.io/AutoTrader/blog
        
    This is a revised version, which will provide signals for a specified period
    after they are first recieved. This will allow manual running of the script 
    to pick up trends a few periods later than initially intended.
    """
    
    def __init__(self, params, data, instrument):
        ''' Initialise strategy indicators '''
        self.name   = "SuperTrend"
        self.data   = data
        self.params = params
        
        ema200 = TA.EMA(data, params['ema_period'])
        st_df  = supertrend(data, period = 12, ATR_multiplier = 2)
        
        
        self.signals = np.zeros(len(data))
        for i in range(len(self.signals)):
            if data.Close[i] > ema200[i] and \
            st_df.trend[i] == 1 and \
            st_df.trend[i-1] == -1:
                # Start of uptrend
                self.signals[i] = 1
            
            elif data.Close[i] < ema200[i] and \
            st_df.trend[i] == -1 and \
            st_df.trend[i-1] == 1:
                # Start of downtrend
                self.signals[i] = -1
    
        # Candles since last signal
        self.candles_since_signal = candles_between_crosses(self.signals)
    
    def generate_signal(self, i, current_position):
        ''' Generate long and short signals based on SuperTrend Indicator '''
        
        order_type  = 'market'
        signal_dict = {}

        if self.signals[i] == 1 and self.candles_since_signal < self.params['candle_tol']:
            # Start of uptrend
            signal = 1
        
        elif self.signals[i] == -1 and self.candles_since_signal < self.params['candle_tol']:
            # Start of downtrend
            signal = -1
        
        else:
            signal = 0
        
        # Construct signal dictionary
        signal_dict["order_type"]   = order_type
        signal_dict["direction"]    = signal
        
        return signal_dict