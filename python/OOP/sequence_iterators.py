class SequenceIterators:
    """An iterator for any of Python sequence types"""
    
    def __init__(self, sequence):
        """Crate an iterator ofr the given sequence"""
        self._seq = sequence    #Keep a reference to the underlying data
        self._k = -1            #will increment to 0 on first call to next
    def __next__(self):
        """Return the next element, or else raise StopIteration error"""                        
        self._k += 1                        # advance to next index
        if self._k < len(self._seq):    
            return self._seq[self._k]       # return the data element
        else:
            raise StopIteration()   # there are no more elements
            
            
    def __iter__(self):
        """By convention an iteror must return itself"""
        return self
        
if __name__ == "__main__":
    l = [1,2,4]
    seq_num = SequenceIterators(l)
    
    for num in seq_num:
        print(num)
        
    st = "hello"
    seq_str = SequenceIterators(st)
    for char in seq_str:
        print(char)