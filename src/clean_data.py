import pandas as pd

# unfortunately, alcohol dependence data was split into two separate tables on KSH
def merge_alcohol_data(previous, fresh):
    # there were overlapping years present in the data
    matching_years = set(previous["Év"]).intersection(set(fresh["Év"]))
    
    if matching_years:
        # so before we work with the data, it's a generally good idea to check whether they match or not
        detected_mismatches = []

        for year in matching_years:
            year_older = previous.loc[previous["Év"] == year, "Alkoholfüggők_becsült_száma"].values[0]
            year_newer = fresh.loc[fresh["Év"] == year, "Alkoholfüggők_becsült_száma"].values[0]

            if year_older != year_newer:
                detected_mismatches.append((year, year_older, year_newer))

        # if finding values that don't match, let's display them
        if detected_mismatches:
            raise ValueError(
                "Eltérést találtam a két adatsor között az alkoholfüggőséggel gondozottak tábláiban:\n" +
                "\n".join([f"Year {y}: previous={p}, fresh={f}" for y, p, f in detected_mismatches])
            )

    # if validated, then merge
    return (
        pd.concat([previous, fresh])
        .drop_duplicates(subset="Év", keep="last")
        .sort_values("Év")
        .reset_index(drop=True)
    )

# we have 4 different tables and we need one dataframe for the project task analysis
def merge_all_data(*dataFrames):
    
    for i, table in enumerate(dataFrames):
        # first, let's verify they all have year column, as that will be one axis in following timed plots
        if "Év" not in table.columns:
            raise ValueError(f"DataFrame {i} is missing 'Év' column")

        years = table["Év"].dropna().astype(int).sort_values()
        # want to catch tables that have potential year gaps (defence against the dark arts)
        expected_range = range(years.min(), years.max() + 1)
        missing_years = sorted(set(expected_range) - set(years))

        if missing_years:
            raise ValueError(f"A {i} táblából hiányoznak a következő évekre vonatkozó adatok: {missing_years}. ")

    # merge all passed tables with inner join (so only mutual years can be present in final table)
    merged = dataFrames[0]
    for table in dataFrames[1:]:
        merged = pd.merge(merged, table, on="Év", how="inner")
        
    return merged

# create normalized variable to make findings less dependent on growing number of car pool (-> intoxicated accidents per 100k cars)
def normalize_accidents(dataFrame):

    needed_data = ["Ittas_Személygépkocsi_Baleset", "Személygépkocsik"]

    # if a column as a whole is not present, the whole function will fail
    for data in needed_data:
        if data not in dataFrame.columns:
            raise ValueError(f"Hiba, hiányzik a következő adatsor: {col}")

    # we need values for all years for the predictive model to work
    if dataFrame[needed_data].isnull().any().any():
        raise ValueError("Hiba: Hiányzó adat a balesetszám normalizáció során.")

    # cannot divide by zero in the computation itself, check it
    if (dataFrame["Személygépkocsik"] == 0).any():
        raise ValueError("Hiba: Autók száma nem lehet nulla, mivel nullával nem tudunk osztani.")

    dataFrame["Ittas_Baleset_100ezer_Autóra"] = (dataFrame["Ittas_Személygépkocsi_Baleset"] / dataFrame["Személygépkocsik"] * 100000)

    return dataFrame

# compute what percentage of the accidents were caused by intoxicated drivers
def describe_intoxicated_rate(dataFrame):

    # now repeating the same error handling as described in the last function
    needed_data = ["Ittas_Személygépkocsi_Baleset", "Személygépkocsi_Baleset"]

    for data in needed_data:
        if data not in dataFrame.columns:
            raise ValueError(f"Hiba, hiányzik a következő adatsor: {col}")

    if dataFrame[needed_data].isnull().any().any():
        raise ValueError("Hiba: Hiányzó adat az ittas baleset arányának kiszámolása során.")

    if (dataFrame["Személygépkocsi_Baleset"] == 0).any():
        raise ValueError("Hiba: Össz. balesetek száma nem lehet nulla, mivel nullával nem tudunk osztani.")

    dataFrame["Ittas_Baleset_Arány"] = (dataFrame["Ittas_Személygépkocsi_Baleset"] / dataFrame["Személygépkocsi_Baleset"] * 100)
    
    return dataFrame