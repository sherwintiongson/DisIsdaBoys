import matplotlib.pyplot as plt


def plot_polygons(coords1, coords2, color1='blue', color2='green', marker1='o', marker2='s'):
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


# Example usage
coords1 = [
    [1, 1],
    [4, 1],
    [4, 4],
    [1, 4]
]

coords2 = [
    [2, 2],
    [6, 2],
    [6, 5],
    [2, 5]
]

plot_polygons(coords1, coords2, color1='blue', color2='red', marker1='o', marker2='x')
