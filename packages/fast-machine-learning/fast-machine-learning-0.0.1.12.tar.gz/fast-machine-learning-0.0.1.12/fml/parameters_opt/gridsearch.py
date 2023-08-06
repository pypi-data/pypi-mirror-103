
import sys, numpy as np
if __name__ == "__main__":
    sys.path.append("..")
    from utils import linspace, split_array, split_range
    from validates import validate_switch
else:
    from ..utils import linspace, split_array, split_range
    from ..validates import validate_switch
from multiprocessing import cpu_count
from joblib import Parallel, delayed
from collections.abc import Iterable
from itertools import product


class GridSearch(object):
    
    def __init__(self, n_jobs=0, verbose=1):
        
        cpus = cpu_count()
        if isinstance(n_jobs, int) and n_jobs > 0 and n_jobs <= cpus:
            self.n_jobs = n_jobs
        else:
            self.n_jobs = round(cpus * 0.8)
            
        self.verbose = verbose
        
    
    def fit(self, flag, algo, X, Y, other_model_dict=dict(), **products_dict):
        
        '''
        flag: True--loo, False--train, cv_number
        '''
        
        if not isinstance(other_model_dict, dict):
            other_model_dict = dict()
        
        for i, j in products_dict.items():
            if not isinstance(j, Iterable):
                raise Exception(f"parameter {i} is not a iterable")
        
        grids = list(product(*products_dict.values()))
        grids = split_range(grids, self.n_jobs)
        self.parameter_names = list(products_dict.keys())
        self.flag = flag
        
        results = Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(
            delayed(self.work_function)(algo, X, Y, index, params, other_model_dict) for index, params in enumerate(grids)
            )
        results = np.concatenate(results, axis=0)
        
        self.grid_result_names = self.parameter_names + ["rmse", "mae", "mse", "r2_score"]
        
        best = results.copy()
        number_parameter = len(products_dict)
        for pname_i in range(4):
            pname_i_ = pname_i + number_parameter
            if pname_i <= 3:
                best = best[best[:, pname_i_] == best[:, pname_i_].min()]
            else:
                best = best[best[:, pname_i_] == best[:, pname_i_].max()]
            if len(best) == 1:
                break
        if len(best) >= 2:
            best = best[0]
        
        self.grid_result = (self.grid_result_names, results, best, )
        
        return self
    
    def work_function(self, algo, X, Y, thread, params, model_dict):
        
        grid_result = []
        
        for param_group in params:
        
            for pname, param in zip(self.parameter_names, param_group):
                model_dict.update({pname: param})
            
            result = validate_switch(self.flag, algo, X, Y, **model_dict)
            
            grid_result += list(param_group)
            
            grid_result += [result["rmse"], result["mae"], result["mse"], result["r2_score"]]
        
            print(grid_result)
        
        grid_result = np.array(grid_result).reshape(-1, len(self.parameter_names)+4)
        
        return grid_result


if __name__ == "__main__":
    
    from sklearn.svm import SVR
    from sklearn.datasets import load_boston
    import numpy as np
    from xgboost import XGBRegressor
    X, Y = load_boston(return_X_y=True)
    # paramters_dict = dict(
    #     C = linspace(1, 20, 1, dtype=int),
    #     epsilon = linspace(0.1, 2.0, 0.1, dtype=float, decimal=1)
    #     )
    
    # gridsearch = GridSearch().fit(10, SVR, X, Y, **paramters_dict)
    # names, results = gridsearch.grid_result
    # c = split_range(list(product(*list(paramters_dict.values()))), 10)
    # c = list(c)
    # gridsearch.work_function(SVR, X, Y, 0, c[0], dict())
    
    gridsearch = GridSearch().fit(10, XGBRegressor, X, Y, **dict(
        n_estimators=linspace(10, 250, 10, dtype=int),
        learning_rate=linspace(0.1, 1, 0.1, decimal=1)
        ))
    names, results = gridsearch.grid_result