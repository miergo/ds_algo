class Range:
    """A class mimics the built in range class"""
     
    def __init__(self,start, stop = None,step = 1):
        """
        Initialize a range instance
        """
        if step == 0:
            raise ValueError("Step cannot be 0")
        
        if  stop is None:           # special case of range(n)
            start, stop = 0, start  # should be treated as if range(0,n)
            
        #calculate the effective length once
        self.__length = max(0, (stop - start + step - 1)//step)
        
        self._start = start
        self._step = step
        
    def __len__(self):
        """Return number of entries in the range"""
        return self.__length
    
    def __getitem__(self,k):
        
        if k<0:
            k += len(self)
        
        if not 0 <= k < self.__length:
            raise IndexError('INDEX OUT OF RANGE')  
        
        return self._start + k * self._step
    
    
    