# Alcohol-Related Road Accident Analysis (Hungary)

This project analyzes the relationship between alcohol consumption and road accidents in Hungary using official statistical data.

The goal is not only to explore trends, but also to evaluate whether the introduction of the zero tolerance policy in 2008 had a measurable impact on alcohol-related accidents.

## I. Project Overview

The analysis is based on publicly available data from the Hungarian Central Statistical Office (KSH), including:

- Number of registered passenger vehicles  
- Total road accidents  
- Accidents caused by intoxicated drivers  
- Estimated number of alcohol-dependent individuals  

The workflow includes:

- Data cleaning and alignment across multiple sources  
- Feature engineering (trend, lag variables, normalization)  
- Exploratory data analysis (EDA)  
- Structural break analysis (2008 policy introduction)  
- Linear regression modeling for interpretation and prediction  

## II. Key Objective

A central question of the project:

> Did the zero tolerance regulation introduced in 2008 contribute to a reduction in alcohol-related road accidents?

This is examined through both visual analysis and regression modeling.

## III. Methodology

- **Normalization**  
  Accidents are scaled per 100,000 vehicles to account for the increasing car population.

- **Lag analysis**  
  Alcohol dependence is introduced with a 1-year lag to reflect delayed effects.

- **Policy variable**  
  A binary indicator captures the post-2008 zero tolerance period.

- **Modeling approach**  
  A multiple linear regression model is used for interpretability rather than complexity.

## IV. Project Structure

    predictive-modelling/
    │
    ├── src/
    │   ├── load_data.py
    │   └── predictive_model.py
    │
    ├── notebooks/
    │   └── analysis.ipynb
    │
    ├── requirements.txt
    └── README.md

## V. Setup & Running the Project

1. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Register Jupyter kernel
```bash
python -m ipykernel install –user –name=pred-model –display-name “Python (pred-model)”
```

4. Launch Jupyter
```bash
jupyter lab
```
Select the kernel: Python (pred-model)

## VI. Verifying Environment

To make sure the notebook uses the correct environment:
```bash
import sys
print(sys.executable)
```
It should point to:
```bash
…/predictive-modelling/.venv/bin/python
```
## VII. Results Summary
- **A strong downward trend is observed after 2008**
- **The zero tolerance policy appears as a structural break in the data**
- **Regression results suggest that policy impact is more significant than alcohol dependence trends alone**  
- **Vehicle growth alone does not explain the observed changes**  

## VIII. Limitations
- **Small dataset (limited number of yearly observations)**
- **Alcohol dependence is estimated, not directly measured**
- **Other external factors (enforcement intensity, cultural shifts) are not included**
