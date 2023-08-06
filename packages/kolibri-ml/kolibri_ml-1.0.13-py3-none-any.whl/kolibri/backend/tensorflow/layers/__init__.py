#from kapre.composed import get_melspectrogram_layer
from tensorflow.python import keras

from kolibri.backend.tensorflow.layers.att_wgt_avg_layer import AttentionWeightedAverage, AttWgtAvgLayer
from kolibri.backend.tensorflow.layers.att_wgt_avg_layer import AttentionWeightedAverageLayer
from kolibri.backend.tensorflow.layers.folding_layer import FoldingLayer
from kolibri.backend.tensorflow.layers.kmax_pool_layer import KMaxPoolingLayer, KMaxPoolLayer, KMaxPooling
from kolibri.backend.tensorflow.layers.non_masking_layer import NonMaskingLayer
from kolibri.backend.tensorflow.layers.multi_head_attention import MultiHeadSelfAttention
#Melspectrogram = get_melspectrogram_layer

L = keras.layers

if __name__ == "__main__":
    print("Hello world")
