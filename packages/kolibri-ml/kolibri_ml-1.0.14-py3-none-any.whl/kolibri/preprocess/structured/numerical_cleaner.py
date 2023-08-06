from kolibri.core.component import Component
from kdmt.dict import update
from sklearn.preprocessing import StandardScaler



class NumericalCleaner(Component):
    name = "numerical_cleaner"

    provides = ["features"]
    hyperparameters= {
        "fixed": {
            "scaler": "standard", #or "min-max"
            "remove-outliers": False,
            "binarize": False,
        },

        "tunable": {
        }
    }

    def __init__(self, config={}):
        self.hyperparameters=update(self.hyperparameters, Component.hyperparameters)
        super().__init__(config)
        self.scaler=StandardScaler()


    def fit(self, X, y):
        self.scaler.fit(X, y)
    def transform(self, X):
        return self.scaler.transform(X)

    def fit_transform(self, X, y):
        return self.scaler.fit_transform(X, y)




from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(NumericalCleaner.name, NumericalCleaner)
