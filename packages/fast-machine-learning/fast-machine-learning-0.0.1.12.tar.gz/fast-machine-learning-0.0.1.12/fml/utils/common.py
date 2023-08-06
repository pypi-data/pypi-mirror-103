import numpy as np

def linspace(start, end, step, dtype=float, decimal=None):
    
    data = []
    while start < end:
        start = dtype(start)
        if dtype is float and decimal is not None:
            start = round(start, decimal)
        data.append(start)
        start += step
    
    return data

def split_range(_range, split_number):
    
    step = int(np.ceil(  len(list(_range)) / split_number  ))
    
    for i in range(0, len(_range), step):
        yield _range[i:i+step]

def split_array(_array, split_number):
    
    step = int(np.ceil(  _array.shape[0] / split_number  ))
    
    for i in range(0, _array.shape[0], step):
        yield _array[i:i+step, :]
