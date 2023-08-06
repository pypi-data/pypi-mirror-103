import json
import os
import pathlib
import tempfile
import time
from abc import abstractmethod
from typing import Dict, Any

import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, LambdaCallback
from kolibri.backend.tensorflow.embeddings import DefaultEmbedding
from kolibri.backend.tensorflow.utils import load_data_object
from kdmt.dict import nested_dict_has_key, nested_dict_set_key_value, nested_dict_get_key_path
from kolibri.indexers.sequence_indexer import SequenceIndexer
from kolibri.data.generators import DataGenerator
import kolibri.version
from kolibri.indexers.label_indexer import LabelIndexer
from kolibri.logger import get_logger

logger = get_logger(__name__)


class TFBaseModel(object):

    def __init__(self, hyper_parameters={}, embedding=None, sequence_length=None, multi_label=False,content_indexer=None, label_indexer=None):

        self.hyper_parameters = self.get_default_hyper_parameters()
        # combine with base class hyperparameters
        self.hyper_parameters.update(TFBaseModel.get_default_hyper_parameters())

        if hyper_parameters:
            self.update_hyper_parameters(hyper_parameters)

        if embedding is None:
            embedding = DefaultEmbedding()  # type: ignore
        if content_indexer is None:
            content_indexer = SequenceIndexer()

        self.content_indexer = content_indexer
        self.embedding = embedding

        self.epoch = 0
        self.tf_model: tf.keras.Model = None
        self.checkpoint_model_path = ""
        self.sequence_length: int
        self.sequence_length = sequence_length
        self.multi_label = multi_label
        if label_indexer is None:
            self.label_indexer = LabelIndexer(multi_label=multi_label)

    def to_dict(self) -> Dict[str, Any]:
        model_json_str = self.tf_model.to_json()

        return {
            'tf_version': tf.__version__,  # type: ignore
            'kolibri_version': kolibri.version.__version__,
            'label_indexer': self.label_indexer.to_dict(),
            'embedding': self.embedding.to_dict(),  # type: ignore
            'content_indexer': self.content_indexer.to_dict(),
            '__class_name__': self.__class__.__name__,
            '__module__': self.__class__.__module__,
            'epoch': self.epoch,
            'config': {
                'hyper_parameters': self.hyper_parameters,  # type: ignore
            },
            'tf_model': json.loads(model_json_str)
        }

    def update_hyper_parameters(self, parameters):
        if self.hyper_parameters is None:
            return

        for k, v in parameters.items():
            if nested_dict_has_key(k, self.hyper_parameters):
                key=nested_dict_get_key_path(k,self.hyper_parameters)
                nested_dict_set_key_value(key, self.hyper_parameters, v)

    @classmethod
    def get_default_hyper_parameters(cls):

        return {
            'save_best': False,
            'early_stop': False,
            'monitor': 'val_accuracy',
            'mode': 'max',
            'early_stopping_patience': 3,
            'epochs': 2
        }

    def fit(self, x_train, y_train, x_validate=None, y_validate=None,
            *,
            batch_size: int = 32,
            epochs: int = 5,
            callbacks=None,
            fit_kwargs: Dict = None):

        train_gen = DataGenerator(x_train, y_train)
        if x_validate is not None:
            valid_gen = DataGenerator(x_validate, y_validate)
        else:
            valid_gen = None
        return self.fit_generator(train_sample_gen=train_gen,
                                  valid_sample_gen=valid_gen,
                                  batch_size=batch_size,
                                  callbacks=callbacks,
                                  fit_kwargs=fit_kwargs)


    def build_model_generator(self, generators):
        raise NotImplementedError

    def fit_generator(self, train_sample_gen, valid_sample_gen=None,
                      *,
                      batch_size: int = 64,
                      callbacks=None,
                      fit_kwargs):

        self.build_model_generator([g for g in [train_sample_gen, valid_sample_gen] if g])

        model_summary = []
        self.tf_model.summary(print_fn=lambda x: model_summary.append(x))
        logger.debug('\n'.join(model_summary))

        train_set = train_sample_gen
        train_set.set_batch_size(batch_size)
        train_set.label_indexer = self.label_indexer
        train_set.content_indexer = self.content_indexer

        if fit_kwargs is None:
            fit_kwargs = {}

        if valid_sample_gen:
            valid_gen = valid_sample_gen
            valid_gen.set_batch_size(batch_size)
            valid_gen.label_indexer = self.label_indexer
            valid_gen.content_indexer = self.content_indexer

            fit_kwargs['validation_data'] = valid_gen
            fit_kwargs['validation_steps'] = len(valid_gen)

        def on_epoch_end(_a, _b):
            self.epoch += 1

        if valid_sample_gen is not None:
            if callbacks is None:
                callbacks = []
            if LambdaCallback(on_epoch_end=on_epoch_end) not in callbacks:
                callbacks.append(LambdaCallback(on_epoch_end=on_epoch_end))

            if self.hyper_parameters['save_best']:
                self.checkpoint_model_path = os.path.join(tempfile.gettempdir(), str(time.time()))
                pathlib.Path(self.checkpoint_model_path).mkdir(parents=True, exist_ok=True)
                self.checkpoint_model_path = os.path.join(self.checkpoint_model_path, 'best_weights.h5')
                callbacks.append(
                    ModelCheckpoint(filepath=self.checkpoint_model_path, monitor=self.hyper_parameters['monitor'],
                                    save_best_only=True, verbose=1, mode=self.hyper_parameters['mode']))
            if self.hyper_parameters['early_stop']:
                callbacks.append(EarlyStopping(monitor=self.hyper_parameters['monitor'],
                                               patience=self.hyper_parameters['early_stopping_patience']))

        history = self.tf_model.fit(train_sample_gen,
                                    steps_per_epoch=len(train_sample_gen),
                                    epochs=self.epoch + self.hyper_parameters['epochs'],
                                    initial_epoch=self.epoch,
                                    callbacks=callbacks,
                                    **fit_kwargs)
        if os.path.exists(self.checkpoint_model_path):
            self.tf_model.load_weights(self.checkpoint_model_path)

        return self.tf_model


    def save(self, model_path: str) -> str:
        """
        Save model
        Args:
            model_path:
        """
        pathlib.Path(model_path).mkdir(exist_ok=True, parents=True)
        model_path = os.path.abspath(model_path)
        with open(os.path.join(model_path, 'model_config.json'), 'w') as f:
            info_dict = self.to_dict()
            f.write(json.dumps(info_dict, indent=2, default=str, ensure_ascii=False))
            f.close()

        self.tf_model.save_weights(os.path.join(model_path, 'model_weights.h5'))  # type: ignore
        logger.info('model saved to {}'.format(os.path.abspath(model_path)))
        self.embedding.embed_model.save_weights(os.path.join(model_path, 'embed_model_weights.h5'))
        logger.info('embedding file saved to {}'.format(os.path.abspath(model_path)))
        return model_path


    @classmethod
    def load_model(cls, model_path):
        from kolibri.backend.tensorflow.layers.crf import ConditionalRandomField
        model_config_path = os.path.join(model_path, 'model_config.json')
        with open(model_config_path, 'r') as f:
            model_config = json.loads(f.read())
        model = load_data_object(model_config)

        model.embedding = load_data_object(model_config['embedding'])
        model.content_indexer = load_data_object(model_config['content_indexer'])
        model.label_indexer = load_data_object(model_config['label_indexer'])
        model.epoch = model_config['epoch']
        tf_model_str = json.dumps(model_config['tf_model'])
        model.tf_model = tf.keras.models.model_from_json(tf_model_str,
                                                         {'ConditionalRandomField': ConditionalRandomField})

        if isinstance(model.tf_model.layers[-1], ConditionalRandomField):
            model.layer_crf = model.tf_model.layers[-1]

        model.tf_model.load_weights(os.path.join(model_path, 'model_weights.h5'))
        model.embedding.embed_model.load_weights(os.path.join(model_path, 'embed_model_weights.h5'))
        return model
    @abstractmethod
    def build_model(self,
                    x_data: Any,
                    y_data: Any) -> None:
        raise NotImplementedError


if __name__ == "__main__":
    path = ''
    m = TFBaseModel.load_model(path)
    m.tf_model.summary()
