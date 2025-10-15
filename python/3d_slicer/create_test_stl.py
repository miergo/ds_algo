import numpy as np
import struct

def create_cube_stl(size=20, filename="test_cube.stl"):
    """Create a simple cube STL file for testing"""
    
    # Define cube vertices
    half_size = size / 2
    vertices = [
        [-half_size, -half_size, 0],      # 0: bottom front left
        [half_size, -half_size, 0],       # 1: bottom front right
        [half_size, half_size, 0],        # 2: bottom back right
        [-half_size, half_size, 0],       # 3: bottom back left
        [-half_size, -half_size, size],   # 4: top front left
        [half_size, -half_size, size],    # 5: top front right
        [half_size, half_size, size],     # 6: top back right
        [-half_size, half_size, size]     # 7: top back left
    ]
    
    # Define triangles (2 per face, 12 total)
    triangles = [
        # Bottom face (Z=0)
        [0, 2, 1], [0, 3, 2],
        # Top face (Z=size)
        [4, 5, 6], [4, 6, 7],
        # Front face (Y=-half_size)
        [0, 1, 5], [0, 5, 4],
        # Back face (Y=half_size)
        [2, 3, 7], [2, 7, 6],
        # Left face (X=-half_size)
        [0, 4, 7], [0, 7, 3],
        # Right face (X=half_size)
        [1, 2, 6], [1, 6, 5]
    ]
    
    # Write binary STL file
    with open(filename, 'wb') as f:
        # Write header (80 bytes)
        header = b"Binary STL created by Python 3D Slicer" + b"\0" * 41
        f.write(header)
        
        # Write number of triangles
        f.write(struct.pack('<I', len(triangles)))
        
        # Write triangles
        for triangle in triangles:
            # Calculate normal vector
            v0 = np.array(vertices[triangle[0]])
            v1 = np.array(vertices[triangle[1]])
            v2 = np.array(vertices[triangle[2]])
            
            edge1 = v1 - v0
            edge2 = v2 - v0
            normal = np.cross(edge1, edge2)
            normal = normal / np.linalg.norm(normal)
            
            # Write normal
            f.write(struct.pack('<fff', normal[0], normal[1], normal[2]))
            
            # Write vertices
            for vertex_idx in triangle:
                vertex = vertices[vertex_idx]
                f.write(struct.pack('<fff', vertex[0], vertex[1], vertex[2]))
                
            # Write attribute byte count (unused)
            f.write(struct.pack('<H', 0))
            
    print(f"Created test STL file: {filename}")

if __name__ == "__main__":
    create_cube_stl()