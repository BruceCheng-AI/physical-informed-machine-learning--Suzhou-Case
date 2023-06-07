# physical-informed-machine-learning--Suzhou-Case
"physical-informed machine learning- Suzhou Case" is a repository of Jupyter Notebooks demonstrating machine learning techniques for modeling physical phenomena in Suzhou.

# Hydrology-Driven Machine Learning Model

## 1. Introduction
This project revolves around the use of hydrology-driven machine learning models that integrate knowledge from hydrology and advanced machine learning algorithms, offering a fresh perspective for predicting water levels and flow rates. The complete process of the model application at Fengqiao Station and Suzhou Station is meticulously documented.

## 2. Data Preprocessing
We kick-started the project by collecting historical hydrological site information from Fengqiao Station and Suzhou Station. The data includes rainfall, water level, and flow data from both stations, each on a daily scale. We also gathered some basic meteorological data including temperature (T2M, T2M_MAX, T2M_MIN), and relative humidity (RH2M) from NASA's POWER project. This data allowed us to calculate evapotranspiration, laying the foundation for subsequent model construction.

## 3. Rating-Curve Fitting
Given the proximity and similar water system of Fengqiao Station and Suzhou Station, we assumed their flow-water level curves (rating curves) are similar. Traditionally, these curves have been calculated using fitted mathematical formulas. However, correlation analysis revealed a correlation of just 0.66 between the two stations, indicating substantial nonlinear correlation. Consequently, we employed the machine learning method - time-attribute-based random forest model, to fit these curves. The results demonstrated high accuracy of the model.

## 4. Hydrological Model
To accurately predict future hydrological conditions, we built an ensemble watershed hydrological model. This model considers several key hydrological processes, such as precipitation, evaporation, surface runoff, infiltration, and groundwater runoff. The model inputs precipitation and outputs river flow. After initial modeling, the model accurately captured trend data, but was less satisfactory in handling low-value information. This opens an avenue for introducing machine learning.

## 5. Machine Learning
On the basis of the hydrological model, we introduced a deep learning model to enhance the accuracy of predictions. This process is inspired by the concept of Physics-informed machine learning, which attempts to incorporate prior knowledge from physics into machine learning models to improve the accuracy and interpretability of predictions. Preliminary experiments utilized the random forest model and indicated that introducing runoff features significantly enhanced the prediction accuracy, setting the foundation for subsequent deep learning models.

## 6. Climate Scenarios
To account for the impact of future climate changes, we introduced climate scenario data from CMIP6. We selected the GFDL-ESM4 model and extracted several climate variables, including humidity, rainfall, air pressure, and temperature. By analyzing this data, we could predict future rainfall trends, which in turn provide the foundation for future water level predictions.

## 7. Future Water Level Prediction
Lastly, we used the VAR model to predict future flow rates and water levels. This process included several steps such as future trend analysis and eigenvalue analysis, which led us to reliable prediction results.

## 8. Conclusion
With the hydrology-driven machine learning model, we successfully predicted future water levels and flows at Fengqiao Station and Suzhou Station. This process integrates hydrological knowledge and machine learning techniques, enabling us to make more accurate hydrological predictions while considering future climate changes. This methodology has broad application prospects and is significant in enhancing our understanding and predictive capability of hydrological processes.

## How to Use this Repository

The source code for the hydrology-driven machine learning model is found within this repository. The data processing, machine learning model fitting, and prediction stages are each broken down into their respective scripts.

### Prerequisites
- Make sure Python 3.x is installed on your system.
- Install the necessary Python libraries using the command: `pip install -r requirements.txt`.

### Steps
1. Clone this repository to your local system.
2. Run the scripts.

### Notes
- You may need to modify the scripts slightly to fit your specific setup or data.
- For any clarifications or issues, please raise an issue in the GitHub repository.

Enjoy forecasting!
