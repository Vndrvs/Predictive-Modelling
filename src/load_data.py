import pandas as pd

# handling the Hungarian encoding and custom table operations here
def read_hun_csv(path, skippedRows, headerRow):
    
    dataFrame = pd.read_csv(path, sep=";", encoding="cp1250", skiprows=skippedRows, header=headerRow)
    
    return dataFrame

# basic data formatting
def prettier_stat_table(dataFrame, selectedColumns):
    # rename columns depending on context
    cleanedDf = dataFrame[list(selectedColumns.keys())].rename(columns=selectedColumns)

    # Hungarian statistical exports use spaces as thousands separators, must strip before numeric conversion
    for col in cleanedDf.columns:
        cleanedDf[col] = (
            cleanedDf[col]
            .astype(str)
            .str.replace(r"\s+", "", regex=True)
        )
        cleanedDf[col] = pd.to_numeric(cleanedDf[col], errors="coerce")

    # fix cleared row
    cleanedDf = cleanedDf.reset_index(drop=True)

    return cleanedDf

# table: "Személylysérüléses közlekedési balesetek"
def load_road_accidents(path):

    accidents = read_hun_csv(path, 0, 0)

    # remove unused row
    accidents.columns = accidents.iloc[0]
    accidents = accidents.iloc[1:]

    # original tables repeat the header row inside the data, have to remove it manually
    accidents = accidents[accidents["Év"] != "Év"]

    selectedColumns = { "Év": "Év", "Ebből: személygépkocsi": "Személygépkocsi_Baleset" }
    accidents = prettier_stat_table(accidents, selectedColumns)
    return accidents

# table: "Ittasan okozott személysérüléses közúti közlekedési balesetek"
def load_intoxicated_accidents(path):
    
    accidents = read_hun_csv(path, 0, 0)

    # remove unused row
    accidents.columns = accidents.iloc[0]
    accidents = accidents.iloc[1:]
    
    accidents = accidents[accidents["Év"] != "Év"]

    selectedColumns = { "Év": "Év", "Ebből: személygépkocsi": "Ittas_Személygépkocsi_Baleset" }
    accidents = prettier_stat_table(accidents, selectedColumns)
    
    return accidents
    
# table: "Személygépjármű állomány"
def load_personal_cars(path):
    
    dataFrame = read_hun_csv(path, 1, 0)

    # this dataset is stored horizontally (years as columns), got to reshape into standard format
    cars = dataFrame.iloc[0, 1:].to_frame().reset_index()

    cars.columns = ["Év", "Személygépkocsik"]
    selectedColumns = { "Év": "Év", "Személygépkocsik": "Személygépkocsik" }
    cars = prettier_stat_table(cars, selectedColumns)
    
    return cars

# table: "Az alkoholisták gondozása"
def load_alcohol_dependence(path):

    dependents = read_hun_csv(path, 0, 0)

    # fix header
    dependents.columns = dependents.iloc[0]
    dependents = dependents.iloc[1:]

    selectedColumns = { "Év": "Év", "Az alkoholisták becsült száma, ezer": "Alkoholfüggők_becsült_száma" }

    dependents = prettier_stat_table(dependents, selectedColumns)
    # convert thousands to actual count
    dependents["Alkoholfüggők_becsült_száma"] = dependents["Alkoholfüggők_becsült_száma"] * 1000

    return dependents

# table: "Alkohol okozta mentális és viselkedészavar miatt egészségügyi járóbeteg szakellátásban részesülõk"
def load_alcohol_treatment(path):

    dependents = read_hun_csv(path, 0, None)

    # find where "Együtt" table starts, keep only that piece
    start = dependents[dependents[0] == "Együtt"].index[0] + 1
    dependents = dependents.iloc[start:]

    # only keep year and last column
    dependents = dependents[[0, dependents.columns[-1]]]

    selectedColumns = { 0: "Év", dependents.columns[-1]: "Alkoholfüggők_becsült_száma"}
    dependents = prettier_stat_table(dependents, selectedColumns)
    # as the number is written in thousands scale, we multiply locally here
    dependents["Alkoholfüggők_becsült_száma"] = dependents["Alkoholfüggők_becsült_száma"] * 1000

    return dependents