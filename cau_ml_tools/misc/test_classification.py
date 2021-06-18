import pandas as pd

from os import path
from utils import utils
from test_file.class_tester import class_tester_controller


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
y = y.values
x = x.values


# ----------------------------------------------------------------------------------------------------------------------
# Trasformiamo l'output per poter essere classificato
"""
tempy = list()

for el in y:
    output_el = [0 for x in range(13)]
    output_el[int(el) - 18] = 1
    tempy.append(output_el)

tempy = numpy.array(tempy)
print(tempy, x)
"""
""" ATTENZIONE! Non considerare r2_score per regressione non lineare.
    Guardare invece la mean_squared_error (Errore quadratico medio) """

# ----------------------------------------------------------------------------------------------------------------------
# Start analysis
score_type = "f1_score"



# Introduction
print("*******************************************")
print("  REGRESSOR FINDER")
print("*******************************************\n")

c = class_tester_controller(x, y, score_type=score_type)

input("Press Enter to continue...")
