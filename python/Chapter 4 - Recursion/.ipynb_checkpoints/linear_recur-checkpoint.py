


""" If a recursive call starts at most one other, we call this a linear recursion
"""

def linear_sum(S,n):
    """Return the sum of the first n numbers of sequence S."""
    if n == 0:
        return 0
    else:
        return linear_sum(S,n - 1) + S[ n-1]
    

def reverse(S,start,stop):
    """Reverse elements in implicit slice S[start:stop]"""

    if start < stop - 1:
        S[start], S[stop - 1] = S[stop - 1], S[start]
        reverse(S, start + 1, stop - 1)
  
        
def power (x,n):
    """Compute the value x**n for integer n"""
    if n == 0:
        return 1
    else:
        return x*power(x,n-1)



if __name__ == "__main__":
    
    data = [4,3,8,7,2]

    # sum of data values
    sum = linear_sum(data,len(data))
    print(sum)
    
    # Reverse list
    reverse(data, 0, len(data))
    print(data)
    
    
    print(power(2,13))