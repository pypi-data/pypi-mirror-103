import tensorflow as tf

from kdmt.ml.metrics.sequences import get_conll_scores


class ConllCallback(tf.keras.callbacks.Callback):
    """
    A Tensorflow(Keras) Conlleval evaluator.
    Runs the conlleval script for given x and y inputs.
    Prints Conlleval F1 score on the end of each epoch.

    Args:
        x: features matrix
        y: labels matrix
        y_vocab (dict): int-to-str labels lexicon
        batch_size (:obj:`int`, optional): batch size
    """

    def __init__(self, val_gen, batch_size=1):
        super(ConllCallback, self).__init__()
        self.x, self.y = val_gen.get_data()
        self.y_vocab = []
        self.nb_indexers = len(val_gen.label_indexer.label_indexers)
        for indexer in val_gen.label_indexer.label_indexers:
            self.y_vocab.append(indexer.idx2vocab)
        self.bsz = batch_size

    def on_epoch_end(self, epoch, logs=None):
        predictions = self.model.predict(self.x, batch_size=self.bsz)
        for i in range(self.nb_indexers):
            stats = get_conll_scores(predictions[i], self.y[i], self.y_vocab[i])
            print()
            print("Evaluation: \n{}".format(stats))
