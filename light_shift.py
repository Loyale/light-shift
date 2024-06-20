import machine
import neopixel
import time
import math

# Define the pin and number of Neopixels
pin = machine.Pin(16)  # GPIO pin connected to the data line of Neopixel
n = 8  # Number of Neopixels
np = neopixel.NeoPixel(pin, n)

# Define the light schedule based on time of day
light_schedule = [
    (20, 20, 20),    # 4 AM
    (20, 20, 20), # 5 AM
    (20, 20, 20), # 6 AM
    (30, 30, 30), # 7 AM
    (50, 50, 50),# 8 AM
    (70, 70, 70),# 9 AM
    (90, 90, 90),# 10 AM
    (100, 100, 100),# 11 AM
    (100, 100, 100),# 12 PM
    (150, 110, 100),
    (90, 90, 90), # 1 PM
    (70, 70, 70), # 2 PM
    (50, 50, 50), # 3 PM
    (30, 30, 30),  # 4 PM
    (20, 20, 20),  # 5 PM
    (20, 20, 20),  # 6 PM
]

# light_schedule = [
#     (0, 0, 0),    # 12 AM
#     (255,0,0),
#     (0,0,255),
#     (0,0,0),
# ]
# Gamma correction function
def gamma_correct(value, gamma=2.2):
    return int((value / 255.0) ** gamma * 255.0)

# Apply gamma correction to an entire color tuple
def apply_gamma_correction(color, gamma=2.2):
    return (
        gamma_correct(color[0], gamma),
        gamma_correct(color[1], gamma),
        gamma_correct(color[2], gamma)
    )

# Function to set the Neopixels to a specific color with gamma correction
def set_color(np, r, g, b, gamma=2.2):
    r, g, b = apply_gamma_correction((r, g, b), gamma)
    for i in range(len(np)):
        np[i] = (r, g, b)
    time.sleep(0.001)  # Small delay to stabilize data
    np.write()

# Function to initialize Neopixels to off state
def initialize_neopixels(np):
    for i in range(len(np)):
        np[i] = (0, 0, 0)
    np.write()
    time.sleep(0.001)  # Small delay to stabilize

# Function to interpolate between two colors
def interpolate_color(color1, color2, factor):
    return (
        int(color1[0] + (color2[0] - color1[0]) * factor),
        int(color1[1] + (color2[1] - color1[1]) * factor),
        int(color1[2] + (color2[2] - color1[2]) * factor)
    )

# Function to smoothly transition between two colors
def smooth_transition(np, color1, color2, duration, steps=100, gamma=2.2):
    for i in range(steps + 1):
        factor = i / steps
        color = interpolate_color(color1, color2, factor)
        set_color(np, *color, gamma)
        time.sleep(duration / steps)

# Function to simulate light changes based on schedule with smooth transitions
def simulate_light(np, light_schedule, gamma=2.2):
    for i in range(len(light_schedule) - 1):
        smooth_transition(np, light_schedule[i], light_schedule[i+1], duration=1, gamma=gamma)

# Initialize Neopixels to off state at startup
initialize_neopixels(np)

# Main loop
while True:
    simulate_light(np, light_schedule)