# E-Commerce Delivery Time Prediction

## Project Overview

This project develops and deploys a Multiple Linear Regression model to
predict e-commerce delivery time in hours using order, package, warehouse,
courier, traffic, product-category and shipping information.

The project covers the complete workflow from raw data-quality assessment
and regression-assumption diagnosis to model evaluation and deployment
through an interactive Streamlit web application.

---

## Business Objective

The objective is to estimate the expected delivery time of a new
e-commerce order.

The prediction can support managers in:

- Delivery planning
- Logistics coordination
- Courier workload planning
- Setting customer delivery expectations

---

## Target Variable

`Delivery_Time_Hours`

The predicted output is expressed in **hours**.

---

## Predictor Variables

### Numerical Predictors

- `Order_Value`
- `Package_Weight_Kg`
- `Warehouse_Distance_Km`
- `Items_in_Order`
- `Warehouse_Processing_Hours`
- `Courier_Load_Index`
- `Traffic_Index`

### Categorical Predictors

- `Product_Category`
- `Shipping_Mode`

`Order_ID` is treated only as an identifier and is not used as a
regression predictor.

---

## Dataset

The raw dataset contains:

- **3,232 rows**
- **11 columns**
- **3,200 unique Order IDs**

After removing exact duplicate records and observations with missing target
values, **3,192 usable observations** remained.

The raw dataset intentionally contains data-quality issues so that the
complete cleaning and regression-diagnostic workflow can be demonstrated.

---

## Data Preparation

The following checks and treatments were performed:

- Missing-value detection
- Exact duplicate detection and removal
- Identification of the target, predictors and identifier
- Standardization of inconsistent categorical values
- Detection of logically impossible numerical values
- Treatment of invalid predictor values as missing
- Median treatment for numerical missing values
- Most-frequent-category treatment for categorical missing values
- IQR-based outlier investigation
- Standardized residual analysis
- Leverage analysis
- Cook's Distance analysis
- Correction of confirmed data-entry errors

Potential statistical outliers were investigated rather than automatically
removed.

---

## Linear Regression Assumption Checks

The project evaluates the major assumptions of Multiple Linear Regression
using:

- Linearity plots
- Correlation analysis
- Variance Inflation Factor (VIF)
- Mean of residuals
- Durbin-Watson statistic
- Residuals-versus-fitted plot
- Breusch-Pagan test
- Residual histogram
- Q-Q plot
- Jarque-Bera test
- Standardized residuals
- Leverage
- Cook's Distance

After confirmed data-entry corrections, the regression assumptions were
re-checked.

### Assumption Results After Corrections

| Diagnostic | Result |
|---|---:|
| OLS R-squared | 0.925365 |
| OLS Adjusted R-squared | 0.925060 |
| Durbin-Watson | 1.982046 |
| Breusch-Pagan p-value | 0.308044 |
| Jarque-Bera p-value | 0.640915 |
| Residual Skewness | 0.032176 |
| Residual Kurtosis | 2.949517 |

The post-correction residual diagnostics showed substantial improvement
compared with the initial uncorrected regression.

---

## Machine Learning Workflow

The final predictive workflow uses an **80/20 train-test split** with
`random_state=42`.

A scikit-learn Pipeline is used so that preprocessing and prediction are
performed consistently.

### Numerical Processing

Missing numerical predictor values are imputed using the median learned
from the training data.

### Categorical Processing

Missing categorical values are imputed using the most frequent category.

Categorical predictors are encoded using:

`OneHotEncoder(drop="first", handle_unknown="ignore")`

### Model

`LinearRegression`

---

## Model Performance

The final train-test evaluation produced:

| Metric | Value |
|---|---:|
| Training R-squared | 0.927116 |
| Training Adjusted R-squared | 0.926743 |
| Test R-squared | 0.917740 |
| Test MAE | 3.325331 hours |
| Test MSE | 17.180302 |
| Test RMSE | 4.144913 hours |

The test R-squared indicates that approximately **91.77% of the variation
in delivery time in the unseen test observations is explained by the
model**.

The Mean Absolute Error indicates an average absolute prediction error of
approximately **3.33 hours** on the test set.

---

## Saved Model

The complete preprocessing and Linear Regression workflow is saved as:

`model.pkl`

The saved object contains:

- Numerical missing-value treatment
- Categorical missing-value treatment
- One-hot encoding
- Multiple Linear Regression

After model evaluation was completed, the deployment version of the
pipeline was fitted on all **3,192 usable observations**.

---

## Streamlit Application

The Streamlit application:

- Loads the saved `model.pkl`
- Does not retrain the model when the application starts
- Accepts all required predictor values
- Performs basic input validation
- Generates predictions for new orders
- Displays delivery time in hours
- Provides a managerial interpretation of the result

### Verified Prediction

The application was verified using:

- Product Category: Electronics
- Shipping Mode: Same-Day
- Order Value: ₹6,000
- Package Weight: 3 kg
- Warehouse Distance: 800 km
- Items in Order: 4
- Warehouse Processing Hours: 3 hours
- Courier Load Index: 5
- Traffic Index: 9

The saved deployment model produced:

**59.69 hours**

---

## Application Screenshot

![Working Streamlit Prediction](screenshots/app_prediction.png)

---

## Project Structure

Project files:

- `ecommerce_delivery_unclean_data_3232.csv`
- `model_training_3232.ipynb`
- `model.pkl`
- `app.py`
- `requirements.txt`
- `README.md`
- `screenshots/app_prediction.png`

---

## Running the Application Locally

### Step 1 - Install Dependencies

Run:

`pip install -r requirements.txt`

### Step 2 - Start the Streamlit Application

Run:

`python -m streamlit run app.py`

### Step 3 - Open the Application

Streamlit will provide a local address, normally:

`http://localhost:8501`

---

## Important Usage Note

The application can generate predictions for new orders that were not
present in the training dataset.

Predictions are most reliable when predictor values remain within or
reasonably close to the ranges represented by the training data.

---

## Copyright

© 2026 Arin Bakshi. All Rights Reserved.

This project's original source code, documentation, application interface,
and project-specific model files may not be copied, modified,
redistributed, published or used commercially without prior written
permission from the author.

Third-party libraries, frameworks, course materials and externally sourced
components remain subject to their respective licenses and ownership.
