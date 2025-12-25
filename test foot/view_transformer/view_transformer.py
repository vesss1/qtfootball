import numpy as np
import cv2

class ViewTransformer():
    def __init__(self,):
        court_width = 68
        court_length = 23.32

        self.pixel_verticies = np.array([
            [110, 1035],
            [265, 275],
            [910, 260],
            [1640, 950],
        ])

        self.target_verticies = np.array([
            [0, court_width],
            [0,0],
            [court_length, 0],
            [court_length,court_width],
        ])

        self.pixel_verticies = self.pixel_verticies.astype(np.float32)
        self.target_verticies = self.target_verticies.astype(np.float32)

        self.perspective_transformer = cv2.getPerspectiveTransform(self.pixel_verticies, self.target_verticies)

    
    def transform_point(self, point):
        """
        Transforms a point using perspective transformation.
        
        Args:
            point: Point coordinates (numpy array or tuple).
            
        Returns:
            Transformed point coordinates or None if point is outside bounds.
            
        Raises:
            ValueError: If point format is invalid.
        """
        if point is None:
            return None
        
        # Check if point is a numpy array or convert from tuple/list
        if isinstance(point, np.ndarray):
            if point.size < 2:
                raise ValueError("point must have at least 2 coordinates")
        elif isinstance(point, (tuple, list)):
            if len(point) < 2:
                raise ValueError("point must have at least 2 coordinates")
            point = np.array(point)
        else:
            raise ValueError("point must be a numpy array, tuple, or list")
        
        p = (int(point[0]), int(point[1]))
        is_inside = cv2.pointPolygonTest(self.pixel_verticies, p, False) >= 0
        if not is_inside:
            return None
        
        reshaped_point = point.reshape(-1,1,2).astype(np.float32)
        transform_point = cv2.perspectiveTransform(reshaped_point, self.perspective_transformer)

        return transform_point.reshape(-1,2)

    
    def add_transformed_position_to_tracks(self, tracks):
        """
        Adds transformed positions to all tracks.
        
        Args:
            tracks (dict): Dictionary containing tracked objects.
            
        Raises:
            ValueError: If tracks is invalid.
        """
        if not tracks or not isinstance(tracks, dict):
            raise ValueError("tracks must be a non-empty dictionary")
        
        for object, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    if 'position_adjusted' not in track_info:
                        continue
                        
                    position = track_info['position_adjusted']
                    
                    if position is None:
                        tracks[object][frame_num][track_id]["position_transformed"] = None
                        continue
                    
                    position = np.array(position)
                    position_transformed = self.transform_point(position)

                    if position_transformed is not None:
                        position_transformed = position_transformed.squeeze().tolist()
                    tracks[object][frame_num][track_id]["position_transformed"] = position_transformed