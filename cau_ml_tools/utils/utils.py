import os
import sys
import yaml

import pandas as pd

from base64 import b64encode
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta


def filter_students_cds_aaOrdId(cds_id: str, aa_ord_id: str = None, cond="concluso"):
    pd.set_option('display.max_columns', None)  #Debug

    types = {"MATRICOLA": str, "TIPO_CORSO_AMB_MOBIL_COD": str, "CDS_COD": str, "CDS_ID": str, "AA_ORD_ID": str}
    cond_list = ('attivo', 'concluso', 'ritirato')

    if cond not in cond_list:
        return None

    ds = pd.read_csv('./utils/export_esse3_student.csv', sep=';', dtype=types)
    ds = ds.iloc[:, 2:]
    ds = ds.loc[ds["CDS_ID"] == cds_id]

    if aa_ord_id is not None:
        ds = ds.loc[ds['AA_ORD_ID'] == aa_ord_id]

    if cond == "concluso":
        ds = ds.loc[ds['DATA_INI_SOSP'].isnull()]
        ds = ds.loc[ds['DATA_CHIUSURA'].notnull()]
    elif cond == "attivo":
        ds = ds.loc[ds['DATA_INI_SOSP'].isnull()]
        ds = ds.loc[ds['DATA_CHIUSURA'].isnull()]
    elif cond == "ritirato":
        ds = ds.loc[ds['DATA_INI_SOSP'].notnull()]
        ds = ds.loc[ds['DATA_CHIUSURA'].isnull()]

    print(ds.head())
    return ds


def clean_null_columns(df: pd.DataFrame):
    df.dropna(subset=['pond'], inplace=True)
    #df.dropna(axis='columns', thresh=(len(df.index) / 10 *4), inplace=True)
    df.dropna(how='all', axis=1, inplace=True)
    return df


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
    diff = time_difference.years  #Perchè si comincia dal PRIMO anno
    return diff


def get_auth_value():
    with open(os.path.join(sys.path[0], "config.yaml"), "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    cred = cfg['s3_cred']
    code = b64encode(bytes("{}:{}".format(cred['username'], cred['password']), encoding='ascii')).decode('ascii')
    return "Basic {}".format(code)


def get_path():
    with open(os.path.join(sys.path[0], "config.yaml"), "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    return cfg['path']
