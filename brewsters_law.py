import numpy as np
import matplotlib.pyplot as plt

def get_user_data():
    print("--- Data Entry (DEGREES ONLY) ---")
    try:
        # 1. Get Least Counts (Instrument Precision) in DEGREES
        lc_angle_deg = float(input("Enter Least Count of Angle Scale (degrees): "))
        lc_reflectance = float(input("Enter Least Count of Reflectance/Current Meter: "))
        
        # 2. Get Data Points
        print("\nEnter your data separated by commas.")
        x_str = input("Angles of Incidence (degrees): ")
        y_str = input("Reflectance/Current values: ")
        
        # Convert strings to numpy arrays
        angles = np.array([float(x) for x in x_str.split(',')])
        reflectance = np.array([float(y) for y in y_str.split(',')])
        
        # Check for size mismatch
        if len(angles) != len(reflectance):
            print(f"Error: You entered {len(angles)} angles but {len(reflectance)} reflectance values.")
            return None, None, None, None
            
        return angles, reflectance, lc_angle_deg, lc_reflectance
        
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return None, None, None, None

# --- Main Execution ---

# 1. Get the data
# Uncomment the line below to enable user input:
angles_deg, reflectance, x_err_deg, y_err = get_user_data()
if angles_deg is None: exit() 

# 2. Sort data
sorted_indices = np.argsort(angles_deg)
angles_deg = angles_deg[sorted_indices]
reflectance = reflectance[sorted_indices]

# 3. Find Experimental Brewster Angle (Minimum Reflectance)
min_index = np.argmin(reflectance)
brewster_angle_deg = angles_deg[min_index]

# Calculate Refractive Index
# Note: np.tan REQUIRES radians, so we convert inside the function call only.
refractive_index = np.tan(np.deg2rad(brewster_angle_deg))

# --- ERROR CALCULATION (Hidden Conversion) ---
# Formula: Δn = sec²(θ) * Δθ
# We multiply by (np.pi / 180) because the derivative of tan(x°) is (π/180)*sec²(x°)
sec_squared = (1 / np.cos(np.deg2rad(brewster_angle_deg)))**2
delta_n = sec_squared * x_err_deg * (np.pi / 180) 

# --- PLOTTING ---
plt.figure(figsize=(10, 7))

# Plot Data with Error Bars (X-Axis is Degrees)
plt.errorbar(angles_deg, reflectance, 
             xerr=x_err_deg, yerr=y_err, 
             fmt='o', color='red', ecolor='black', capsize=5, 
             label='Measured Data', markersize=6)

# Connect dots
plt.plot(angles_deg, reflectance, linestyle='--', color='gray', alpha=0.5)

# Mark the Minimum
plt.axvline(x=brewster_angle_deg, color='blue', linestyle='-.', alpha=0.8)
plt.text(brewster_angle_deg + 2, max(reflectance)*0.8, 
         f"Brewster Angle: {brewster_angle_deg}°", 
         color='blue', fontweight='bold')

# Formatting
plt.title(f"Reflectance vs Angle (Degrees)\n(Instrument Error: $\\pm{x_err_deg}^\circ$)", fontsize=14)
plt.xlabel("Angle of Incidence (Degrees)", fontsize=12)
plt.ylabel("Reflectance Intensity", fontsize=12)
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.minorticks_on()

# Display Results
plt.figtext(0.15, 0.80, 
            f"Results:\n"
            f"Angle $\\theta_B$ = {brewster_angle_deg}°\n"
            f"Refractive Index $n$ = {refractive_index:.3f} $\\pm$ {delta_n:.3f}",
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'))

plt.show()

print(f"Experimental Brewster Angle: {brewster_angle_deg} degrees")
print(f"Refractive Index (n): {refractive_index:.4f} +/- {delta_n:.4f}")
