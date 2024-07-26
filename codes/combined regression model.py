import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the distance range in meters
distance_meters = np.arange(0, 1001, 50)  # 0m to 1km, every 50m

# Define the polynomial regression model (distance in km)
def polynomial_regression(distance_km):
    return -0.35299846 * distance_km**2 + 0.99133024 * distance_km + 77.28837766

# Define the logarithmic regression model (distance in meters)
def logarithmic_regression(distance_m):
    if distance_m == 0:
        return None  # log(0) is undefined
    return -12.35 * np.log(distance_m) + 105.34

# Define the distance range in km for the polynomial regression model
distance_km = distance_meters / 1000  # convert to km

# Calculate noise levels for both models
polynomial_noise_km = [polynomial_regression(d) for d in distance_km]
logarithmic_noise_m = [logarithmic_regression(d) for d in distance_meters]

# Define the reference noise level and distance
reference_distance = 150  # in meters
reference_noise = 70  # in dB

# Recalculate the integrated noise level considering the reference noise level at 150m
integrated_noise_with_reference = []
for distance in distance_meters:
    # Adjust the polynomial and logarithmic models to consider the reference noise at 150m
    polynomial_adjustment = reference_noise - (polynomial_regression(reference_distance / 1000))
    logarithmic_adjustment = reference_noise - logarithmic_regression(reference_distance)

    # Apply adjustments
    if distance == 0:
        integrated_noise_with_reference.append(reference_noise)  # log(0) is undefined, use reference noise
    else:
        poly_noise_adjusted = polynomial_regression(distance / 1000) + polynomial_adjustment
        log_noise_adjusted = logarithmic_regression(distance) + logarithmic_adjustment
        integrated_noise_with_reference.append((poly_noise_adjusted + log_noise_adjusted) / 2)

# Create a dataframe to display the results
data = {
    "Distance (m)": distance_meters,
    "Polynomial Noise Level (km)": polynomial_noise_km,
    "Logarithmic Noise Level (m)": logarithmic_noise_m,
    "Integrated Noise Level with Reference": integrated_noise_with_reference
}

df = pd.DataFrame(data)

# Regression function (assumed polynomial for simplicity)
def regression_function(x, a, b, c):
    return a * x**2 + b * x + c

# Fit the regression model to the adjusted integrated noise level
params, covariance = curve_fit(regression_function, distance_meters, integrated_noise_with_reference)

# Extract the coefficients
a, b, c = params

# Calculate the fitted values
fitted_values = regression_function(distance_meters, a, b, c)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(distance_meters, integrated_noise_with_reference, 'o', label='Observed Integrated Noise Level with Reference')
plt.plot(distance_meters, fitted_values, '-', label=f'Fitted Curve: {a:.5f}x^2 + {b:.5f}x + {c:.5f}')
plt.xlabel('Distance (m)')
plt.ylabel('Noise Level (dB)')
plt.title('Adjusted Integrated Noise Level with Reference')
plt.legend()
plt.grid(True)
plt.show()

# Regression equation
regression_equation = f"Noise Level = {a:.5f} * Distance^2 + {b:.5f} * Distance + {c:.5f}"
