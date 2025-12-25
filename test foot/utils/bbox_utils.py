def get_center_of_bbox(bbox):
    """
    Returns the center point of a bounding box.
    
    Args:
        bbox (tuple/list): Bounding box coordinates (x1, y1, x2, y2).
        
    Returns:
        tuple: (center_x, center_y) coordinates.
        
    Raises:
        ValueError: If bbox format is invalid.
    """
    if not bbox or len(bbox) != 4:
        raise ValueError("bbox must contain exactly 4 coordinates (x1, y1, x2, y2)")
    
    x1, y1, x2, y2 = bbox
    
    # Validate coordinates
    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"Invalid bounding box: x2 must be > x1 and y2 must be > y1. Got: {bbox}")
    
    return int((x1 + x2) / 2), int((y1 + y2) / 2)


def get_bbox_width(bbox):
    """
    Returns the width of a bounding box.
    
    Args:
        bbox (tuple/list): Bounding box coordinates (x1, y1, x2, y2).
        
    Returns:
        int: Width of the bounding box.
        
    Raises:
        ValueError: If bbox format is invalid.
    """
    if not bbox or len(bbox) != 4:
        raise ValueError("bbox must contain exactly 4 coordinates (x1, y1, x2, y2)")
    
    width = int(bbox[2] - bbox[0])
    
    if width <= 0:
        raise ValueError(f"Invalid bounding box width: {width}. Bbox: {bbox}")
    
    return width


def measure_distance(p1, p2):
    """
    Calculates the Euclidean distance between two points.
    
    Args:
        p1 (tuple/list): First point (x, y).
        p2 (tuple/list): Second point (x, y).
        
    Returns:
        float: Distance between the two points.
        
    Raises:
        ValueError: If points format is invalid.
    """
    if not p1 or not p2 or len(p1) < 2 or len(p2) < 2:
        raise ValueError("Both points must have at least 2 coordinates (x, y)")
    
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5


def measure_xy_distance(p1, p2):
    """
    Calculates the x and y distance between two points.
    
    Args:
        p1 (tuple/list): First point (x, y).
        p2 (tuple/list): Second point (x, y).
        
    Returns:
        tuple: (x_distance, y_distance).
        
    Raises:
        ValueError: If points format is invalid.
    """
    if not p1 or not p2 or len(p1) < 2 or len(p2) < 2:
        raise ValueError("Both points must have at least 2 coordinates (x, y)")
    
    return (p1[0] - p2[0]), (p1[1] - p2[1])

def get_foot_position(bbox):
    """
    Returns the foot position (bottom center) of a bounding box.
    
    Args:
        bbox (tuple/list): Bounding box coordinates (x1, y1, x2, y2).
        
    Returns:
        tuple: (center_x, bottom_y) coordinates.
        
    Raises:
        ValueError: If bbox format is invalid.
    """
    if not bbox or len(bbox) != 4:
        raise ValueError("bbox must contain exactly 4 coordinates (x1, y1, x2, y2)")
    
    x1, y1, x2, y2 = bbox
    
    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"Invalid bounding box: x2 must be > x1 and y2 must be > y1. Got: {bbox}")
    
    return int((x1 + x2) / 2), int(y2)
