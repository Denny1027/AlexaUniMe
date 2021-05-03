import tensorflow as tf
from .custom_exception import NotFittedException


class _ArtificialNeuralNetwork:

    def __init__(self, name: str, path: str):

        self._path: str = path
        self._name: str = name
        self._nn = tf.keras.Sequential()

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def save_ann(self):
        try:
            self._nn.save(self._path + self._name)
        except ValueError:
            raise NotFittedException("La rete neurale non è stata ancora allenata. Modello non salvato")

    def load_ann(self):
        try:
            self._nn = tf.keras.models.load_model(self._path + self._name)
            print(self._name, " caricato!")
        except (IOError, ImportError):
            print("Errore durante il caricamento di ", self._name, ". Modello non caricato!")

    def train(self, x, y, batch_size=32, epochs=100):
        try:
            self._nn.fit(x, y, batch_size=batch_size, epochs=epochs)
            print("Training eseguito con successo!")
        except RuntimeError:
            print("Training Error: modello non compilato!")
        except ValueError:
            print("Training Error: Dati in input vuoti o del formato errato")

    def predict(self, prediction):
        return self._nn.predict(prediction)