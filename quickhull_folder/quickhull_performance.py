import math

# Function to find the distance between a point and a line defined by two points
def find_distance(p1, p2, p3):

    # Calculate coefficients for the line equation ax + by + c = 0
    a = p1[1] - p2[1]
    b = p2[0] - p1[0]
    c = p1[0] * p2[1] - p2[0] * p1[1]
    
    # Use the dot product formula to find the distance between the line and a point
    return abs(a * p3[0] + b * p3[1] + c) / math.sqrt(a * a + b * b)

# Function to create segments above and below a line defined by two points
def create_segment(p1, p2, v):
    
    above = []
    below = []

    if p2[0] - p1[0] == 0:
    
        return above, below
    
    # Calculate the slope (m) and y-intercept (c) for the line equation y = mx + c
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
def upper_lower_hull(p1, p2, segment, flag):
    
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
            
    convex_hull = convex_hull + [farthest_point]

    # Point is now in the convex hull, so remove it from the segment
    segment.remove(farthest_point)

    # Determine the segments formed from two lines: p1-farthest_point and p2-farthest_point
    point1above, point1below = create_segment(p1, farthest_point, segment)
    point2above, point2below = create_segment(p2, farthest_point, segment)

    # Only use the segments in the same direction; the opposite direction is contained in the convex hull
    if flag == "above":
    
        convex_hull = convex_hull + upper_lower_hull(p1, farthest_point, point1above, "above")
        convex_hull = convex_hull + upper_lower_hull(farthest_point, p2, point2above, "above")
    
    else:
    
        convex_hull = convex_hull + upper_lower_hull(p1, farthest_point, point1below, "below")
        convex_hull = convex_hull + upper_lower_hull(farthest_point, p2, point2below, "below")

    return convex_hull

# Main function to compute the convex hull using the Quickhull algorithm
def quickhull(points):
    
    if len(points) <= 2:
    
        return points
        
    convex_hull = []

    # Sort the input points based on their x-coordinates
    sort = sorted(points, key=lambda x: x[0])

    p1 = sort[0]
    p2 = sort[-1]

    convex_hull = convex_hull + [p1, p2]

    # Remove the first and last points from the list as they are now in the convex hull
    sort.pop(0)
    sort.pop(-1)

    # Determine points above and below the line formed by p1 and p2
    above, below = create_segment(p1, p2, sort)
    
    # Recursively compute the upper and lower hulls
    convex_hull = convex_hull + upper_lower_hull(p1, p2, above, "above")
    convex_hull = convex_hull + upper_lower_hull(p1, p2, below, "below")

    # Return the computed convex hull points
    return convex_hull