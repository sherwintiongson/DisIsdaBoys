import matplotlib.pyplot as plt
import numpy as np

# Example 2D array of polygon vertices
vertices = np.array([
    [571, 845],
    [1724, 489],
    [2875, 135],
    [2172, -1998],
    [168, -3510],
    [-3463, -2807],
    [-3324, -1155],
    [-245, 1094]
])

# Extract x and y coordinates
x = vertices[:, 0]
y = vertices[:, 1]

# Close the polygon by adding the first point to the end
x = np.append(x, x[0])
y = np.append(y, y[0])

# Plot the polygon
plt.figure()
plt.plot(x, y, marker='o')  # 'o' to mark vertices
plt.title('Polygon from 2D Array')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)

# Label each coordinate
for i, (x_coord, y_coord) in enumerate(vertices):
    plt.text(x_coord, y_coord, f'({x_coord}, {y_coord})', fontsize=12, ha='right')

plt.show()
