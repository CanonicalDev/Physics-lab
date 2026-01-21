import matplotlib.pyplot as plt
import numpy as np

# 1. Get Input
x_input = input("Input Angle values (x) separated by commas: ")
y_input = input("Input Reflectance values (y) separated by commas: ")

# 2. Convert to lists of numbers
x = [float(i) for i in x_input.split(",")]
y = [float(i) for i in y_input.split(",")]

# 3. SORT the data (Important for connecting lines properly)
# This pairs (x,y), sorts them by x, and separates them back
data = sorted(zip(x, y))
x_sorted, y_sorted = zip(*data)

# 4. Plot
plt.figure(figsize=(8, 5))

# 'o-' means: o (draw a dot at each point) and - (draw a line between them)
plt.plot(x_sorted, y_sorted, 'o-', color='blue', linewidth=2, label='Measured Data')

plt.title("Brewster's Law Experiment")
plt.xlabel("Angle of Incidence (degrees)")
plt.ylabel("Reflectance")
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

plt.show()