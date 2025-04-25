from abc import ABCMeta, abstractmethod

class Sequence(metaclass=ABCMeta):
    """Our own version collections.Sequence abstract base class"""
    
    @abstractmethod
    def __len__(self) -> int :
        """"Return the length of the sequence"""
    
    @abstractmethod
    def __getitem__(self, j) -> int:
        """Return the element at index j of the sequence"""
        
    def __contains__(self, val) -> bool:
        """Return True if val found in the sequence; False Otherwise"""
        for j in range(len(self)):
            if self[j] == val:
                return True
        return False
    
    def index(self, val):
        """Return leftmost index at which val is found (or raise ValueError)"""
        for j in range(len(self)):
            if self[j] == val:
                return j
        return ValueError('value not in sequence')
    
    def count(self, val):
        """Return the number of elements equal to given value"""  
        k = 0
        for j in range(len(self)):
            if self[j] == val:
                k += 1
        return k
class Range(Sequence):
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
    

if __name__ == "__main__":
    seq = Range(1,10,2)

    print(f"Range class output:", " ".join(str(i) for i in seq))

        
    print(f"Length of sequence: {len(seq)}", )
    
    print(f"First index in sequence: {seq[1]}")