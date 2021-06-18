import os
import sys
import yaml
import time
import json

import pandas as pd
import requests as rqst

from utils import utils
from datetime import date, datetime

# ----------------------------------------------------------------------------------------------------------------------
# check se i parametri sono stati impostati correttamente e, eventualmente, eseguiamo un parsing dei parametri in stringa
if sys.argv.__len__() != 2:
    raise AttributeError("Wrong argument number. Please insert only 1 argument.")

cds_id = str(sys.argv[1])

# ----------------------------------------------------------------------------------------------------------------------
# Ricaviamo dal file config.yaml il path di riferimento

my_path = utils.get_path()
auth = utils.get_auth_value()

# ----------------------------------------------------------------------------------------------------------------------
# Check se esiste cartella di output. Se non esiste, creala
try:
    os.makedirs("{}/subscr_guess".format(my_path), exist_ok=True)
except PermissionError:
    raise PermissionError("Invalid permissions for folder creation. Check path in config.yaml")

# Creazione del dataframe
column_set = ("ad_id", "anno_esame", "ses_id", "num_iscritti")
new_dataset = pd.DataFrame(columns=column_set)

## CREAZOIONE SET ATTIVITA' DIDATTICHE ##
# Ho l'id del Corso di Studio. Adesso cerco tutte le materie che si sono susseguite
#   da oggi a 10 anni fa e le inserisco all'interno di un set, in modo da non
#   ripetere le stesse materie.

set_ad = set()     # Set di attività didattiche
for year in range(date.today().year, date.today().year - 10, -1):

    print("♣ year {}".format(year))

    temp_req = rqst.get(
        "https://unime.esse3.cineca.it/e3rest/api/offerta-service-v1/offerte/{}/{}/attivita".format(year, cds_id))

    # Controllo se il json con la risposta è vuoto o pieno
    if not temp_req:
        print(" <-> NO aaOffId: jump over")
        continue

    for mat in json.loads(temp_req.text):

        tadid = mat["chiaveAdContCapoGruppo"]["adId"]
        set_ad.add(tadid)

        print("--  ♠ ad_id: {}".format(tadid))

print(" || set_ad created! || ")

## RICERCA NUMERO ISCRITTI E CREAZIONE DATASET
# adesso set_ad è pronto con tutte le materie da qui a 10 anni
#   il prossimo passo è quello di iterare set_ad e, per ogni materia,
#   fare richiesta ad una API con cds_id e con ad_id

print(" || Starting retrieving info || ")
for ad_id in set_ad:

    print("Wait 5 sec")
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)

    print(" ♦ ad_id: {}".format(ad_id))
    temp_req_ad = rqst.get(
        "https://unime.esse3.cineca.it/e3rest/api/calesa-service-v1/appelli/{}/{}/?stato=C&fields=appId".format(cds_id, ad_id),
        headers={"Authorization": auth})

    # Check attributi autenticazione
    if temp_req_ad.status_code == 403:
        raise InterruptedError("Wrong username or password: check into config.yaml")

    json_req = json.loads(temp_req_ad.text)
    if not json_req:
        print(" <-> no-info: jump over".format(ad_id))
        continue

    for el in json_req:
        # Se Se tante appId sono nulle, questo metodo fa così tante richiesta da ricevere, ad un certo punto,
        #   una esclusione (status code = 429) "Too Many Request". A tal punto, ritardiamo di mezzo secondo ogni
        #   richiesta.

        print(" -- ♦  app_id: {}".format(el["appId"]))

        temp_req_app = rqst.get(
            "https://unime.esse3.cineca.it/e3rest/api/calesa-service-v1/appelli/{}/{}/{}".format(cds_id, ad_id, el["appId"]),
            headers={"Authorization": auth})

        json_app = json.loads(temp_req_app.text)
        if not json_app:
            print(" <-> empty: jump over! {}|{}".format(ad_id, el["appId"]))
            continue

        # sarebbe stato meglio avere anche l'ordinale dell'appello in una sessione.
        # Ho cercato ma non c'è modo di ottenere questa info perchè non la considerano;
        #   ci sarebbe appLogId ma non è quello.

        temp_dict = {
            "ad_id": str(ad_id),
            "anno_esame": str(datetime.strptime(json_app["dataInizioApp"], '%d/%m/%Y %H:%M:%S').year),
            "ses_id": str(json_app["sessioni"][0]["sesId"]),
            "num_iscritti": str(json_app["numIscritti"])
        }

        new_dataset = new_dataset.append(temp_dict, ignore_index=True)
        print(" | {}|{} -> perfekt! | ".format(ad_id, el["appId"]))

# FINE RICERCA -> Il dataset è stato riempito.
print("End requests - Saving file {}.csv on {}".format(cds_id, my_path))

new_dataset.to_csv("{}/subscr_guess/{}.csv".format(my_path, cds_id), sep=";", index=False)

print("File saved.")
input("Press Enter to continue...")
