import json
import yaml
import tensorflow as tf

from os import path
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt


with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

my_path = cfg['path']


def guess(cds_id, aa_ord_id, ad_id, pond, data_imm, data_nascita):
    if not path.exists("{}\\datasets\\{}\\{}.csv".format(my_path, aa_ord_id, cds_id)):
        return {"value": -1} # non esiste il dataset, quindi non dovrebbe esistere nemmeno il modulo salvato
    if not path.exists("{}\\predict_marks\\{}\\{}\\{}".format(my_path, aa_ord_id, cds_id, ad_id)):
        return {"value": -2} # esiste il dataset ma non esiste il modulo salvato

    ann = tf.keras.models.load_model("{}\\predict_marks\\{}\\{}\\{}".format(my_path, aa_ord_id, cds_id, ad_id))

    now = dt.now()
    data_odierna = now.strftime("%d/%m/%Y %H:%M:%S")

    pond = float(pond)
    temp_pred = ann.predict([[pond, count_age(data_nascita, data_odierna), count_years(data_odierna, data_imm)]])
    #ptt = temp_pred[0].tolist()
    #return y_dict[str(round(temp_pred[0]))]
    print(temp_pred.item(0))
    return {"value": temp_pred.item(0)}

def count_years(imm_date, exam_date):
    temp_imm = dt.strptime(imm_date, '%d/%m/%Y %H:%M:%S')
    temp_exam = dt.strptime(exam_date, '%d/%m/%Y %H:%M:%S')

    time_difference = relativedelta(temp_exam, temp_imm)
    diff = time_difference.years + 1   #Perchè si comincia dal PRIMO anno
    return diff


def count_age(birth_date, imm_date):
    temp_imm = dt.strptime(imm_date, '%d/%m/%Y %H:%M:%S')
    temp_birth = dt.strptime(birth_date, '%d/%m/%Y %H:%M:%S')

    time_difference = relativedelta(temp_imm, temp_birth)
    diff = time_difference.years
    return diff
