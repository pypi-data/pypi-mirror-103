
import sys, numpy as np
if __name__ == "__main__":
    sys.path.append("../")
    from utils import check_2D, check_not_2D
else:
    from ..utils import check_2D, check_not_2D

def del_na_mask(array):
    if check_not_2D(array):
        raise "array must be 2D"
    mask = np.ones(array.shape[1], dtype=bool)
    for col_i, col in enumerate(array.T):
        try:
            col.astype(float)
        except:
            mask[col_i] = False
    return mask

def del_sd_mask(array, sd_criterion=0.00001):
    if check_not_2D(array):
        raise "array must be 2D"
    mask = np.ones(array.shape[1], dtype=bool)
    for col_i, col in enumerate(array.T):
        try:
            if col.astype(float).std() < sd_criterion:
                mask[col_i] = False
        except:
            mask[col_i] = False
    return mask

def del_corr_mask(array, corr_criterion=0.99):
    if check_not_2D(array):
        raise "array must be 2D"
    mask = np.zeros(array.shape[1], dtype=bool)
    corr = np.corrcoef(array.T)
    brackets = {}
    brackets[0] = [0]
    for col_i in range(1, array.shape[1]):
        new = True
        stop = False
        for index, bracket in brackets.items():
            for col_b_i in bracket:
                corr_ = corr[col_i, col_b_i]
                if np.abs(corr_) >= corr_criterion:
                    brackets[index].append(col_i)
                    stop = True
                    new = False
                    break
            if stop:
                break
        if new:
            brackets[len(brackets)] = [col_i]
    values = [ i[0] for i in brackets.values() ]
    mask[values] = True
    
    return mask

if __name__ == "__main__":
    
    from sklearn.datasets import make_regression
    X, Y = make_regression(n_samples=250, n_features=2500, n_informative=25, 
                           n_targets=1, noise=0.1, random_state=0)
    
    from fml.dataobject import ReadData
    from luktianutl.preprocessing import del_corr_mask as dcm
    df = ReadData("Y://研究生期间其他工作//邵月月//新建文件夹 (3)//fp.txt")().to_df()
    X = df.iloc[:, 4:].values
    X = X[:, del_sd_mask(X)].astype(float)
    # mask = del_corr_mask(X, 0.95)
    mask = dcm(X, 0.95)
    X = X[:, mask]
