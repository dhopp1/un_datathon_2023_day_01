import matplotlib.pyplot as plt
import pandas as pd
### if the module is in a different directory
# import sys
# sys.path.append("path/containing/library/folder/")
from datathon.data_collection import currency_convert, get_oecd
from datathon.plotting import line_plot

# get ais data
ais = pd.read_csv("https://raw.githubusercontent.com/dhopp1/ais_russia_data/main/russian_port_data.csv", parse_dates = ["date"])
ais["date"] = pd.to_datetime([str(x)[:7] + "-01" for x in ais["date"]]) # aggregate to monthly
ais = ais.loc[:, ["date", "num_ships"]].groupby("date").sum().reset_index()

# get OECD data
end_date = "2023-08"
start_date = "2019-01"
geos = ["RUS"]; geos = "+".join(geos) # in case there are multiple geographies
dataset = "MEI_ARCHIVE"
variables = ["703"]; variables = "+".join(variables)

# API call
url = f"https://stats.oecd.org/restsdmx/sdmx.ashx/GetData/{dataset}/{geos}.{variables}/all?startTime={start_date}&endTime={end_date}"
oecd = get_oecd(url)

# keep 1 value per month, from the latest edition
oecd = oecd.sort_values(["obsTime", "EDI"]).groupby("obsTime").tail(1).reset_index(drop = True)

# convert obsTime to a date
oecd["obsTime"] = pd.to_datetime(oecd["obsTime"] + "-01")

# convert to USD
oecd["exports_usd"] = currency_convert(oecd.loc[:, ["obsTime", "obsValue"]].set_index("obsTime"), "RUB", "USD")

# plotting
p = line_plot((ais.date, ais.num_ships), (oecd.obsTime, oecd.exports_usd))
p
plt.savefig("plot.png")