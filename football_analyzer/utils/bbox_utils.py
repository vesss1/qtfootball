def get_center_of_bbox(bbox):
    """
    Returns the center point of a bounding box.

    Parameters:
        bbox (tuple/list): A tuple/list (x1, y1, x2, y2) representing the bounding box coordinates.

    Returns:
        tuple: (center_x, center_y) of the bounding box.
    """
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int((y1 + y2) / 2)


def get_bbox_width(bbox):
    """
    Returns the width of a bounding box.

    Parameters:
        bbox (tuple/list): A tuple/list (x1, y1, x2, y2) representing the bounding box coordinates.

    Returns:
        int: Width of the bounding box.
    """
    return int(bbox[2] - bbox[0])


def measure_distance(p1, p2):
    """
    Calculates the Euclidean distance between two points.

    Parameters:
        p1 (tuple): The first point (x1, y1).
        p2 (tuple): The second point (x2, y2).

    Returns:
        float: The distance between the two points.
    """
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5


def measure_xy_distance(p1, p2):
    """
    Calculates the x and y distance between two points.

    Parameters:
        p1 (tuple): The first point (x1, y1).
        p2 (tuple): The second point (x2, y2).

    Returns:
        tuple: (x_distance, y_distance) between the two points.
    """
    return (p1[0] - p2[0]), (p1[1] - p2[1])


def get_foot_position(bbox):
    """
    Returns the foot position (center-bottom) of a bounding box.

    Parameters:
        bbox (tuple/list): A tuple/list (x1, y1, x2, y2) representing the bounding box coordinates.

    Returns:
        tuple: (center_x, bottom_y) of the bounding box.
    """
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int(y2)
