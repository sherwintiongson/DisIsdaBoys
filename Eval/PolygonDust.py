import matplotlib.pyplot as plt
import copy

X=0
Y=1
BackgroundX = 0
BackgroundY = 0
HYST_BUENDIG =  0.7800000
HYST_FREIZONE =  0.7800000


poly_on = [
    [700, 800],  # 0
    [1800, 500],  # 1
    [0, 0],  # 2
    [0, 0],  # 3
    [0, 0],  # 4
    [0, 0],  # 5
    [0, 0],  # 6
    [0, 0]  # 7
]

poly_off = [
    [0, 0],  # 0
    [0, 0],  # 1
    [0, 0],  # 2
    [0, 0],  # 3
    [0, 0],  # 4
    [0, 0],  # 5
    [0, 0],  # 6
    [0, 0]  # 7
]

dust_poly_on = [
    [0, 0],  # 0
    [0, 0],  # 1
    [0, 0],  # 2
    [0, 0],  # 3
    [0, 0],  # 4
    [0, 0],  # 5
    [0, 0],  # 6
    [0, 0]  # 7
]

dust_poly_off = [
    [0, 0],  # 0
    [0, 0],  # 1
    [0, 0],  # 2
    [0, 0],  # 3
    [0, 0],  # 4
    [0, 0],  # 5
    [0, 0],  # 6
    [0, 0]  # 7
]


def plot_polygon(coordinates):
    """
    Plots a polygon using the given coordinates.

    Parameters:
    coordinates (list of list of floats): A 2D array where each inner list contains the x and y coordinates of a vertex.
    """
    # Unpack the coordinates into two separate lists: x and y
    x, y = zip(*coordinates)

    # Close the polygon by adding the first point at the end
    x = list(x) + [x[0]]
    y = list(y) + [y[0]]

    # Plot the polygon
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.fill(x, y, alpha=0.3)  # Fill the polygon with a transparent color
    plt.title("Polygon Plot")
    plt.xlabel("X coordinates")
    plt.ylabel("Y coordinates")
    plt.grid(True)
    plt.show()


def plot_TwoPolygons(coords1, coords2, color1='blue', color2='green', marker1='o', marker2='s'):
    """
    Plots two polygons using the given coordinates.

    Parameters:
    coords1 (list of list of floats): A 2D array where each inner list contains the x and y coordinates of the first polygon.
    coords2 (list of list of floats): A 2D array where each inner list contains the x and y coordinates of the second polygon.
    color1 (str): Color for the first polygon.
    color2 (str): Color for the second polygon.
    marker1 (str): Marker style for the first polygon.
    marker2 (str): Marker style for the second polygon.
    """
    # Unpack the coordinates into two separate lists for each polygon
    x1, y1 = zip(*coords1)
    x2, y2 = zip(*coords2)

    # Close the polygons by adding the first point at the end
    x1 = list(x1) + [x1[0]]
    y1 = list(y1) + [y1[0]]
    x2 = list(x2) + [x2[0]]
    y2 = list(y2) + [y2[0]]

    # Plot the first polygon
    plt.plot(x1, y1, marker=marker1, color=color1, label='Polygon 1')
    plt.fill(x1, y1, color=color1, alpha=0.3)  # Fill the polygon with a transparent color

    # Plot the second polygon
    plt.plot(x2, y2, marker=marker2, color=color2, label='Polygon 2')
    plt.fill(x2, y2, color=color2, alpha=0.3)  # Fill the polygon with a transparent color

    # Adding titles and labels
    plt.title("Polygons Plot")
    plt.xlabel("X coordinates")
    plt.ylabel("Y coordinates")
    plt.grid(True)
    plt.legend()
    plt.show()


