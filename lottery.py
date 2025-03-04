import pandas as pd 
import numpy as np 
import requests
import datetime

# Get the current draw for today.
def get_lottery_type():
	curr_date = datetime.datetime.today()
	day = curr_date.weekday()
	curr_time = curr_date.time()

	# Selection for next draw starts after 10pm
	cutoff_time = datetime.time(22, 0, 0)
	
	if curr_time > cutoff_time:
		day = (day + 1) % 7
		
	match day:
		case 0 | 3: return "set-for-life"
		case 1 | 4: return "euromillions"
		case 2 | 5: return "lotto"
		case 6: return None

# Returns the:
# 1. Name of the draw. 
# 2. CSV file where the filtered, unanalysed data is located.
# 3. CSV file where the analysed data is located.
def get_stats() -> tuple[str, str, str]:
	draw = get_lottery_type()
    
	# If it's a Sunday, no draws take place.
	if not draw:
		return (None, None, None)
       
	url = f"https://www.national-lottery.co.uk/results/{draw}/draw-history/csv"
	data_file = "data.csv"
	filtered_file = "filtered_data.csv"
	res_file = "most_freq.csv"

	store_raw_data(url, data_file)

	store_filtered_data(data_file, filtered_file)

	analyse_data(filtered_file, res_file)

	return (draw, filtered_file, res_file)


def store_raw_data(url: str, data_file: str):
	# Get the data & store it in `data.csv`
	response = requests.get(url, stream=True)

	with open(data_file, "wb") as file:
		file.write(response.content)
	
def store_filtered_data(in_file: str, out_file: str):
	df = pd.read_csv(in_file)

	filter_mask = (df.columns == "DrawDate") | \
				  (df.columns.str.contains("ball|star", case=False) & df.apply(lambda x: pd.api.types.is_numeric_dtype(x)))
	
	filtered_df = df.loc[:, filter_mask]
	filtered_df.to_csv(out_file, index=False)
	

def analyse_data(file, out_file):
	# Extract only only the fields containing the balls.
	df = pd.read_csv(file)

	# Get sorted numbers for each draw.
	sorted_df = df.drop("DrawDate", axis=1)

	# Generate most commonly occurring number for each entry.
	most_freq_balls: pd.DataFrame = sorted_df.mode().iloc[[0]]
	most_freq_balls.to_csv(out_file, index=False)
