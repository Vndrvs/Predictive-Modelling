import pandas as pd

# two tables contain alcohol dependence data, we have to merge them into one frame
def merge_alcohol_data(prev, fresh):
    # remove overlapping duplicates (data was available in two separate tables)
    return (pd.concat([prev, fresh])
            .drop_duplicates(subset="Év", keep="last")
            .sort_values("Év")
            .reset_index(drop=True))

# create one dataframe from separate ones
def merge_all_data(*dataFrames):
    # merge any number of tables with inner join (so only common years remain)
    return reduce(lambda left, right: pd.merge(left, right, on="Év", how="inner"), dataFrames)

# create normalized variable (intoxicated accidents per 100k cars)
def normalize_accidents(dataFrame):

    df["Ittas_Baleset_100ezer_Autóra"] = (
        df["Ittas_Személygépkocsi_Baleset"]
        / df["Személygépkocsik"]
        * 100000
    )

    return dataFrame