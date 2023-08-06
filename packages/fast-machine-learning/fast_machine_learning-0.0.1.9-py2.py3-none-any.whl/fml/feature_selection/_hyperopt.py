
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials, pyll
if __name__ == "__main__":
    from fml.validates import validate_switch
else:
    from ..validates import validate_switch
import numpy as np

def single_hyperopt(X, Y, algo, flen, loo=10):
    
    featurespace = {}
    for fl in range(flen):
        featurespace.update({str(fl): hp.randint(str(fl), X.shape[1])})
    
    trials = Trials()
    
    def f(params):
        print(params)
        result = validate_switch(loo, algo, X[:, np.array(list(params.values()))], Y)
        if len(set(Y)) > 8:
            loss = result["rmse"]
        else:
            loss = 1 / result["accuracy_score"] + 0.0000001
        return {'loss': loss, 'status': STATUS_OK}

    best = fmin(fn=f, space=featurespace, algo=tpe.suggest, max_evals=100, trials=trials)

    return best, f(best)["loss"]

def auto_hyperopt(X, Y, algo, loo=10):
    
    maxflen = X.shape[1]
    
    # try:
    #     pyll.scope.getattr(pyll.scope, "foo")
    #     pyll.scope.undefine("foo")
    # except:
    #     pass
    
    # @pyll.scope.define
    # def foo():
    #     flen = np.random.randint(maxflen)
    #     return np.random.choice(np.arange(flen))
    
    # featurespace = pyll.scope.foo()
    
    featurespace = {}
    featurespace.update(dict(rs=hp.randint("rs", 0, 999999)))
    featurespace.update(dict(maxf=hp.randint("maxf", 2, maxflen)))
    
    trials = Trials()
    
    def f(params):
        print(params)
        
        from sklearn.utils import check_random_state
        rng = check_random_state(params["rs"])
        perm = rng.permutation(maxflen)
        fi = perm[:params["maxf"]]
        
        result = validate_switch(loo, algo, X[:, fi], Y)
        if len(set(Y)) > 8:
            loss = result["rmse"]
        else:
            loss = 1 / result["accuracy_score"] + 0.0000001
        return {'loss': loss, 'status': STATUS_OK, "fi":fi}

    best = fmin(fn=f, space=featurespace, algo=tpe.suggest, max_evals=100, trials=trials)

    return best, f(best)

if __name__ == "__main__":
    from sklearn.datasets import load_boston
    import xgboost; algo = xgboost.XGBRegressor
    dataset = load_boston()
    X = dataset.data
    Y = dataset.target
    
    best, loss = single_hyperopt(X, Y, algo, 12, False)
    # best, loss = auto_hyperopt(X, Y, algo, False)