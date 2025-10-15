"""If a recursive call may start two other recursive call, we call this a binary recursion"""

def binary_sum(S, start, stop):
    """Return the sum of the numbers in implicit slice S[start:stop]"""
    if start >= stop:       # zero elements in slice
        return 0
    elif start == stop - 1:  # One elements in slice
        return S[start]
    else:
        mid = (start + stop) // 2
        return binary_sum(S,start,mid) + binary_sum(S,mid,stop)