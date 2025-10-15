import numpy as np
import struct

class Mesh:
    def __init__(self, triangles):
        self.triangles = np.array(triangles)
        self._bounds = None
        self._volume = None
        
    @property
    def bounds(self):
        if self._bounds is None:
            vertices = self.triangles.reshape(-1, 3)
            self._bounds = np.array([vertices.min(axis=0), vertices.max(axis=0)])
        return self._bounds
        
    @property
    def volume(self):
        if self._volume is None:
            # Calculate volume using divergence theorem
            volume = 0.0
            for triangle in self.triangles:
                v0, v1, v2 = triangle
                volume += np.dot(v0, np.cross(v1, v2))
            self._volume = abs(volume) / 6.0
        return self._volume

class STLLoader:
    def __init__(self):
        pass
        
    def load(self, file_path):
        """Load STL file and return Mesh object"""
        with open(file_path, 'rb') as f:
            # Check if binary or ASCII
            header = f.read(80)
            f.seek(0)
            
            # Try to detect ASCII format
            try:
                content = f.read(1024).decode('ascii').lower()
                if 'solid' in content and 'facet' in content:
                    f.seek(0)
                    return self._load_ascii(f)
            except:
                pass
                
            # Load as binary
            f.seek(0)
            return self._load_binary(f)
            
    def _load_binary(self, f):
        """Load binary STL file"""
        # Skip header
        f.read(80)
        
        # Read number of triangles
        triangle_count = struct.unpack('<I', f.read(4))[0]
        
        triangles = []
        for _ in range(triangle_count):
            # Read normal vector (skip it for now)
            f.read(12)
            
            # Read vertices
            triangle = []
            for _ in range(3):
                vertex = struct.unpack('<fff', f.read(12))
                triangle.append(vertex)
            
            triangles.append(triangle)
            
            # Skip attribute byte count
            f.read(2)
            
        return Mesh(triangles)
        
    def _load_ascii(self, f):
        """Load ASCII STL file"""
        triangles = []
        current_triangle = []
        
        for line in f:
            line = line.decode('ascii').strip().lower()
            
            if line.startswith('vertex'):
                coords = line.split()[1:4]
                vertex = [float(x) for x in coords]
                current_triangle.append(vertex)
                
            elif line.startswith('endfacet'):
                if len(current_triangle) == 3:
                    triangles.append(current_triangle)
                current_triangle = []
                
        return Mesh(triangles)