import time
import numpy as np
import math

from IPython.display import clear_output

time_sleeping = 1.0

# Function to initialize the plot with convex hull points
def initial_plot_updated(ax, canvas, convex_hull):
    
    time.sleep(time_sleeping)
    
    # Draw Convex Hull points in red
    ax.scatter([x[0] for x in convex_hull], [y[1] for y in convex_hull], c='r', marker='o', label='Highlighted Points')
    
    # Draw a dashed line connecting the highlighted points
    ax.plot([x[0] for x in convex_hull], [y[1] for y in convex_hull], 'k--', linewidth=1, label='Line between Highlighted Points')
    
    canvas.draw()
    
    return ax, canvas

# Function to update the plot internally when computing the convex hull
def update_plot_internally(ax, p1, p2, farthest_point, canvas):
    
    time.sleep(time_sleeping)
    
    # Draw the farthest Convex Hull point in red
    ax.scatter(farthest_point[0], farthest_point[1], c='r', marker='o')
    
    # Draw dashed lines from the farthest point to p1 and p2
    ax.plot([farthest_point[0], p1[0]], [farthest_point[1], p1[1]], 'k--', linewidth=1)
    ax.plot([farthest_point[0], p2[0]], [farthest_point[1], p2[1]], 'k--', linewidth=1)
    
    canvas.draw()
    
    return ax, canvas

# Function to create the final plot of the convex hull
def final_plot(ax, convex_hull, canvas):
    
    time.sleep(time_sleeping)
    
    # Convert convex_hull to numpy array for easier manipulation
    convex_hull = np.array(convex_hull)
    
    if len(convex_hull) > 2:
    
        # Calculate polar coordinates (angle and radius) with respect to the center
        center = np.mean(convex_hull, axis=0)
        angles = np.arctan2(convex_hull[:, 1] - center[1], convex_hull[:, 0] - center[0])
    
        # Sort convex_hull based on angles
        sorted_indices = np.argsort(angles)
        sorted_convex_hull = convex_hull[sorted_indices]
        # Connect the convex_hull points to form a circular shape
        ax.plot(np.append(sorted_convex_hull[:, 0], sorted_convex_hull[0, 0]), np.append(sorted_convex_hull[:, 1], sorted_convex_hull[0, 1]), 'r-', linewidth=2)
    
    else:
    
        # Connect the convex_hull points if there are only 2 or 3 points
        x = convex_hull[:, 0]
        y = convex_hull[:, 1]
        ax.plot(x, y, 'r-', linewidth=2)
    
    canvas.draw()

# Function to find the distance between a point and a line defined by two points
def find_distance(p1, p2, p3):
    
    # Using the formula ax + by + c = 0
    a = p1[1] - p2[1]
    b = p2[0] - p1[0]
    c = p1[0] * p2[1] - p2[0] * p1[1]
    
    # Use dot product to find the distance between a line and a point
    return abs(a * p3[0] + b * p3[1] + c) / math.sqrt(a * a + b * b)

# Function to create segments above and below a line defined by two points
def create_segment(p1, p2, v):
    
    above = []
    below = []

    if p2[0] - p1[0] == 0:
    
        return above, below

    # Calculate m and c for y = mx + c
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    c = -m * p1[0] + p1[1]

    # Loop through each coordinate and place it into the correct list (above or below the line)
    for coordinate in v:
    
        # y > mx + c means it is above the line
    
        if coordinate[1] > m * coordinate[0] + c:
    
            above.append(coordinate)
    
        # y < mx + c means it is below the line
        elif coordinate[1] < m * coordinate[0] + c:
    
            below.append(coordinate)

    return above, below

# Recursive function to compute the upper or lower hull
def upper_lower_hull(ax, p1, p2, segment, flag, canvas, root):
    
    if segment == [] or p1 is None or p2 is None:

        return []

    convex_hull = []

    # Calculate the distance of every point from the line to find the farthest point
    farthest_distance = -1
    farthest_point = None

    for point in segment:

        distance = find_distance(p1, p2, point)

        if distance > farthest_distance:

            farthest_distance = distance
            farthest_point = point

    # Update the plot if a farthest point is found
    if farthest_point:

        convex_hull = convex_hull + [farthest_point]
        ax, canvas = update_plot_internally(ax, p1, p2, farthest_point, canvas)
        root.update()  # Update the GUI

    # Remove the farthest point from the segment
    segment.remove(farthest_point)

    # Determine the segments formed from two lines: p1-farthest_point and p2-farthest_point
    point1above, point1below = create_segment(p1, farthest_point, segment)
    point2above, point2below = create_segment(p2, farthest_point, segment)

    # Only use the segments in the same direction; the opposite direction is contained in the convex hull
    if flag == "above":

        convex_hull = convex_hull + upper_lower_hull(ax, p1, farthest_point, point1above, "above", canvas, root)
        convex_hull = convex_hull + upper_lower_hull(ax, farthest_point, p2, point2above, "above", canvas, root)

    else:

        convex_hull = convex_hull + upper_lower_hull(ax, p1, farthest_point, point1below, "below", canvas, root)
        convex_hull = convex_hull + upper_lower_hull(ax, farthest_point, p2, point2below, "below", canvas, root)

    return convex_hull

# Main function to compute the convex hull using the Quickhull algorithm
def quickhull(ax, canvas, root, points, current_value):

    global time_sleeping
    time_sleeping = current_value

    if len(points) <= 1:

        raise ValueError("At least 2 points are required to create a convex hull")

    if len(points) > 2:

        convex_hull = []
        sort = sorted(points, key=lambda x: x[0])
        p1 = sort[0]
        p2 = sort[-1]
        convex_hull = convex_hull + [p1, p2]

        if len(points) == 2:

            ax, canvas = initial_plot_updated(ax, canvas, convex_hull)

            return ax, points

        sort.pop(0)
        sort.pop(-1)

        ax, canvas = initial_plot_updated(ax, canvas, convex_hull)
        root.update()  # Update the GUI

        above, below = create_segment(p1, p2, sort)

        convex_hull = convex_hull + upper_lower_hull(ax, p1, p2, above, "above", canvas, root)
        convex_hull = convex_hull + upper_lower_hull(ax, p1, p2, below, "below", canvas, root)

        final_plot(ax, convex_hull, canvas)

        return convex_hull

    else:

        final_plot(ax, points, canvas)

        return points