"""
    Class Prophet:
    
    Prophet is a procedure for forecasting time series data based on 
    an additive model where non-linear 
    trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. 
    It works best with time series that have strong seasonal effects and several seasons of historical data. 
    Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.

"""

import pandas as pd
import json
import datetime

from prophet import Prophet, serialize

from utils import get_logger, LOG_LEVEL

logger = get_logger(__name__, loglevel=LOG_LEVEL)

logger.info(LOG_LEVEL)

ARTIFACT_PATH = 'mlmodel'

class Model(object):

    def __init__(self):

        self.model = None

    def run(self, dataset, period, config):

        # dataset = data.get('dataset')
        # period = data.get('period')

        # config = data.get('model_config')

        input_window = config.pop('input_window', None)
        if not input_window: raise RuntimeError('input_window is empty')
        output_window = config.pop('output_window', None)
        if not output_window: raise RuntimeError('output_window is empty')
        granularity = config.pop('granularity', None)
        if not granularity: raise RuntimeError('granularity is empty')

        if isinstance(dataset, list):
            df_dataset = self.prepare_dataset(dataset, columns=['ds', 'y'])

        if self.fit_model(df=df_dataset, config=config):

            if isinstance(period, list):
                df_period = self.prepare_dataset(period, columns=['ds'])
            else:
                df_period = self.generate_dataset(freq=granularity, periods=output_window)
            
            result = self.model.predict(df_period)     
 
            series = self.to_series(df=result)

            logger.debug(f"Series shape: ({len(series)}, {len(series[0])})")
            return series
        else:
            raise RuntimeError('Cannot fit model')

    def to_series(self, df)->list:
            
        df['ds'] = df[['ds']].apply(lambda x: x[0].timestamp(), axis=1).astype(int)

        v = df[['ds', 'yhat']].values.tolist()  

        return list(map(lambda x: [int(x[0]), x[1]], v))      
    
    def generate_dataset(self, freq=3600, periods=24)->pd.DataFrame():

        freq = f'{freq}S'

        df = Prophet.make_future_dataframe(self.model, periods, freq, include_history = False)
        logger.debug(f'generate future dataset shape: {df.shape}')

        return df

    def fit_model(self, df, config=None):
        
        if isinstance(config, dict):

            seasonality = config.pop('seasonality', None) 

            if isinstance(config, dict):
                self.model = Prophet(**config)
            else:
                self.model = Prophet()
            
            if isinstance(seasonality, list):
                [self.model.add_seasonality(**items) for items in seasonality]
        
            self.model.fit(df)

        return True

    def prepare_dataset(self, dataset, columns=None) -> pd.DataFrame:

        logger.debug(f'Prepare dataset with length: {len(dataset)}')
        df = pd.DataFrame(dataset, columns=columns)

        df['ds'] = pd.to_datetime(df['ds'], unit='ms', utc=False)
        
        df.reset_index(inplace=True, drop=True)
        
        logger.debug(df.shape)

        return df
