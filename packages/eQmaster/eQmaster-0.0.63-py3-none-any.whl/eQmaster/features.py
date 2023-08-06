import pandas 

def bolinger_band(dataframe, period=20, multiplier=2):

    try:
        if dataframe is None:
            return None

        

    except Exception as ex:
        print(ex)
        return None