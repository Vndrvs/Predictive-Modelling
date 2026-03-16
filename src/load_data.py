import pandas as pd

# csv parser with hungarian encoding
def parse_csv(path, skippedRows, headerRow):
    dataFrame = pd.read_csv(path, sep=";", encoding="cp1250", skiprows=skippedRows, header=headerRow)
    
    return dataFrame

# basic data formatting
def clean_dataframe(dataFrame, selectedColumns):
    # rename columns depending on context
    cleanedDf = dataFrame[list(selectedColumns.keys())].rename(columns=selectedColumns)

    # remove spaces from strings and convert strings to numbers
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
    

def load_road_accidents(path):
     # read hungarian text
    df = parse_csv(path, 0, 0)

    # remove unused row
    df.columns = df.iloc[0]
    df = df.iloc[1:]

    # clean duplicate row
    df = df[df["Év"] != "Év"]

    selectedColumns = { "Év": "Év", "Ebből: személygépkocsi": "Személygépkocsi_Baleset" }
    df = clean_dataframe(df, selectedColumns)
    return df

#  table: "Ittasan okozott személysérüléses közúti közlekedési balesetek"
def load_intoxicated_accidents(path):
    
    df = parse_csv(path, 0, 0)

    # remove unused row
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    
    # clear duplicate row
    df = df[df["Év"] != "Év"]

    selectedColumns = { "Év": "Év", "Ebből: személygépkocsi": "Ittas_Személygépkocsi_Baleset" }
    df = clean_dataframe(df, selectedColumns)
    
    return df
    

def load_personal_cars(path):
    df = parse_csv(path, 1, 0)

    cars = df.iloc[0, 1:].to_frame().reset_index()

    cars.columns = ["Év", "Személygépkocsik"]
    selectedColumns = { "Év": "Év", "Személygépkocsik": "Személygépkocsik" }
    cars = clean_dataframe(cars, selectedColumns)
    
    return cars

def load_alcohol_dependence(path):

    df = parse_csv(path, 0, 0)

    # fix header
    df.columns = df.iloc[0]
    df = df.iloc[1:]

    selectedColumns = { "Év": "Év", "Az alkoholisták becsült száma, ezer": "Alkoholfüggők_becsült_száma" }

    df = clean_dataframe(df, selectedColumns)
    # convert thousands → actual count
    df["Alkoholfüggők_becsült_száma"] = df["Alkoholfüggők_becsült_száma"] * 1000

    return df


def load_alcohol_treatment(path):

    df = parse_csv(path, 0, None)

    # find where the actual "Együtt" table starts
    start = df[df[0] == "Együtt"].index[0] + 1

    # keep only that block
    df = df.iloc[start:]

    # keep year and last column
    df = df[[0, df.columns[-1]]]

    selectedColumns = { 0: "Év", df.columns[-1]: "Alkoholfüggők_becsült_száma"}
    df = clean_dataframe(df, selectedColumns)
    df["Alkoholfüggők_becsült_száma"] = df["Alkoholfüggők_becsült_száma"] * 1000

    return df