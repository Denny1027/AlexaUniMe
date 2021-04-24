import tensorflow as tf


class ArtificialNeuralNetwork:

    def __init__(self, name):
        self._nn = tf.keras.models.Sequential()
        #cerca se esiste un modello già salvato. Se esiste caricalo, altrimenti creane uno nuovo
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def create_ann(self):
        pass

    def save_ann(self):
        self._nn.save('./ml_classes/ml_modules/' + self._name)

    def load_ann(self):
        try:
            self._nn = tf.keras.models.load_model('./ml_classes/ml_modules/' + self._name)
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


class ClassificatorNeuralNetwork(ArtificialNeuralNetwork):

    def __init__(self, name):
        super().__init__(name)

    def __init__(self, *args, name):
        super().__init__(name)

        if len(args) <= 1:
            print("Numero di layers insufficienti. ANN vuota. Inserire almeno 1 hidden layer e 1 output layer")
            return

        loss_funct = 'categorical_crossentropy'
        activation = 'softmax'
        if args[-1] == 1: #binary
            loss_funct = 'binary_crossentropy'
            activation = 'sigmoid'

        for arg in args[:-1]:
            self._nn.add(tf.keras.layers.Dense(units=arg, activation='relu'))
        self._nn.add(tf.keras.layers.Dense(units=args[-1], activation=activation))

        print("ANN creata con successo!")
        print("dimensione: {} hidden {}; Dimensione output: {}".format(len(args[:-1]), args[:-1], args[-1]))
        self._nn.compile(optimizer='adam', loss=loss_funct, metrics=['accuracy'])
        print("ANN compilato con successo: LossFunction = ", loss_funct)

    def create_ann(self, *args):
        if len(args) <= 1:
            print("Numero di layers insufficienti. ANN vuota. Inserire almeno 1 hidden layer e 1 output layer")
            return False

        loss_funct = 'categorical_crossentropy'
        activation = 'softmax'
        if args[-1] == 1: #binary
            loss_funct = 'binary_crossentropy'
            activation = 'sigmoid'

        for arg in args[:-1]:
            self._nn.add(tf.keras.layers.Dense(units=arg, activation='relu'))

        self._nn.add(tf.keras.layers.Dense(units=args[-1], activation=activation))

        print("ANN creata con successo!")
        print("dimensione: {} hidden {}; Dimensione output: {}".format(len(args[:-1]), args[:-1], args[-1]))
        self._nn.compile(optimizer='adam', loss=loss_funct, metrics=['accuracy'])
        print("ANN compilato con successo: LossFunction = ", loss_funct)
        return True


class RegressorNeuralNetwork(ArtificialNeuralNetwork):
    def __init__(self, name):
        super().__init__(name)

    def __init__(self, *args, name):
        super().__init__(name)

        if len(args) <= 1:
            print("Numero di layers insufficienti. ANN vuota. Inserire almeno 1 hidden layer e 1 output layer")
            return

        for arg in args[:-1]:
            self._nn.add(tf.keras.layers.Dense(units=arg, activation='relu'))
        self._nn.add(tf.keras.layers.Dense(units=args[-1]))

        print("ANN creata con successo!")
        print("dimensione: {} hidden {}; Dimensione output: {}".format(len(args[:-1]), args[:-1], args[-1]))
        self._nn.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error'])
        print("ANN compilato con successo: LossFunction = 'mean_squared_error'")

    def create_ann(self, *args):
        if len(args) <= 1:
            print("Numero di layers insufficienti. ANN vuota. Inserire almeno 1 hidden layer e 1 output layer")
            return False

        for arg in args[:-1]:
            self._nn.add(tf.keras.layers.Dense(units=arg, activation='relu'))

        self._nn.add(tf.keras.layers.Dense(units=args[-1]))

        print("ANN creata con successo!")
        print("dimensione: {} hidden {}; Dimensione output: {}".format(len(args[:-1]), args[:-1], args[-1]))
        self._nn.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error'])
        print("ANN compilato con successo: LossFunction = 'mean_squared_error'")
        return True