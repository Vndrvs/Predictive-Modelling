import pandas as pd
from functools import reduce

# two tables contain alcohol dependence data, we have to merge them into one frame
def merge_alcohol_data(prev, fresh):
    # remove overlapping duplicates (data was available in two separate tables)
    return (pd.concat([prev, fresh])
            .drop_duplicates(subset="Év", keep="last")
            .sort_values("Év")
            .reset_index(drop=True))

# create one dataframe from separate ones
def merge_all_data(*dataFrames):
    # merge any number of tables with inner join (we need matching years which is 2002-2024)
    return reduce(lambda left, right: pd.merge(left, right, on="Év", how="inner"), dataFrames)

# create normalized variable to make findings less dependent on number of cars (intoxicated accidents per 100k cars)
def normalize_accidents(dataFrame):

    dataFrame["Ittas_Baleset_100ezer_Autóra"] = (dataFrame["Ittas_Személygépkocsi_Baleset"] / dataFrame["Személygépkocsik"] * 100000)

    return dataFrame

# what percentage of the accidents were caused by intoxicated drivers
def describe_intoxicated_rate(dataFrame):

    dataFrame["Ittas_Baleset_Arány"] = (dataFrame["Ittas_Személygépkocsi_Baleset"] / dataFrame["Személygépkocsi_Baleset"] * 100)
    
    return dataFrame