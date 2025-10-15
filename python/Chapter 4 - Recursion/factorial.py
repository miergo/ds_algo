def factorial(n):
    if n == 0:
        return 1
    
    result = n * factorial(n-1)
    print(f"factorial {n}: {result}")
    
    return  result

if  __name__ == "__main__":
    
    factorial(0)