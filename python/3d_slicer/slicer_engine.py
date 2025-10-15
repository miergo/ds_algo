import numpy as np
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union, polygonize
import math

class Layer:
    def __init__(self, z_height, perimeters=None, infill_lines=None):
        self.z_height = z_height
        self.perimeters = perimeters or []
        self.infill_lines = infill_lines or []

class SlicerEngine:
    def __init__(self):
        pass
        
    def slice(self, mesh, layer_height, progress_callback=None):
        """Slice mesh into layers"""
        bounds = mesh.bounds
        min_z, max_z = bounds[0][2], bounds[1][2]
        
        # Calculate layer positions
        layer_count = int(math.ceil((max_z - min_z) / layer_height))
        layers = []
        
        for i in range(layer_count):
            if progress_callback:
                progress_callback((i / layer_count) * 100)
                
            z = min_z + i * layer_height
            layer = self._slice_at_z(mesh, z)
            layers.append(layer)
            
        return layers
        
    def _slice_at_z(self, mesh, z):
        """Create a layer by slicing the mesh at given Z height"""
        intersections = []
        
        # Find all triangle intersections with the Z plane
        for triangle in mesh.triangles:
            intersection = self._triangle_plane_intersection(triangle, z)
            if intersection is not None:
                intersections.append(intersection)
                
        # Convert intersections to polygons
        perimeters = self._lines_to_polygons(intersections)
        
        # Generate infill for each polygon
        infill_lines = []
        for polygon in perimeters:
            infill = self._generate_infill(polygon, z)
            infill_lines.extend(infill)
            
        return Layer(z, perimeters, infill_lines)
        
    def _triangle_plane_intersection(self, triangle, z):
        """Find intersection between triangle and horizontal plane at Z"""
        v0, v1, v2 = triangle
        
        # Check which vertices are above/below the plane
        z_coords = [v0[2], v1[2], v2[2]]
        vertices = [v0, v1, v2]
        
        # Find intersections with plane
        intersections = []
        
        for i in range(3):
            j = (i + 1) % 3
            z1, z2 = z_coords[i], z_coords[j]
            
            # Check if edge crosses the plane
            if (z1 <= z <= z2) or (z2 <= z <= z1):
                if abs(z1 - z2) > 1e-10:  # Avoid division by zero
                    t = (z - z1) / (z2 - z1)
                    intersection = [
                        vertices[i][0] + t * (vertices[j][0] - vertices[i][0]),
                        vertices[i][1] + t * (vertices[j][1] - vertices[i][1]),
                        z
                    ]
                    intersections.append(intersection[:2])  # Only X, Y coordinates
                    
        # Remove duplicates and return line segment if we have exactly 2 points
        unique_intersections = []
        for point in intersections:
            is_duplicate = False
            for existing in unique_intersections:
                if abs(point[0] - existing[0]) < 1e-6 and abs(point[1] - existing[1]) < 1e-6:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_intersections.append(point)
                
        if len(unique_intersections) == 2:
            return unique_intersections
        return None
        
    def _lines_to_polygons(self, lines):
        """Convert line segments to closed polygons"""
        if not lines:
            return []
            
        polygons = []
        
        # For simple shapes like cubes, we can build polygons by connecting line segments
        if len(lines) >= 3:
            try:
                # First, try the shapely polygonize function
                line_strings = [LineString(line) for line in lines if len(line) >= 2]
                if line_strings:
                    result = list(polygonize(line_strings))
                    polygons.extend([p for p in result if p.is_valid and not p.is_empty])
                    
                # If polygonize didn't work, try a simpler approach
                if not polygons:
                    # Collect all points and try to form a polygon
                    all_points = []
                    for line in lines:
                        all_points.extend(line)
                    
                    if len(all_points) >= 6:  # At least 3 points (x,y pairs)
                        # Remove duplicates while preserving order
                        unique_points = []
                        for point in all_points:
                            is_duplicate = False
                            for existing in unique_points:
                                if abs(point[0] - existing[0]) < 1e-6 and abs(point[1] - existing[1]) < 1e-6:
                                    is_duplicate = True
                                    break
                            if not is_duplicate:
                                unique_points.append(point)
                        
                        if len(unique_points) >= 3:
                            # Sort points to form a proper polygon (convex hull approach)
                            center_x = sum(p[0] for p in unique_points) / len(unique_points)
                            center_y = sum(p[1] for p in unique_points) / len(unique_points)
                            
                            def angle_from_center(point):
                                return math.atan2(point[1] - center_y, point[0] - center_x)
                            
                            sorted_points = sorted(unique_points, key=angle_from_center)
                            
                            try:
                                polygon = Polygon(sorted_points)
                                if polygon.is_valid and not polygon.is_empty:
                                    polygons.append(polygon)
                            except:
                                pass
                                
            except Exception as e:
                print(f"Error in _lines_to_polygons: {e}")
                pass
                
        return polygons
        
    def _generate_infill(self, polygon, z, density=0.2, line_spacing=2.0):
        """Generate infill lines for a polygon"""
        if not polygon.is_valid or polygon.is_empty:
            return []
            
        infill_lines = []
        bounds = polygon.bounds
        min_x, min_y, max_x, max_y = bounds
        
        # Generate horizontal infill lines
        y = min_y
        line_direction = 1  # Alternate direction for better print quality
        
        while y <= max_y:
            if line_direction > 0:
                line = LineString([(min_x - 1, y), (max_x + 1, y)])
            else:
                line = LineString([(max_x + 1, y), (min_x - 1, y)])
                
            try:
                intersection = polygon.intersection(line)
                
                if intersection.geom_type == 'LineString':
                    coords = list(intersection.coords)
                    if len(coords) >= 2:
                        infill_lines.append(coords)
                elif intersection.geom_type == 'MultiLineString':
                    for line_seg in intersection.geoms:
                        coords = list(line_seg.coords)
                        if len(coords) >= 2:
                            infill_lines.append(coords)
            except:
                pass
                
            y += line_spacing
            line_direction *= -1
            
        return infill_lines


