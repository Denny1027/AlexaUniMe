import sys
import json

import numpy
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from os import path
from utils import utils
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


# ----------------------------------------------------------------------------------------------------------------------
# check se i parametri sono stati impostati correttamente e, eventualmente, eseguiamo un parsing dei parametri in stringa

#if sys.argv.__len__() != 4:
#    raise AttributeError("Wrong argument number. Please insert only 3 arguments.")

#aa_ord_id = str(sys.argv[1])
#cds_id = str(sys.argv[2])
#ad_id = str(sys.argv[3])

aa_ord_id = str(2013)
cds_id = str(10047)
ad_id = str(5868)
# ----------------------------------------------------------------------------------------------------------------------
# Ricaviamo dal file config.yaml il path di riferimento

my_path = utils.get_path()

# ----------------------------------------------------------------------------------------------------------------------
# Check se esiste la directory dove prelevare il dataset richiesto, altrimenti lancia un errore
if not path.exists("{}\\datasets\\{}\\{}.csv".format(my_path, aa_ord_id, cds_id)):
    raise FileNotFoundError("Starting dataset not exist. It must be in {}\\datasets\\{}\\{}.csv".format(my_path,
                                                                                                        aa_ord_id,
                                                                                                        cds_id))

# ----------------------------------------------------------------------------------------------------------------------
# Carica il file e filtra gli elementi utili per la creazione del modello

ds = pd.read_csv("{}\\datasets\\{}\\{}.csv".format(my_path, aa_ord_id, cds_id), sep=";")
ds = utils.clean_null_columns(ds)
ds.reset_index(inplace=True)

subds = None
try:
    subds = ds[["matr", "pond", "eta_iscr", str(ad_id), "{}_year".format(ad_id)]]
except KeyError:
    raise KeyError("adId not found. You cannot create a model for this teching activity because there are no data about it.")


subds = subds.dropna(subset=[str(ad_id), "{}_year".format(ad_id)])
subds = subds.reset_index(drop=True)
subds = subds.rename(columns={str(ad_id): "voto", "{}_year".format(ad_id): "anno_esec"})

y = subds['voto']  # temp output
x = subds.drop(['voto', 'matr'], axis=1)  # tolgo da input ds voto e matricola
# ----------------------------------------------------------------------------------------------------------------------
# Trasformiamo l'output per poter essere classificato

tempy = list()

for el in y:
    output_el = [0 for x in range(13)]
    output_el[int(el) - 18] = 1
    tempy.append(output_el)

tempy = numpy.array(tempy)

# Siccome il risultato esce codificato in quanto andrò ad eseguire il OneHotEncoder sull'output
# mi creo un dizionario che mi permette di individuare il voto, dipendentemente dalla posizione
# del valore nell'output. Questo dizionario lo salverò in un json
lungh_out = len(tempy)

ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units=13 * 3, activation='relu'))
ann.add(tf.keras.layers.Dense(units=13 * 2, activation='relu'))
ann.add(tf.keras.layers.Dense(units=13, activation='softmax'))

#callback1 = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=5)
callback2 = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

ann.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print("Modello compilato")
history = ann.fit(x, tempy, validation_split=0.25, epochs=100, batch_size=lungh_out, verbose=1, callbacks=[callback2])
print("Modello trainato")
ann.save("{}\\predict_marks\\{}\\{}\\{}".format(my_path, aa_ord_id, cds_id, ad_id))
print("Modello salvato")

#with open("{}\\predict_marks\\{}\\{}\\{}\\output_map.json".format(my_path, aa_ord_id, cds_id, ad_id), 'w') as fp:
#    json.dump(tempy, fp)

# ----------------------------------------------------------------------------------------------------------------------
# Mostra i grafici relativi all'accuratezza e alla loss
# Accuratezza (Accuracy)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Accuracy {} | {} | {}".format(aa_ord_id, cds_id, ad_id))
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

#Loss Function
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("Loss {} | {} | {}".format(aa_ord_id, cds_id, ad_id))
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

#input("Press Enter to continue...")
