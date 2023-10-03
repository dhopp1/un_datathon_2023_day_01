import pandas as pd
import requests
from bs4 import BeautifulSoup

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