import json
import pandas as pd
import requests as rqst
from datetime import date, datetime
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler


def guess_subscriber(cds_id: str, ad_id: int, path: str):
## INIT ##

    today = datetime.strptime(date.today().__str__(), '%Y-%m-%d')

    sess_req = rqst.get(
        "https://unime.esse3.cineca.it/e3rest/api/calesa-service-v1/sessioni?cdsId={}&order=-dataInizio".format(cds_id))

    sessioni = json.loads(sess_req.text)

    this_sess = None
    year_this_sess = None
    next_sess = None
    year_next_sess = None

    for sessione in sessioni:

        endDate = datetime.strptime(sessione["dataFine"], '%d/%m/%Y %H:%M:%S')
        startDate = datetime.strptime(sessione["dataInizio"], '%d/%m/%Y %H:%M:%S')

        if today < startDate:
            next_sess = sessione["sesId"]
            year_next_sess = startDate.year

        if endDate > today > startDate:
            this_sess = sessione["sesId"]
            year_this_sess = startDate.year
            break

        # Carica dataset e filtra per cds_id

    ds = filter_ad_id(cds_id, ad_id, path)

    # Se il dataset è vuoto == se il dataset non contiene i dati di interesse
    if ds.empty:
        return False

    x, y = split_dataset(ds)

    #Usiamo SVR con kernel RBF perchè è l'unico che ha una MSE minore di 1
    scx = StandardScaler()
    scy = StandardScaler()

    y = y.reshape(len(y), 1)
    x = scx.fit_transform(x)
    y = scy.fit_transform(y)

    svr = SVR(kernel='rbf')
    svr.fit(x, y.ravel())


    predict_this_sess = None
    predict_next_sess = None

    if this_sess:
        predict_this_sess = scy.inverse_transform(svr.predict(scx.transform([[year_this_sess, this_sess]])))

    predict_next_sess = scy.inverse_transform(svr.predict(scx.transform([[year_next_sess, next_sess]])))

    return {
        "this_session": {
            "num": this_sess,
            "stud": round(predict_this_sess[0])
        },
        "next_session": {
            "num": next_sess,
            "stud": round(predict_next_sess[0])
        }}

## METODI UTILI PER LA SELEZIONE DEL DATASET ##
def filter_ad_id(cds_id: str, ad_id: int, path: str):
    ds = pd.read_csv("{}/subscr_guess/{}.csv".format(path, cds_id), sep=';')
    ds = ds.loc[ds["ad_id"] == ad_id]
    return ds


def split_dataset(dataset: pd.DataFrame):
    x = dataset.iloc[:, 1:-1].values
    y = dataset.iloc[:, -1].values
    return x, y