def Set_Polygon_M18_Buendig(polygon):
    # Point B
    polygon[2][X] = (polygon[1][X] << 1) - polygon[0][X];
    polygon[2][Y] = (polygon[1][Y] << 1) - polygon[0][Y];

    # Point C
    polygon[3][X] = ((polygon[2][X]-BackgroundX)*0.7071000) - (((polygon[2][Y]-BackgroundY)* (-0.7071000))+BackgroundX)
    polygon[3][Y] = ((polygon[2][X] - BackgroundX) * (-0.7071000)) - (((polygon[2][Y] - BackgroundY) * 0.7071000) + BackgroundY)

    # Point D
    polygon[4][X] = polygon[2][Y] - BackgroundY + BackgroundX
    polygon[4][Y] = -polygon[2][X] + BackgroundX + BackgroundY

    # Point E
    polygon[5][X] = ((polygon[2][X]-BackgroundX) * (-0.7071000)) - (((polygon[2][Y] - BackgroundY) * (-0.7071000) ) + BackgroundX)
    polygon[5][Y] = ((polygon[2][X]-BackgroundX) * (-0.7071000)) + (((polygon[2][Y] - BackgroundY) * (-0.7071000) ) + BackgroundY)

    # Point 2
    polygon[6][X] = (BackgroundX << 1) - polygon[1][X]
    polygon[6][Y] = (BackgroundY << 1) - polygon[1][Y]

    # Point 1
    polygon[7][X] = polygon[0][X] - (0.7071000 * (polygon[1][X] - polygon[0][X]))
    polygon[7][Y] = polygon[0][Y] - (0.7071000 * (polygon[1][Y] - polygon[0][Y]))

    return polygon


def Set_Polygon_M18_Freizone(polygon):
    # Point B
    polygon[2][X] = polygon[1][X] + (1.414210 * (polygon[1][X] - polygon[0][X]));
    polygon[2][Y] = polygon[1][Y] + (1.414210 * (polygon[1][Y] - polygon[0][Y]));

    # Point C
    polygon[3][X] = ((polygon[2][X]-BackgroundX)*0.7071000) - (((polygon[2][Y]-BackgroundY)* (-0.7071000))+BackgroundX)
    polygon[3][Y] = ((polygon[2][X] - BackgroundX) * (-0.7071000)) - (((polygon[2][Y] - BackgroundY) * 0.7071000) + BackgroundY)

    # Point D
    polygon[4][X] = polygon[2][Y] - BackgroundY + BackgroundX
    polygon[4][Y] = -polygon[2][X] + BackgroundX + BackgroundY

    # Point E
    polygon[5][X] = ((polygon[2][X]-BackgroundX) * (-0.7071000)) - (((polygon[2][Y] - BackgroundY) * (-0.7071000) ) + BackgroundX)
    polygon[5][Y] = ((polygon[2][X]-BackgroundX) * (-0.7071000)) + (((polygon[2][Y] - BackgroundY) * (-0.7071000) ) + BackgroundY)

    # Point 2
    polygon[6][X] = ((polygon[1][X]-BackgroundX) * (-0.7071000)) - ((polygon[1][Y]-BackgroundY) * 0.6427800) + BackgroundX
    polygon[6][Y] = ((polygon[1][X]-BackgroundX) * 0.6427800) + ((polygon[1][Y] - BackgroundY) * (-0.7071000)) + BackgroundY

    # Point 1
    polygon[7][X] = (polygon[0][X] << 1) - polygon[1][X];
    polygon[7][Y] = (polygon[0][Y] << 1) - polygon[1][Y];

    return polygon


def Calc_Off_Polygon(polygon, hysteresis):
    polygon_off = [
        [0, 0],  # 0
        [0, 0],  # 1
        [0, 0],  # 2
        [0, 0],  # 3
        [0, 0],  # 4
        [0, 0],  # 5
        [0, 0],  # 6
        [0, 0]  # 7
    ]
    for i in range(len(polygon)):
        polygon_off[i][X] = (hysteresis * (polygon[i][X] - BackgroundX)) + BackgroundX
        polygon_off[i][Y] = (hysteresis * (polygon[i][Y] - BackgroundY)) + BackgroundY

    return polygon_off



