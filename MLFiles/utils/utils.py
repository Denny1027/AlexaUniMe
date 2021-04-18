import csv
import random
import requests
import json
from datetime import datetime as dt
import base64 as b64


"""
 Questo file contiene alcuni metodi utili per ottenere o modificare alcune informazioni
 utili per il corretto funzionamento degli algoritmi di machine learning.
"""

def createRandomStudentsInfoFile(CFList, *, lenght=1000):
    """
    Questo metodo permette di creare un file contenente le informazioni relative
    :param CFList: Lista di Codici Fiscali da cui prelevare un numero definito di elementi randomici
    :param lenght: numero di elementi randomici da ottenere (1000 elementi di default)
    :return crea un file "timestamp".csv con lenght elementi contenenti la matricola, nome, cognome, cf, matId,
        persId e studId
    """
    resultArray = [["matricola", "nome", "cognome", "cf", "matId", "persId", "stuId"]]
    random.shuffle(CFList)

    cont = 1
    while cont <= lenght:
        if not CFList:
            return resultArray

        tempCF = CFList.pop()
        print("---" + tempCF + "---")
        r = requests.get("https://unime.esse3.cineca.it/e3rest/api/badge-service-v1/badge?codFis=" + tempCF,
                         headers={"Authorization": __get_credentials("credentials.json")})
        if r.status_code != 200:
            print("# {} scartato # Status Code: {}".format(tempCF, r.status_code))
            continue

        if r.text == "[]":
            print("+" + tempCF + " badge not exist. Continue")
            continue

        r_dict = r.json()[0]
        nome = r_dict['nome']
        cognome = r_dict['cognome']
        matricola = r_dict['matricola']
        mat_id = r_dict['matId']
        pers_id = r_dict['persId']
        stu_id = r_dict['stuId']

        temp = [matricola, nome, cognome, tempCF, mat_id, pers_id, stu_id]
        resultArray.append(temp)
        print("(" + str(cont) + "/" + str(lenght) + ") " + tempCF + " inserito!")
        cont += 1

    filename = '%s.csv' % str(dt.now().isoformat(timespec='seconds'))
    filename = filename.replace(':', '_')
    print(filename)

    with open("./files/"+filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(resultArray)


def __get_credentials(json_file):

    auth_json = None
    try:
        auth_json = json.load(open(json_file))
    except OSError:
        print("Errore durante l'apertura del file. Ritorna None")
        return None

    if auth_json["username"] and auth_json["password"]:
        a = "{}:{}".format(auth_json["username"], auth_json["password"])
        ascii_a = a.encode("ascii")
        b = "Basic {}".format(b64.b64encode(ascii_a).decode('ascii'))
    else:
        print("Formato del JSON errato. Ritorna None")
        b = None

    return b

