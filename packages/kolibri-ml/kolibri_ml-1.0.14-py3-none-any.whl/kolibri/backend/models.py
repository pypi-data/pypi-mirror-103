# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:

import numpy as np
import sklearn.svm as svm
from mlxtend.classifier import EnsembleVoteClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn_crfsuite import CRF
from xgboost import XGBClassifier

from kolibri.datasets.ressources import resources
from kdmt.file import read_json_file
from kdmt.objects import class_from_module_path
sklearn_models_path= resources.get('models/sklearn/models.json').path
sklearn_models=read_json_file(sklearn_models_path)

tensoflow_models_path= resources.get('models/kolibri/tensorflow/models.json').path
tensorflow_models=read_json_file(tensoflow_models_path)

n_estimators = 10

def get_model(model_name, weights=None):
    if isinstance(model_name, list):
        models_ = [sklearn_models.get(model, None) for model in model_name]
        if weights is None:
            weights = [1 for model in model_name]
        model_cict={
      "class": "mlxtend.classifier.EnsembleVoteClassifier",
      "parameters": {
        "clfs": {
          "value": models_
        },
        "voting": {
          "value": "soft",
          "type": "categorical",
          "values": ["soft", "hard"]
        },
        "weights": {
          "value": weights
        }
      }
    }

        return model_cict

    else:
        model= sklearn_models.get(model_name, None)
        if model is None:
            model=tensorflow_models.get(model_name.lower(), None)
    return model



if __name__=="__main__":
    models_=["logistic-regression", "knn"]
    models_=[get_model_(m) for m in models_]
    print(models_)