# Example usage
coordinates = [
    [700, 800],         # 0
    [1800, 500],        # 1
    [2900, 100],        # 2
    [2300,-2000],       # 3
    [50, -3500],        # 4
    [-3500, -2400],     # 5
    [-3300, -1200],      # 6
    [-150, 1050]       # 7
]

#poly_on = Set_Polygon_M18_Buendig(poly_on)
#poly_off = Calc_Off_Polygon(poly_on, HYST_FREIZONE)
#plot_TwoPolygons(poly_on, poly_off, color1='blue', color2='red', marker1='o', marker2='x')

poly_on = Set_Polygon_M18_Buendig(poly_on)
#poly_on = Set_Polygon_M18_Freizone(poly_on)
poly_off = Calc_Off_Polygon(poly_on, HYST_FREIZONE)
#plot_TwoPolygons(poly_on, poly_off, color1='blue', color2='red', marker1='o', marker2='x')

dust_poly_on = copy.deepcopy(poly_on)
dust_poly_off = copy.deepcopy(poly_off)

#dust_poly_on[4][X] = dust_poly_on[4][X] - 1000
dust_poly_on[4][Y] = dust_poly_on[4][Y] - 2000
dust_poly_on[5][X] = dust_poly_on[5][X] - 4500
dust_poly_on[5][Y] = dust_poly_on[5][Y] - 2000
dust_poly_on[6][X] = dust_poly_on[6][X] - 4500
dust_poly_on[6][Y] = dust_poly_on[6][Y]

#dust_poly_off[4][X] = poly_off[4][X] - 1000
dust_poly_off[4][Y] = poly_off[4][Y] - 2000
dust_poly_off[5][X] = poly_off[5][X] - 4400
dust_poly_off[5][Y] = poly_off[5][Y] - 2000
dust_poly_off[6][X] = poly_off[6][X] - 4200
dust_poly_off[6][Y] = poly_off[6][Y] - 200

#plot_TwoPolygons(poly_on, dust_poly_on, color1='blue', color2='red', marker1='o', marker2='x')

# Unpack the coordinates into two separate lists for each polygon
x1, y1 = zip(*poly_on)
x2, y2 = zip(*poly_off)
x3, y3 = zip(*dust_poly_on)
x4, y4 = zip(*dust_poly_off)

# Close the polygons by adding the first point at the end
x1 = list(x1) + [x1[0]]
y1 = list(y1) + [y1[0]]
x2 = list(x2) + [x2[0]]
y2 = list(y2) + [y2[0]]
x3 = list(x3) + [x3[0]]
y3 = list(y3) + [y3[0]]
x4 = list(x4) + [x4[0]]
y4 = list(y4) + [y4[0]]

# Plot the first polygon
plt.plot(x1, y1, marker='o', color='blue', label='poly_on')
plt.fill(x1, y1, color='blue', alpha=0.3)  # Fill the polygon with a transparent color

# Plot the second polygon
plt.plot(x2, y2, marker='x', color='red', label='poly_off')
plt.fill(x2, y2, color='red', alpha=0.3)  # Fill the polygon with a transparent color

# Plot the second polygon
plt.plot(x3, y3, marker="v", color='orange', label='dust_poly_on')
plt.fill(x3, y3, color='orange', alpha=0.3)  # Fill the polygon with a transparent color

# Plot the second polygon
plt.plot(x4, y4, marker="^", color='green', label='dust_poly_off')
plt.fill(x4, y4, color='green', alpha=0.3)  # Fill the polygon with a transparent color

# Adding titles and labels
plt.title("Polygons Plot")
plt.xlabel("X coordinates")
plt.ylabel("Y coordinates")
plt.grid(True)
plt.legend()
plt.show()
