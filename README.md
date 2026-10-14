# AVARisk

Avalanche Risk Assessment Library for Python.

A library for calculating avalanche risk based on slope angle (radians),
temperature (°C), fresh snowfall (metres), and slope length (metres).

## Installation

```bash
pip install numpy
```

## Individual Function Breakdown

The library provides many functions beyond just computing avalanche risk. Here's a breakdown of each:

### 1. `degrees_to_radians(angle_degrees)`

Converts an angle from degrees to radians. The common practise is working with degrees but numpy's trig functions require radians.

```python
radians = degrees_to_radians(feta)     # (Radians)
```

### 2. `compute_slope_gradient(height1, height2, horizontal_distance)`

Calculates the slope gradient (rise over run) between two terrain points.

```python
gradient = compute_slope_gradient(x_1, x_2, y_1)
```

### 3. `compute_slope_gradient_risk(slope_gradient)`

Converts a slope gradient into a risk category based on likelihood of avalanche.

```python
risk = compute_slope_gradient_risk(x_3)
```

### 4. `compute_gradient_to_angle(slope_gradient)`

Converts a slope gradient to an angle in radians using arctan.

```python
angle = compute_gradient_to_angle(x_4)
```

### 5. `compute_slope_length(height1, height2, horizontal_distance)`

Calculates the actual slope length using Pythagoras' theorem (accounts for both vertical and horizontal distance).

```python
length = compute_slope_length(x_5, x_6, y_2)     # (Metres)
```

### 6. `compute_slope_angle(height1, height2, horizontal_distance)`

Calculates the angle of a slope in radians using trigonometry.

```python
angle = compute_slope_angle(x_6, x_7, y_3)     # (Radians)
```

### 7. `compute_slope_angle_risk(slope_angle)`

Converts a slope angle (in radians) to a risk score between 0 and 1.

```python
risk = compute_slope_angle_risk(feta_2)
```

### 8. `compute_temperature_risk(temperature)`

Converts temperature (Celsius) to a risk score based on snow stability.

```python
risk = compute_temperature_risk(y)    # (°C)
```

### 9. `compute_fresh_snowfall_risk(fresh_snowfall)`

Converts fresh snowfall depth to a risk score. Higher snowfall = higher risk.

```python
risk = compute_fresh_snowfall_risk(R)
```

### 10. `compute_slope_length_risk(slope_length)`

Converts slope length to a risk score. Longer slopes = more momentum = higher risk.

```python
risk = compute_slope_length_risk(L)
```

### 11. `compute_avalanche_risk(slope_angle, fresh_snowfall, temperature, slope_length)`

- Combines all risk factors into a single avalanche risk classification.

```python
snow_risk = compute_fresh_snowfall_risk(fresh_snowfall)
temp_risk = compute_temperature_risk(temperature)
length_risk = compute_slope_length_risk(slope_length)
angle_risk = compute_slope_angle_risk(slope_angle)

total_score = (1.2 * angle_risk) + (1.2 * snow_risk) + temp_risk + (0.6 * length_risk)
```

The risk is then categorised into 5 categories based on what number it scores

### 12. `score_to_classification(score)`

Converts a numeric score to a risk classification. Used internally by `compute_avalanche_risk`.

```python
level = score_to_classification(C)
```

## Induvidual Code With Little Docstring

### Basic Geometry Functions

```python
def degrees_to_radians(angle_degrees):
    """
    Convert degrees to radians
    """
    return angle_degrees * np.pi / 180


def compute_slope_gradient(height1, height2, horizontal_distance):
    """
    Compute slope gradient (unitless).
    """
    return (height2 - height1) / horizontal_distance


def compute_gradient_to_angle(slope_gradient):
    """
    Convert slope gradient to angle (radians)
    """
    return np.arctan(slope_gradient)


def compute_slope_length(height1, height2, horizontal_distance):
    """
    Compute slope length using Pythagoras
    """
    return np.sqrt((height2 - height1)**2 + horizontal_distance**2)


def compute_slope_angle(height1, height2, horizontal_distance):
    """
    Compute slope angle (radians)
    """
    return np.arctan((height2 - height1) / horizontal_distance)
```

### Risk Component Functions

