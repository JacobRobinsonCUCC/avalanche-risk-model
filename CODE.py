import numpy as np


def degrees_to_radians(angle_degrees):
    """
    Returns the conversion of an angle from degrees to radians.

    In modern day, many people measure their angles in degrees but in numpy sin,cos and tan (the varibales we will be using in our slope)
    require angles to be in the form of radians rather than degress.

    When an angle is in degrees, it uses the formula to convert degrees to radians which is:
    radians = degrees × (π / 180)

    An example of this in use is below:
    degrees_to_radians(30) =
    (30 * π / 180) =
    0.5236
    """
    return angle_degrees * np.pi / 180


def compute_slope_gradient(height1, height2, horizontal_distance):
    """
    Returns the slope gradient (metres) between two terrain points at separate y coordinates but the same x coordinates.

    The slope represents how steep the terrain is and is calculated as
    the change in height divided by the horizontal distance between points (in other words, the gradient).

    grad = (y2-y1)/(x2-x1)
    (x2-x1) = horizontal distance

    The steeper the slope, the higher probability an avalanche will occur due to the gravity applying a larger
    downslope force (newtons), making it easier to overcome the frictional force (newtons) holding it.
    """
    return (height2 - height1) / horizontal_distance


def compute_gradient_to_angle(slope_gradient):
    """
    converts the slope gradient to an angle (radians)

    """
    return np.arctan(slope_gradient)


def compute_slope_length(height1, height2, horizontal_distance):
    """
     Returns the slope length (metres) between two terrain points at separate y coordinates but the same y coordinates but the same x
coordinates.

     Using Pythagoras' theorem (a^2 = (b^2 + c^2)), we can calulate the slope length (metres).

     slope length = ((height2 - height1)^2 + (horizontal_distance)^2)^1/2

     Assume the slope is smooth and straight.

     The slope length (metres) also affects the chances of an avalanche occurring
     due to a larger volume of snow and increased weight and stress.

    An example of this in use is below:
    compute_slope_length(3,6,4) =
    (((6 - 3 ) ** 2) + (4 ** 2))^0.5 =
    5
     """
    return np.sqrt(((height2 - height1) ** 2) + ((horizontal_distance) ** 2))


def compute_slope_angle(height1, height2, horizontal_distance):
    """
    Returns the angle of a slope using trig.

    Using the horizontal distance (metres) with the change in height (metres),
    you can calculate the angle (radians) using trigonometry.

    Avalanche risk increases significantly for slopes between
    approximately 30° and 45° with roughly 97% of avalanches happening above 30° (google).

    The angle (radians) is computed using:

    angle = arctan(height_change / distance)
    """
    return np.arctan((height2 - height1) / horizontal_distance)


def compute_slope_angle_risk(slope_angle):
    """
    Returns the risk of an avalanche based on the angle of the slope converting it between 0 and 1.

    Avalanche risk increases significantly for slopes between
    approximately 30° and 45° with roughly 97% of avalanches happening above 30°.
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
    Returns the risk of an avalanche based on the temperature (Celsius), placing it between a fixed value of 0 and 1.

    Using the temperature of the air (Celsius), we can create a model which creates a coefficient
    that puts depending on the

    Colder snow tends to be more stable and compact (although not as nice to ski on),
    while warmer snow becomes softer and more unstable.

    Example scale:

    temperature < -15°C: very hard snow
    -15°C to -5°C:         moderate hardness
    -5°C to 0°C:         soft snow (higher avalanche risk)
    """

    if temperature < -15:
        return 0.3
    if temperature < -8:
        return 0.45
    if temperature < 0:
        return 0.7
    else:
        return 1


def compute_fresh_snowfall_risk(fresh_snowfall):
    """
    Returns the risk of an avalanche based on the depth of fresh snowfall (metres), placing it between a fixed value of 0 and 1.
    Fresh snowfall is snowfall that has fallen within a 24-hour period.

    Fresh snowfall over a short period is used as a key factor,
    due to rapid snow accumulation, significantly increasing the chances of an avalanche due to added load on the snow.
    """

    if fresh_snowfall < 0.15:
        return 0.2
    if fresh_snowfall < 0.25:
        return 0.5
    if fresh_snowfall < 0.5:
        return 0.75
    else:
        return 1


def compute_slope_length_risk(slope_length):
    """
    Returns the risk of an avalanche based on the length of the slope, placing it between a fixed value of 0 and 1.

    The length of the slope can play a factor in the avalanche risk as longer slopes provide more room for   accleration,
    creating a larger momentum so there is a larger avalanche risk.

    """
    if slope_length < 60:
        return 0.2
    if slope_length < 150:
        return 0.6
    if slope_length < 300:
        return 0.8
    else:
        return 1


def compute_avalanche_risk(slope_angle, fresh_snowfall, temperature, slope_length):
    """
    Returns avalanche risk based on slope angle, snow depth, slope length and temperature.

    Using numbers calculated by using previous results, we can create an algorithm to categorise
    the chance of an avalanhce.

    Avalanche risk classification:
    'low', 'moderate', 'considerable', 'high' or 'extreme'. (like they use in ski resorts in Europe)

    Avalanche probability increases when:

    - Slopes are steeper (but not to steep as then the snow will not accumulate)
    - Fresh snowfall spawning in in quick succession
    - Temperature rises, melting the snow, making it softer and therefore less stable
    - The slope length is long

    The reason for each value being multiplied is that every variable plays a different factor into the chances of an avalanche,
    with the angle of the slope (radians) and fresh snowfall (metres) playing a larger chance of an avalanche,
    say compared to length of slope (metres) and the temperature (celcius).

    The reason they have been multiplied in this way is so that it can still achieve the max value of 4
    e.g 1.2 + 1.2 + 1 + 0.6 = 4
    """

    snow_risk = compute_fresh_snowfall_risk(fresh_snowfall)
    temp_risk = compute_temperature_risk(temperature)
    length_risk = compute_slope_length_risk(slope_length)
    angle_risk = compute_slope_angle_risk(slope_angle)

    total_score = (1.2 * angle_risk) + (1.2 * snow_risk) + temp_risk + (0.6 * length_risk)

    return score_to_classification(total_score)


def score_to_classification(score):
    """
    Using the addition of slope angle risk (radians), temperature risk (Celsius), slope length risk(metres) and fresh snowfall risk (metres),
    it converts it into a score between 0 and 4

    As there is 5 zones (low, moderate, considerable, high, extreme) we have divided 4 by 5 to segregate the zones evenly
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
