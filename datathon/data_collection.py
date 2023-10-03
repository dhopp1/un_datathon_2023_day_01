from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests
import yahoo_fin.stock_info as si

def get_oecd(url):
    """
    OECD api call
    parameters:
        :url: SDMX url
    output:
        :pd.DataFrame: result of the SDMX call
    """    
    r = requests.get(url)
    xml_content = BeautifulSoup(r.content, "xml")
    
    row_counter = 0
    for series in xml_content.find("DataSet").find_all("Series"):
        # non-value columns
        col_counter = 0
        for value in series.find_all("Value"):
            tmp_df = pd.DataFrame({
                value.get("concept"): value.get("value")
            }, index = [0])
            
            if col_counter == 0:
                col_df = tmp_df
            else:
                col_df = pd.concat([col_df, tmp_df], axis = 1)
            col_counter += 1
        
        # actual values
        value_counter = 0
        for value in series.find_all("Obs"):
            tmp_df = pd.DataFrame({
                "obsTime": value.text,
                "obsValue": float(value.find_all("ObsValue")[0].get("value"))
            }, index = [0])
            
            if value_counter == 0:
                value_df = tmp_df
            else:
                value_df = pd.concat([value_df, tmp_df], axis = 0, ignore_index = True)
            value_counter += 1
            
        # constructing final dataframe
        series_df = value_df
        for col in col_df.columns:
            series_df[col] = col_df[col].values[0]
            
        if row_counter == 0:
            row_df = series_df
        else:
            row_df = pd.concat([row_df, series_df], axis = 0, ignore_index = True)
        row_counter += 1
        
        # move obsTime and obsValue to end
        move_to_end = ["obsTime", "obsValue"]
        row_df = row_df.loc[:, [x for x in row_df.columns if x not in move_to_end] + move_to_end]
    return row_df


def currency_convert(series, curr_from = "RUB", curr_to = "USD"):
    """
    Convert a series from one currency to another
    parameters:
        :series: pd.Series, series with the index set to the date
        :curr_from: String, 3-letter code for the series to convert from
        :curr_to: String, 3-letter code for the series to convert to
    output:
        :pd.DataFrame: result of the SDMX call
    """    
    symbol = f"{curr_from}{curr_to}=X"
    ex_rates = [si.get_data(symbol, interval="1mo", start_date = series.index[i], end_date = series.index[i] + relativedelta(day=31)).close.values[0] for i in range(len(series))]
    converted_values = [series.values[i][0] * ex_rates[i] for i in range(len(series))]
    return converted_values