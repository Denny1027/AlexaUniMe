import os
import sys
import json
import time

import pandas as pd
import requests as rqst


from utils import utils


# ----------------------------------------------------------------------------------------------------------------------
# check se i parametri sono stati impostati correttamente e, eventualmente,
# eseguiamo un parsing dei parametri in stringa
if sys.argv.__len__() != 3:
    raise AttributeError("Wrong argument number. Please insert only 2 argument.")

aa_ord_id = str(sys.argv[1])
cds_id = str(sys.argv[2])
# ----------------------------------------------------------------------------------------------------------------------
# Ricaviamo dal file config.yaml il path di riferimento

my_path = utils.get_path()
auth = utils.get_auth_value()

# ----------------------------------------------------------------------------------------------------------------------
# Filtriamo il dataset export_esse3_student.csv per cds_id e aa_ord_id
df = utils.filter_students_cds_aaOrdId(cds_id=cds_id, aa_ord_id=aa_ord_id)

if df.empty:
    raise ValueError("Empty reference dataframe: nothing to search. Abort.")

cds_cod = df.iloc[1]['CDS_COD']
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Parte 1 -> Creare set() con matr, sesso, pond e tutte le materie + materie_year

column_set = set()
column_set.add('matr')  # matricola
column_set.add('sex')  # sesso
column_set.add('pond')  # ponderata
column_set.add('eta_iscr')  # età al momento dell'iscrizione
print("Ottengo materie di tutte le offerte formative")

# API CALL -> Cerco tutte le offerte disponibili per un dato CDS_COD
req_off_form = rqst.get(
    "https://unime.esse3.cineca.it/e3rest/api/offerta-service-v1/offerte?cdsCod={}&order=aaOffId".format(cds_cod))

for offerta in json.loads(req_off_form.text):

    aaOffId = offerta["aaOffId"]
    # Visto che l'anno di ordinamento è aaOrdId, partiamo da quell'anno, quindi
    # saltiamo tutti gli anni precedenti
    if aaOffId < int(aa_ord_id):
        continue

    # Cerco le materie per ogni offerta formativa
    req_mat = rqst.get(
        "https://unime.esse3.cineca.it/e3rest/api/offerta-service-v1/offerte/{}/{}/attivita".format(aaOffId, cds_id))

    # Per ogni materia in offerta formativa inserisco in set sia adCod che "adCod"_year
    for materia in json.loads(req_mat.text):
        adId = materia["chiaveAdContestualizzata"]["adId"]
        column_set.add(adId)
        column_set.add("{}_year".format(adId))  # anno accademico in cui ha eseguito l'esame

# COLUMN_SET CREATO -> Creiamo DataFrame!
new_dataset = pd.DataFrame(columns=column_set)

print("DataFrame Creato. Popolamento")

# ITERIAMO IL DATASET PASSATO COME ARGOMENTO
i = 0
done = 0

for index, el in df.iterrows():
    i += 1
    print("{}/{} ---> {}".format(i, len(df.index), el["MATRICOLA"]))
    # Per ogni studente, creo il dizionario temporaneo con tutte le materie impostate come chiavi
    studente_dict = {x: None for x in column_set}

    # Controlliamo se hanno finito gli studi. Se LAUREATI ("TIT") continuiamo, altrimenti saltiamo lo studente
    req_carriera = rqst.get(
        "https://unime.esse3.cineca.it/e3rest/api/anagrafica-service-v2/carriere/{}".format(el["STU_ID"]),
        headers={"Authorization": auth})

    carriera = json.loads(req_carriera.text)
    if carriera["motStastuCod"] != "TIT":  # Se non ha terminato gli studi passa ad altro studente
        print(" -> Studi non completati -> Salta")
        time.sleep(1)
        continue

    # DA QUI IN POI LO STUDENTE DOVREBBE AVER TERMINATO GLI STUDI (MA CI SARANNO ALCUNI SENZA VOTO)
    # INIZIAMO CON LA RICERCA!

    # inserisco matricola e sesso
    studente_dict["matr"] = carriera["matricola"]  #
    studente_dict["sex"] = carriera["sesso"]  #
    studente_dict["eta_iscr"] = utils.count_age(carriera["dataNascita"], carriera["dataImm"])  #

    # cerchiamo e prendiamo la media
    req_media = rqst.get(
        "https://unime.esse3.cineca.it/e3rest/api/libretto-service-v2/libretti/{}/medie/CDSORD/P".format(el[20]),
        headers={"Authorization": auth})
    media = json.loads(req_media.text)
    studente_dict["pond"] = media[0]["media"]  #

    # Ora cerchiamo i voti di tutte le materie dello studente
    req_libretto = rqst.get(
        "https://unime.esse3.cineca.it/e3rest/api/libretto-service-v2/libretti/{}/righe/".format(el[20]),
        headers={"Authorization": auth})

    libretto = json.loads(req_libretto.text)
    for materia in libretto:
        ad_id_temp = materia["chiaveADContestualizzata"]["adId"]
        studente_dict[ad_id_temp] = materia["esito"]["voto"]  #

        # controlliamo se l'anno di esecuzione di un esame è positivo (si, esistono anni negativi)
        # o se non hanno inserito l'anno...
        anno_esame = None
        if (not pd.isna(materia["dataFreq"])) and (materia["dataFreq"] != ""):
            anno_esame = utils.count_years(carriera["dataImm"], materia["dataFreq"])
        else:
            anno_esame = 1  # Imposto 1 perchè non so che impostare

        if anno_esame > 0:
            studente_dict["{}_year".format(ad_id_temp)] = anno_esame
        else:
            # immagino che gli anni negativi fanno riferimento a quando uno studente
            # cambia il cds e gli vengono convalidati alcuni esami precedenti, quindi
            # li imposto come se li avesse fatti al primo anno
            studente_dict["{}_year".format(ad_id_temp)] = 1

    # ABBIAMO INSERITO TUTTI GLI ESAMI NEL DICT, ORA INSERIAMO IL DICT COME NUOVA RIGA DEL DF
    # new_row = pd.Series(studente_dict, name=el["MATRICOLA"])
    new_dataset = new_dataset.append(studente_dict, ignore_index=True)
    done += 1
    print("Completati: {}".format(done))

print("\n** END MINING **\n")
print("Students: {}\nValid: {}\nPercentage: {:.2f}%".format(len(df.index), done, (done/len(df.index)*100)))

os.makedirs("{}/datasets/{}".format(my_path, aa_ord_id), exist_ok=True)
new_dataset.to_csv("{}/datasets/{}/{}.csv".format(my_path, aa_ord_id, cds_id), sep=";", index=False)

input("Press Enter to continue...")





