```python
def compute_slope_angle_risk(slope_angle):
    """
    Numerical risk (0–1) from slope angle (radians)
    """
    if slope_angle < np.radians(20):
        return 0.2
    if slope_angle < np.radians(30):
        return 0.6
    if slope_angle < np.radians(45):
        return 1
    else:
        return 0.5


def compute_temperature_risk(temperature):
    """
    Risk from temperature (°C)
    """
    if temperature < -15:
        return 0.3
    if temperature < -8:
        return 0.45
    if temperature < 0:
        return 0.7
    else:
        return 1.0


def compute_fresh_snowfall_risk(fresh_snowfall):
    """
    Risk from fresh snowfall (metres).
    Rapid accumulation of snow creates extra load on the slope
    """
    if fresh_snowfall < 0.15:
        return 0.2
    if fresh_snowfall < 0.25:
        return 0.5
    if fresh_snowfall < 0.5:
        return 0.75
    else:
        return 1.0


def compute_slope_length_risk(slope_length):
    """
    Risk from slope length (metres)
    """
    if slope_length < 60:
        return 0.2
    if slope_length < 150:
        return 0.6
    if slope_length < 300:
        return 0.8
    else:
        return 1.0
```

## Final Model

```python
def compute_total_risk(angle_risk, snowfall_risk, temperature_risk, length_risk):
    """
    Weighted total risk score (0–4)
    """
    return (1.2 * angle_risk) + (1.2 * snowfall_risk) + temperature_risk +
    (0.6 * length_risk)


def score_to_classification(score):
    """
    Convert numeric score (0–4) into avalanche category
    """
    if score < 0.8:
        return "low"
    if score < 1.6:
        return "moderate"
    if score < 2.4:
        return "considerable"
    if score < 3.2:
        return "high"
    else:
        return "very high"


def compute_avalanche_risk(height1, height2, horizontal_distance,
                           fresh_snowfall, temperature):
    """
    Full avalanche risk model.
    Returns a classification string.
    """

    # Geometry
    slope_angle = compute_slope_angle(height1, height2, horizontal_distance)
    slope_length = compute_slope_length(height1, height2, horizontal_distance)

    # Risk components
    angle_risk = compute_slope_angle_risk(slope_angle)
    snow_risk = compute_fresh_snowfall_risk(fresh_snowfall)
    temp_risk = compute_temperature_risk(temperature)
    length_risk = compute_slope_length_risk(slope_length)

    # Total score
    total_score = compute_total_risk(angle_risk, snow_risk, temp_risk, length_risk)
```

# Explenation of code above

```python
"""
The Avalanche Risk Model combines geometric and environmental variables
into a probabilistic classification.
"""

import numpy as np

#Avalanche initiation depends strongly on slope angle between 30°–45°,
#where roughly 97% of avalanches occur.

### Example elevation data

h1 = 1500 # lower height (m)
h2 = 1650 # upper height (m)
d = 300 # horizontal distance (m)

### The slope angle θ is calculated using arctan of the height change over distance:

theta = np.arctan((h2- h1) / d)
theta_degrees = np.degrees(theta)

print("Slope angle (degrees):", theta_degrees)

### The gradient (slope steepness) and slope length are auxiliary quantities:

gradient = (h2- h1) / d
slope_length = np.sqrt((h2- h1)**2 + d**2)

print("Gradient:", gradient)
print("Slope length (m):", slope_length)
```

## Environmental factors

```python
# Temperature: warmer snow is less compact and increases instability
# Fresh snowfall: rapid accumulation adds extra load
# Slope length: longer slopes allow larger avalanches to develop
# Slop angle: Stepper slope increase the gravitational force against the frictional force so makes snow more unstavle
# Each variable is scaled between 0 and 1 and combined with specific weights:
```

R = 1.2*A + 1.2*S + T + 0.6*L

Where:

- A = angle risk
- S = snowfall risk
- T = temperature risk
- L = slope-length risk

The weighting values were chosen to reflect the relative influence of each factor on the formation of an avalanche.

Slope angle and snowfall risk have the largest coefficients (1.2) as they are the most influential drivers of slab failure.

Then Temperature is given a coefficient value of 1.0 as it plays a major role in weakening the snowpack, but usually acts by amplifying existing instabilities rather than creating them by itself.

The final factor is slope length which is given a smaller weight (0.6) as it affects the scale and runout of an avalanche.

However it doesn't have much of an effect on the inital trigger of an avalanche.

This is why the selected weighting have been used to keep our model scientifically correct and accurate.

```python
#The sum gives a total risk score between 0 and 4.

def compute_total_risk(angle_risk, snowfall_risk, temperature_risk, length_risk):
    """
    Combine weighted risk components to compute total risk score (0–4).
    """
    R = (1.2 * angle_risk) + (1.2 * snowfall_risk) + temperature_risk + (0.6 * length_risk)
    return R
```

Thank you for reading ReadMe. I hope this has explaiend how to use the code.
