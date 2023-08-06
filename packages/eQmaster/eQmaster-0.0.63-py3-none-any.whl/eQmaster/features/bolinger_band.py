import pandas

def bolinger_band(dataframe=None, label='Close', multiplier=2, period=14):

    try:
        if dataframe is None:
            raise Exception('dataframe is empty')
        
        if label not in dataframe.columns:
            raise Exception('Close column is required but is not found.')
        
        dataframe['UpperBand'] = dataframe[label].rolling(period).mean() + dataframe[label].rolling(period).std() * multiplier
        dataframe['LowerBand'] = dataframe[label].rolling(period).mean() - dataframe[label].rolling(period).std() * multiplier

        return dataframe

    except Exception as ex:
        print(f'[ERROR]: {ex}')
        return None
