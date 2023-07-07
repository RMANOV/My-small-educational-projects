import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima

# Load the excel file
data = pd.read_excel("C:/Users/r.manov/OneDrive/Работен плот/CH86_20230707_134852.xlsx")

# Print the first few rows of the DataFrame
print(data.head())

# Check the column names
print(data.columns)

# Strip extra spaces from column names
data.columns = data.columns.str.strip()

# Convert the 'Година' column to datetime format
data['Година'] = pd.to_datetime(data['Година'], format='%Y', errors='coerce')

# Set 'Година' as the index
data.set_index('Година', inplace=True)

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(data['Unnamed: 1'])
plt.xlabel('Year')
plt.ylabel('Sales Value')
plt.title('Annual Total Sales of Meat Products')
plt.grid(True)
plt.show()

# Determine the order of differencing (d) using the Augmented Dickey-Fuller test
result = adfuller(data['Unnamed: 1'].dropna())
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])

# auto_arima will automatically find the best p, d, q parameters
stepwise_fit = auto_arima(data['Unnamed: 1'].dropna(), trace=True, suppress_warnings=True)           

# Print the best parameters
print(stepwise_fit.summary())

# Build and fit the ARIMA model with the best parameters
model = ARIMA(data['Unnamed: 1'].dropna(), order=stepwise_fit.order)
model_fit = model.fit()

# Forecast for 2023
forecast = model_fit.forecast(steps=1)

# Adjust the forecast based on the CPI increase
cpi_increase = 0.13  # 13%
forecast_2023 = forecast[0] * (1 + cpi_increase)
print('Forecast for 2023:', forecast_2023)



# Sales level up to 07.07.2023
sales_current = 44848580.94

# Forecasted CPI for 2023 (10% ± 3%)
cpi_forecast_min = 0.07  # 10% - 3%
cpi_forecast_max = 0.13  # 10% + 3%

# The current date is 07.07.2023, so more than half of the year has passed.
# We'll assume that sales are equally distributed throughout the year, 
# so we'll estimate the total sales for 2023 based on the sales up to now.
sales_forecast = sales_current / (7/12)

# Adjust the forecasted sales for the expected change in CPI
sales_forecast_min = sales_forecast * (1 + cpi_forecast_min)
sales_forecast_max = sales_forecast * (1 + cpi_forecast_max)

print('Forecast for 2023 (with 7% CPI increase):', sales_forecast_min)
print('Forecast for 2023 (with 13% CPI increase):', sales_forecast_max)
