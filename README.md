
# 2023 UN Datathon Day 1 Workshop
## Task
The workshop task is to gather and process data from the OECD about Russian trade in order to compare it to AIS data.

Try to apply the principles and practices discussed in the presentation earlier. That means try to:

- Consider what you would have done before the presentation and think about what you might do differently now  
- Make the process as automatic as possible  
- Make the process as flexible/extendable as possible  
- Use version control and make the project a git repository

## Steps
1.  Get the AIS data on the number of tankers and cargo ships visiting Russian ports. For simplicity, the AIS processing has already been done and the data is available here: [https://github.com/dhopp1/ais_russia_data/blob/main/russian_port_data.csv](https://github.com/dhopp1/ais_russia_data/blob/main/russian_port_data.csv)
2.  Get monthly Russian export data from the OECD (2019-01 to 2023-08). Use this dataset:
	-  [https://stats.oecd.org/Index.aspx?DataSetCode=MEI_ARCHIVE#](https://stats.oecd.org/Index.aspx?DataSetCode=MEI_ARCHIVE), Revisions Analysis Dataset – Infra-annual Economic Indicators; take the data for each month from the latest edition available
3.  Convert the Russian data from Rubles to USD
4.  Combine the two datasets in order to create a plot showing the AIS data (tankers and cargo ships combined) compared to the OECD data

## Example of an unoptimized approach to the task
1.  Create a directory in your documents folder for this project named `russian_trade_data/`
2.  Go to [https://github.com/dhopp1/ais_russia_data/blob/main/russian_port_data.csv](https://github.com/dhopp1/ais_russia_data/blob/main/russian_port_data.csv) and download the CSV file, put it in the newly created directory
3.  Go to [https://stats.oecd.org/Index.aspx?DataSetCode=MEI_ARCHIVE#](https://stats.oecd.org/Index.aspx?DataSetCode=MEI_ARCHIVE#) and:
	1.  Set the country filter to `Russia`
	2.  Set the variable filter to `international trade in goods – exports (702)`
	3.  Set the frequency variable to `Monthly`
	4.  Set the time variable from `2019M1` to `2023M8`
	5.  Set the edition variable to cover the same months
	6.  Export the file to CSV and put in the directory
4.  Create a new excel file and paste the AIS data and the OECD data into two tabs
5.  Create a new tab where the AIS data is summed to have one value per month
6.  Create a new tab where the OECD data for each month is equivalent to the data from the latest edition
7.  Go to [https://www.investing.com/currencies/rub-usd-historical-data](https://www.investing.com/currencies/rub-usd-historical-data) and download the daily data to convert Rubles to USD
8.  Paste in a new sheet and use to convert the OECD data to USD
9.  Paste the monthly AIS data and OECD data into a new `plotting` tab and create plots

## What this repository does
- This repository accomplishes the task in a more optimized manner by running the `run_update.py` file, which, in sequence:
	- downloads the AIS data from GitHub
	- aggregates it to the monthly level
	- gets and cleans the OECD data
	- converts the OECD data to Rubles
	- saves the plot to disk