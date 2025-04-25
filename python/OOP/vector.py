class Vector:
    """Represent a Vector Class"""
    
    def __init__(self,d):
        """Create d-dimensional vector of zeros"""
        self._coords = [0] * d
        
    def __len__(self):
        """Return dimension of vector """
        return len(self._coords)
    
    def __getitem__(self,j):
        """Return jth coordinates of vector"""
        return self._coords[j]
    
    def __setitem__(self, j, val):
        """ Set jth coordinate to a given value"""
        self._coords[j] = val
        
    def __add__(self,other):
        """Return sum of two vectors"""
        if len(self._coords) != len(other):
            raise ValueError('dimensions must equal to each other')
        result = Vector(len(self))
        for j in range(len(self)):
            result[j] = self._coords[j] + other[j]
        return result 
    
    def __eq__(self, other):
        """Return True if vectors hae the same coordinates as other"""
        return self._coords == other._coords
    
    def __ne__(self, other):
        """Return True if vector differs from other"""
        return not self == other
    
    def __str__(self):
        """Produce string representation of vector"""
        return '<' + str(self._coords)[1:-1] + '>' 
    
    
if __name__ == "__main__":
    v = Vector(5)
    
    print(f'The Vector is {v}')
    
    v[1] = 50
    v[-1] = 1
    
    print(v[4])
    
    u = v + v
    
    print(f"Vector addition of V's to create U: {u}" )
    
    total = 0
    
    for entry in v:
        print(f'Entry: {entry}, v: {v}')
        total += entry 
        print(f"total: {total}")
        
        
    