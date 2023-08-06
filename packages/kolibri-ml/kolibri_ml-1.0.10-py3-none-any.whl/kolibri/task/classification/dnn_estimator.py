import joblib

from kolibri.backend.base.estimator import BaseEstimator
from kolibri.logger import get_logger
from kdmt.dict import update
from kolibri.config import TaskType
from kolibri.indexers.label_indexer import LabelIndexer
from sklearn.model_selection import train_test_split
from kolibri.evaluators.evaluator import ClassifierEvaluator
from kolibri.backend.tensorflow.embeddings import DefaultEmbedding, WordEmbedding
from sklearn.utils import class_weight
import numpy as np
from kdmt.objects import class_from_module_path
from copy import deepcopy
import os


logger = get_logger(__name__)

KOLIBRI_MODEL_FILE_NAME = "classifier_kolibri.pkl"
DNN_MODEL_FILE_NAME = "classifier_dnn"


class DnnEstimator(BaseEstimator):
    """classifier using the sklearn framework"""

    _estimator_type = 'estimator'

    name = 'dnn_classifier'

    provides = []

    requires = []

    hyperparameters = {

        "fixed":{
            # the models used in the classifier if several models are given they will be combined
            "embeddings": "default",
            "sequence_length": 'auto',
            "epochs": 1,
            "loss": 'categorical_crossentropy',
            "test_size": 0.3
        },
        "tunable":{

        }
    }

    def __init__(self, hyperparameters=None):
        """Construct a new class classifier using the sklearn framework."""
        self.hyperparameters=update(self.hyperparameters, BaseEstimator.hyperparameters)
        super().__init__(params=hyperparameters)

        self.indexer = LabelIndexer(multi_label=self.get_prameter("multi-label"))

        if self.get_prameter('embeddings') == 'default':
            self.embeddings = DefaultEmbedding(task=TaskType.CLASSIFICATION,
                                               sequence_length=self.get_prameter("sequence_length"),
                                               indexer=self.indexer)
        elif self.get_prameter('embeddings') == 'word':
            self.embeddings = WordEmbedding(w2v_path=self.get_prameter("embedding_path"),
                                            task=TaskType.CLASSIFICATION,
                                            sequence_length=self.get_prameter("sequence_length"),
                                            indexer=self.indexer)
        elif self.get_prameter('embeddings') == None:
            self.embeddings = None

        self.model = self.load_model_from_parameters(self.get_prameter("model"))

        self.classifier_type = type(self.model)


    def load_model_from_parameters(self, model_params):
        model_params=deepcopy(model_params)
        model=class_from_module_path(model_params["class"])
        default_params={p:model_params["parameters"][p]["value"] for p in model_params["parameters"]}
        for param, param_val in default_params.items():
            if isinstance(param_val, list):
                for i, p in enumerate(param_val):
                    if isinstance(p, dict):
                        default_params[param][i]=self.load_model_from_parameters(p)
            elif isinstance(param, dict):
                default_params[param] = self.load_model_from_parameters(param_val)

        return model(default_params)


    @classmethod
    def required_packages(cls):
        return ["tensorflow"]

    def fit(self, X, y, X_validation=None, y_validation=None, **kwargs):
        fit_kwargs = {}
        if self.get_prameter('class-weight'):
            class_weights = class_weight.compute_class_weight('balanced',
                                                              np.unique(y),
                                                              y)
            fit_kwargs = {"class_weight": class_weights}

        if X_validation ==None or y_validation==None:
            X, X_val, y,y_val = train_test_split(X, y, test_size=self.get_prameter("test_size"))

        self.model.fit(X, y, x_validate=X_validation, y_validate=y_validation, epochs=self.get_prameter("epochs"),
                     fit_kwargs=fit_kwargs)

        if self.get_prameter('evaluate-performance') and X_validation is not None and y_validation is not None:
            y_pred=self.model.predict(X_validation)
            self.performace_scores=ClassifierEvaluator.get_performance_report(y_validation, y_pred, target_names=list(self.indexer.vocab2idx.keys()))


    def __getstate__(self):
        """Return state values to be pickled."""
        return (self.hyperparameters, self.classifier_type, self.indexer)

    def __setstate__(self, state):
        """Restore state from the unpickled state values."""
        self.hyperparameters, self.classifier_type, self.indexer = state


    def predict(self, X):
        """Given a bow vector of an input text, predict most probable label.

        Return only the most likely label.

        :param X: bow of input text
        :return: tuple of first, the most probable label and second,
                 its probability."""
        probabilities=[]
        raw_predictions, classes, probabilities=self.model.predict_proba(X)


        return self.process([list(zip(classe, probability)) for classe, probability in zip(classes, probabilities)])

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):

        meta = model_metadata.for_component(cls.name)
        classifier_file_name = meta.get("classifier_file", KOLIBRI_MODEL_FILE_NAME)
        dnn_file_name = meta.get("dnn_file", DNN_MODEL_FILE_NAME)
        classifier_file = os.path.join(model_dir, classifier_file_name)
        if os.path.exists(classifier_file):
            # Load saved model
            model = joblib.load(classifier_file)

            clf = model.classifier_type.load_model(os.path.join(model_dir, dnn_file_name))

            model.model = clf
            model.multi_label=model.get_prameter("multi-label")
            model.multi_label_threshold=model.get_prameter("multi-label-threshold")
            return model
        else:
            return cls(meta)

    def persist(self, model_dir):
        """Persist this model into the passed directory.

        Returns the metadata necessary to load the model again."""
        classifier_file = os.path.join(model_dir, KOLIBRI_MODEL_FILE_NAME)
        joblib.dump(self, classifier_file)
        dnn_file = os.path.join(model_dir, DNN_MODEL_FILE_NAME)
        if self.model:
            self.model.save(dnn_file)


        return {"classifier_file": KOLIBRI_MODEL_FILE_NAME, "dnn_file": DNN_MODEL_FILE_NAME,  "performace_scores": self.performace_scores,}



from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(DnnEstimator.name, DnnEstimator)


