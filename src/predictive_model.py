from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pandas as pd
import matplotlib.pyplot as plt

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