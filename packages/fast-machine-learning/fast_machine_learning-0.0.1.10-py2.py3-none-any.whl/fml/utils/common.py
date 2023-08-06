
def linspace(start, end, step, dtype=float, decimal=None):
    
    data = []
    while start < end:
        start = dtype(start)
        if dtype is float and decimal is not None:
            start = round(start, decimal)
        data.append(start)
        start += step
    
    return data