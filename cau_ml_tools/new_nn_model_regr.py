import sys
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from os import path
from utils import utils



# ----------------------------------------------------------------------------------------------------------------------
# check se i parametri sono stati impostati correttamente e, eventualmente, eseguiamo un parsing dei parametri in stringa

if sys.argv.__len__() != 4:
    raise AttributeError("Wrong argument number. Please insert only 3 arguments.")

aa_ord_id = str(sys.argv[1])
cds_id = str(sys.argv[2])
ad_id = str(sys.argv[3])

# x debug
#aa_ord_id = str(2013)
#cds_id = str(10047)
#ad_id = str(5868)
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

#Conta il numero di record del dataset
print("Number of elements: {}".format(len(subds.index)))

y = subds['voto']  # temp output
x = subds.drop(['voto', 'matr'], axis=1)  # tolgo da input ds voto e matricola
# ----------------------------------------------------------------------------------------------------------------------
# Trasformiamo l'output per poter essere classificato
y = y.values
x = x.values
print(y, x)

# split commentato in quanto viene eseguito automaticamente durante il training tramite l'attributo validation_split
#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units=9, activation='relu'))
ann.add(tf.keras.layers.Dense(units=6, activation='relu'))
ann.add(tf.keras.layers.Dense(units=1))

#Early stopping. Usiamo Patience = 3 basato sulla loss function in testing
callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

ann.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error'])
print("Modello compilato")
history = ann.fit(x, y, validation_split=0.30, batch_size=32, epochs=100000, callbacks=[callback])
print("Modello allenato")
ann.save("{}\\predict_marks\\{}\\{}\\{}".format(my_path, aa_ord_id, cds_id, ad_id))
print("Modello salvato")


#y_pred = ann.predict(x_test)
#np.set_printoptions(precision = 2)
#print(np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), axis=1))
# ----------------------------------------------------------------------------------------------------------------------

# Mostra un plot relativo all'andamento della loss function in training e in testing

plt.plot(history.history['mean_squared_error'])
plt.plot(history.history['val_mean_squared_error'])
plt.title("Loss {} | {} | {}".format(aa_ord_id, cds_id, ad_id))
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

input("Press Enter to continue...")