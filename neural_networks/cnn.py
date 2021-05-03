from typing import Tuple
from .custom_exception import *
import tensorflow as tf
from .ann import _ArtificialNeuralNetwork


class NeuralNetworkClassificator(_ArtificialNeuralNetwork):

    def __init__(self, *, name: str, path: str, layers: Tuple[int, ...] = ()):
        """
        This class allows you to create an object containing a neural network classificator defined by a name. The
        methods made available allow to perform training, predictions and to load or save the model. The name plays a
        very important role, since, thanks to it, it is possible to load the model of a specific neural network.
        Attention! Before creating any object through this class, set the path where to load or save any model,
        because the creator automatically searches for the model at the time of its construction.

        :param name: Name of the Neural Network Classificator. Through this name, a saved model can be loaded
        :param layers: Tuple of layers with number of neurons for each layer (ex: 1st -> 8 neur. 2nd -> 7 neur.,
                       outp -> 1 neur.)
        """
        super().__init__(name, path)

        try:
            self._nn = tf.keras.models.load_model(self._path + self._name)
            print(self._name, " caricato!")
        except (IOError, ImportError):
            # modello non trovato. Provvedo alla creazione di una nuova rete neurale SE è stato definito correttamente
            # layers
            if layers or len(layers) > 1:

                ######## CREAZIONE RETE NEURALE #########
                loss_funct = 'categorical_crossentropy'
                activation = 'softmax'
                if layers[-1] == 1:  # binary
                    loss_funct = 'binary_crossentropy'
                    activation = 'sigmoid'

                for arg in layers[:-1]:
                    self._nn.add(tf.keras.layers.Dense(units=arg, activation='relu'))
                self._nn.add(tf.keras.layers.Dense(units=layers[-1], activation=activation))

                print("CNN successfully created!")
                print("dimension: {} -> hidden {} output: {}".format(len(layers[:-1]), layers[:-1], layers[-1]))
                self._nn.compile(optimizer='adam', loss=loss_funct, metrics=['accuracy'])
                print("CNN successfully compiled! LossFunction = ", loss_funct)
                ##### FINE CREAZIONE RETE NEURALE #####

            else:
                raise WrongParameterException()
                # non esiste il modulo con nome "xxx" e non sono stati definiti correttamente i layer

