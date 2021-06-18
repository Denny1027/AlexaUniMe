import sys

import pandas as pd

from os import path
from utils import regr_tester as rt, utils

# ----------------------------------------------------------------------------------------------------------------------
# check se i parametri sono stati impostati correttamente e, eventualmente,
# eseguiamo un parsing dei parametri in stringa

if sys.argv.__len__() != 3:
    raise AttributeError("Wrong argument number. Please insert only 2 arguments.")

cds_id = str(sys.argv[1])
ad_id = str(sys.argv[2])

# ----------------------------------------------------------------------------------------------------------------------
# Ricaviamo dal file config.yaml il path di riferimento

my_path = utils.get_path()

# ----------------------------------------------------------------------------------------------------------------------
# Check se esiste la directory dove prelevare il dataset richiesto, altrimenti lancia un errore
if not path.exists("{}/subscr_guess/{}.csv".format(my_path, cds_id)):
    raise FileNotFoundError("Reference dataset not exist. It must be in {}\\datasets\\{}.csv".format(my_path,
                                                                                                     cds_id))

# ----------------------------------------------------------------------------------------------------------------------
# filtro dataset per ad_id e divido in x(input) e y(output)
ds = pd.read_csv("{}/subscr_guess/{}.csv".format(my_path, cds_id), sep=';')
ds = ds.loc[ds["ad_id"] == int(ad_id)]

if ds.empty:
    raise ValueError("Empty dataframe. Abort.")

x = ds.iloc[:, 1:-1].values
y = ds.iloc[:, -1].values

# ----------------------------------------------------------------------------------------------------------------------
# Inizio Analisi
score_type = "r2_score"

""" ATTENZIONE! Non considerare r2_score per regressione non lineare.
    Guardare invece la mean_squared_error (Errore quadratico medio) """

# Introduction
print("*******************************************")
print("  REGRESSOR FINDER")
print("*******************************************\n")

json_results = {}
methods_name = ('simple_linear', 'poly_regr', 'support_vector_regressor', 'decision_tree', 'random_forest')
methods = [rt.__simple_linear_regression(x, y, score_type, 0.2),
           rt.__poly_linear_regression(x, y, score_type),
           rt.__support_vector_regressor(x, y, score_type),
           rt.__decision_tree_regressor(x, y, score_type),
           rt.__random_forest_regressor(x, y, score_type)
           ]

for i in range(len(methods_name)):
    json_results[methods_name[i]] = methods[i]

input("Press Enter to continue...")