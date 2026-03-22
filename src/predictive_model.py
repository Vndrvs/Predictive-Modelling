from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# prepare the cleaned dataframe for the predictive model by calculating trends, lag variables, and the olicy flags
def prepare_model_data(dataFrame):

    df_copy = dataFrame.copy()
    
    # sort by year and reset to make sure trend calculation is accurate
    df_copy["Év"] = df_copy["Év"].astype(int)
    df_copy = df_copy.sort_values("Év").reset_index(drop=True)
    
    # trend captures long-term decline in accidents independent of other factors
    df_copy["Trend"] = df_copy["Év"] - df_copy["Év"].min()
    # alcohol dependence likely affects accidents with delay
    df_copy["Alkoholfüggők_lag1"] = df_copy["Alkoholfüggők_becsült_száma"].shift(1)
    
    # zero-tolerance law introduced in 2008, expect structural break in intoxicated driving behavior
    df_copy["Zéró_Tolerancia"] = (df_copy["Év"] >= 2008).astype(int)

    # delete first row because there is nothing to compare to beforehand
    return df_copy.dropna()

def forecast_model(dataFrame, y_variable, x_variables):

    # target: number of intoxicated driving related accidents the forecast should explain
    actual_accidents = dataFrame[y_variable]
    # predictors reflect competing explanations:
    # long-term trend (overall road safety improvements)
    # alcohol dependence (behavioral factor)
    # policy (zero tolerance after 2008)
    predictors = dataFrame[x_variables]

    # sample size is small, so simple linear model seems a fit
    model = LinearRegression()
    model.fit(predictors, actual_accidents)

    # in-sample prediction: used to understand fit and variable influence
    predicted_accidents = model.predict(predictors)
    # r2 shows how much of the variation in accidents is explained
    r2 = r2_score(actual_accidents, predicted_accidents)

    return model, predictors, actual_accidents, predicted_accidents, r2

def showcase_model_results(model, predictors, actual_accidents, predicted_accidents, r2, title):
    
     # display coefficients to see which features drive the result
    output_weights = pd.DataFrame({
        "Változó": predictors.columns,
        "Együttható": model.coef_
    })

    print(f"Tengelymetszet: {model.intercept_:.3f}")
    print(f"R² Eredmény: {r2:.3f}")
    print("\nEgyütthatók:")
    print(output_weights)

    # set our scatter plot
    plt.figure(figsize=(6, 5))
    plt.scatter(actual_accidents, predicted_accidents, alpha=0.7)

    # draw reference line for better visibility
    min_val = min(actual_accidents.min(), predicted_accidents.min())
    max_val = max(actual_accidents.max(), predicted_accidents.max())
    plt.plot([min_val, max_val], [min_val, max_val],
             color='red', linestyle='--', alpha=0.5,
             label='Tökéletes illeszkedés')

    plt.xlabel("Tényleges érték")
    plt.ylabel("Becsült érték")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
def compare_models(dataFrame, y_variable, model_specs):
    # compare different explanations: time trend / policy / alcohol dependence
    results = []
    for name, x_variables in model_specs.items():

        model, predictors, actual_accidents, predicted_accidents, r2 = forecast_model(dataFrame, y_variable, x_variables)
        row = {
            "Model": name,
            "R2": round(r2, 3)
        }
        # map coefficients back to their variable names
        for var, coef in zip(predictors.columns, model.coef_):
            row[var] = round(coef, 4)

        results.append(row)

    # fill 'NaN' fields with empty spacing to improve looks
    return pd.DataFrame(results).fillna("")

def forecast_and_plot_future(dataFrame, model, x_variables,
                            actual_accidents, predicted_accidents,
                            years_ahead=5):

    # create future years based on accident and behaviour data from last observed year
    last_year = dataFrame["Év"].max()

    future_data = pd.DataFrame({
        "Év": range(last_year + 1, last_year + 1 + years_ahead)
    })

    # extend trend consistently with training data of our model
    future_data["Trend"] = future_data["Év"] - dataFrame["Év"].min()

    # hungarian zero tolerance policy remains active after
    future_data["Zéró_Tolerancia"] = 1

    # estimate future number of personal cars in the country using linear trend
    car_trend = np.polyfit(dataFrame["Év"], dataFrame["Személygépkocsik"], 1)
    future_data["Személygépkocsik"] = np.poly1d(car_trend)(future_data["Év"])

    # projection of dependent people
    alcohol_trend = np.polyfit(
        dataFrame["Év"],
        dataFrame["Alkoholfüggők_becsült_száma"],
        1
    )

    future_data["Alkoholfüggők"] = np.poly1d(alcohol_trend)(future_data["Év"])

    # create same lag as before
    future_data["Alkoholfüggők_lag1"] = future_data["Alkoholfüggők"].shift(1)

    # first future row uses last observed real accident value
    future_data.loc[0, "Alkoholfüggők_lag1"] = (
        dataFrame["Alkoholfüggők_becsült_száma"].iloc[-1]
    )

    # prepare predictors for future forecast
    future_predictors = future_data[x_variables]

    future_data["Predicted"] = model.predict(future_predictors)
    plt.figure(figsize=(8, 5))

    # historical actual vs fitted
    plt.plot(dataFrame["Év"], actual_accidents,
             marker='o', label="Tényleges")
    plt.plot(dataFrame["Év"], predicted_accidents,
             linestyle='--', label="Becsült")

    # future forecast
    plt.plot(future_data["Év"], future_data["Predicted"],
             linestyle=':', marker='o', label="Előrejelzés")

    plt.xlabel("Év")
    plt.ylabel("Ittas balesetek száma")
    plt.title("Modell illeszkedés és előrejelzés")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.show()

    return future_data