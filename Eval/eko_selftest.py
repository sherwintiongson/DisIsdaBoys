import numpy as np
import matplotlib.pyplot as plt

X, Y = 0, 1

# Constants (example thresholds)
EKO_MIN_EC80_B_HUB = 50
EKO_MAX_EC80_ALU_B_HUB = 5000
PROX_ERROR = 1
BUENDIG = 0

# Simulated system state
class SystemStateClass:
    def __init__(self):
        self.u8_Art = BUENDIG
        self.i32_UnsymmetryTeach = 20

SystemState = SystemStateClass()

# Simulated polygons (10 points each)
np.random.seed(42)
ai16_points_on = np.random.randint(110, 150, size=(10, 2))  # object present
ai16_points_off = np.random.randint(95, 105, size=(10, 2))  # background

# Compute centroids
def compute_centroid(points):
    points = np.array(points)
    centroid_x = np.mean(points[:, X])
    centroid_y = np.mean(points[:, Y])
    return centroid_x, centroid_y

centroid_on_x, centroid_on_y = compute_centroid(ai16_points_on)
centroid_off_x, centroid_off_y = compute_centroid(ai16_points_off)

# Calculate amplitudes relative to polygon centroid
Amp_points_on = np.sum((ai16_points_on[:, X] - centroid_on_x)**2 +
                       (ai16_points_on[:, Y] - centroid_on_y)**2, axis=0)
Amp_points_off = np.sum((ai16_points_off[:, X] - centroid_off_x)**2 +
                        (ai16_points_off[:, Y] - centroid_off_y)**2, axis=0)

# Hub calculation between first two points of ai16_points_on
dx_hub = ai16_points_on[1][X] - ai16_points_on[0][X]
dy_hub = ai16_points_on[1][Y] - ai16_points_on[0][Y]
hub_distance = dx_hub**2 + dy_hub**2

# Plot polygons and centroid
plt.figure(figsize=(8, 8))
plt.scatter(ai16_points_on[:, X], ai16_points_on[:, Y], color='blue', label='Points ON')
plt.scatter(ai16_points_off[:, X], ai16_points_off[:, Y], color='orange', label='Points OFF')
plt.scatter([centroid_on_x], [centroid_on_y], color='blue', marker='x', s=100, label='Centroid ON')
plt.scatter([centroid_off_x], [centroid_off_y], color='orange', marker='x', s=100, label='Centroid OFF')

plt.plot([ai16_points_on[0][X], ai16_points_on[1][X]],
         [ai16_points_on[0][Y], ai16_points_on[1][Y]], 'r--', label='Hub (first 2 points)')

plt.title(f'Polygon Points and Hub Distance: {hub_distance}')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()

print(f"Total amplitude ON: {Amp_points_on}")
print(f"Total amplitude OFF: {Amp_points_off}")
print(f"Hub distance between first two points: {hub_distance}")