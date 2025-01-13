# **Real-Time Market Forecasting Model**

## Project Overview

This repository contains a sophisticated pipeline for handling high-dimensional time-series market data, performing feature engineering, imputation, and building a predictive model. 
The end-to-end process involves:
1. Distributed reading of large Parquet files using **Dask**.
2. Tracking missing-value distributions.
3. Dynamically categorizing columns for imputation vs. removal.
4. Transforming and scaling feature sets.
5. Training and evaluating an **XGBoost** regressor.
6. Using **SHAP** values for model explainability.

## Data Reading & Preprocessing

- **Dask** is leveraged to read multiple Parquet partitions in parallel, enabling efficient ingestion of large-scale datasets.
- A subset of data is sampled for in-memory manipulation (using `sample(frac=0.001)`).
- **StandardScaler** normalizes the sampled data to ensure stable gradients and improve the convergence of our regressor.

**Key Steps:**
1. Read Parquet files via Dask:
   ```python
   df = dd.read_parquet(filePaths)
2. Sample data at a given fraction:
   ```python
   ola = df.sample(frac=0.001)
   sampledf, test_df = ola.random_split([0.8, 0.2], random_state=42)
   sampledf = sampledf.compute()
3. Scale with `StandardScaler`:
   ```python
   sampledf = pd.DataFrame(StandardScaler().fit_transform(sampledf),
                        index=sampledf.index,
                        columns=sampledf.columns)

---

## Handling Missingness

- Missing percentages are calculated externally (from "Missing Percentage.txt") to split columns into **Impute** vs. **Exclude** categories.
- Missingness flags (`column_nan`) are introduced as separate binary features.
- Only columns with ≤10% missingness are imputed.

**Key Steps:**
1. Generate indicator variables for each column with NaNs:
   ```python
   df[f"{column}_nan"] = df[column].isna().astype(int)
2. Distinguish between columns to be imputed vs. dropped:
   ```python
   if nanColumns[column] > 10:
        nonImputeColumns.append(column)
   else:
        imputeColumns.append(column)
3. Perform IterativeImputer only on columns that are feasible for imputation.

---

## Feature Engineering & Selection

- Additional binary flags for missing data are treated as potential predictors.
- Columns with high missingness are either dropped or flagged as separate variables, depending on correlation thresholds.
- Correlations with the target (`responder_6`) are computed to guide final feature selection.

**Key Steps:**
1. Construct `X` and `y`:
   ```python
   X = checkdf.drop('responder_6', axis=1)
   y = checkdf['responder_6']
2. Split into training and testing sets:
   ```python
   X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    random_state=42)
3. Drop less relevant or highly sparse columns (`nonImputeColumns`):
   ```python
   sampledf = sampledf.drop(columns=nonImputeColumns)

---

## Imputation with IterativeImputer

**IterativeImputer** recursively models each feature with missing values as a function of other features to produce statistically coherent imputations.

**Key Steps:**
1. Select columns for imputation (`imputeColumns`).
2. Fit the imputer on the dataset:
   ```python
   imputeDF = X_test[imputeColumns]
   imputedArray = IterativeImputer(random_state=42, max_iter=45).fit_transform(imputeDF)
   X_test[imputeColumns] = imputedArray
3. Repeat the process for the main training sample or final dataset if necessary.

---

## XGBoost Regressor Training

- **XGBoost** provides a fast, parallelizable gradient boosting framework.
- Tunable hyperparameters like `n_estimators`, `learning_rate`, and `max_depth` are set for robust optimization.

**Key Steps:**
1. Instantiate the regressor:
   ```python
   model = xgb.XGBRegressor(n_estimators=100,
                            learning_rate=0.1,
                            max_depth=6,
                            random_state=42)
2. Fit the model on the training set:
   ```python
   model.fit(X_train, y_train)
3. Generate predictions and assess performance metrics (MSE, R²):
   ```python
   y_pred = model.predict(X_test)
   mse = mean_squared_error(y_test, y_pred)
   r2 = r2_score(y_test, y_pred)
   print("MSE:", mse)
   print("R2:", r2)

---

## Model Explainability with SHAP

- **SHAP (SHapley Additive exPlanations)** provides interpretability for complex models.
- Calculates per-feature contribution values, enabling a deeper understanding of model behavior.

**Key Steps:**
1. Construct SHAP explainer:
   ```python
   explainer = shap.TreeExplainer(model)
   shap_values = explainer.shap_values(X_test)
2. Visualize summary plots:
   ```python
   shap.summary_plot(shap_values, X_test)
3. Inspect local and global interpretability for vital business or research insights.

---

## Conclusions & Next Steps

- The pipeline demonstrates a high degree of predictive accuracy (R² ~ 0.99).
- Missing-value treatment via iterative imputation, combined with XGBoost, yields robust results.
- **Potential Future Work**:
  1. Hyperparameter tuning (e.g., Bayesian optimization).
  2. Integrating domain-specific feature engineering.
  3. Leveraging distributed training approaches for full data scale-up.
 
---

## Repository Structure

```plaintext
.
├── Data
│   └── jane-street-real-time-market-data-forecasting
│       ├── train.parquet
│       └── ...
├── Info
│   ├── Missing Percentage.txt
│   └── CorrelationMatrix.csv
├── Main.py  # Or your script name containing the code
└── README.md        # This documentation
```

---

## License & Acknowledgments

- This project is under Kaggle's Jane Street Competition.
- Special thanks to the **Dask** and **XGBoost** developer communities, as well as the creators of **SHAP** for model interpretability.
- Data courtesy of **Jane Street** for real-time market data forecasting.

