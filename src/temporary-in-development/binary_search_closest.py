def binary_search(arr, x):
    # https://www.geeksforgeeks.org/python-program-for-binary-search/
    low = 0
    high = len(arr) - 1
    mid = 0
 
    while low <= high:
 
        mid = (high + low) // 2
        # If we at the highest index, check if we have found the value in range
        if mid + 1 == len(arr):
            if arr[mid] >= x:
                return mid
            else:
                return -1
        
        # If our current value lies between 2 points, then we have found the correct range.
        if arr[mid] <= x and arr[mid + 1] > x:
            return mid
        
        # If x is greater, ignore left half
        elif arr[mid] < x:
            low = mid + 1
 
        # If x is smaller, ignore right half
        elif arr[mid] > x:
            high = mid - 1
 
       
 
    # If we reach here, then the element was not present
    return -1