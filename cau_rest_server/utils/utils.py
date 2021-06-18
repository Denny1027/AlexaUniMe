import yaml
import sys
import os
import hashlib
from dateutil.relativedelta import relativedelta
from datetime import datetime
from base64 import b64encode

with open(os.path.join(sys.path[0], "config.yaml"), "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


def get_auth_value():
    cred = cfg['s3_cred']
    code = b64encode(bytes("{}:{}".format(cred['username'], cred['password']), encoding='ascii')).decode('ascii')
    return "Basic {}".format(code)


def get_path():
    return cfg['path']


def get_cred_server():
    return cfg['server_cred']

def get_hashed_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def count_years(imm_date, exam_date):
    temp_imm = datetime.strptime(imm_date, '%d/%m/%Y %H:%M:%S')
    temp_exam = datetime.strptime(exam_date, '%d/%m/%Y %H:%M:%S')

    time_difference = relativedelta(temp_exam, temp_imm)
    diff = time_difference.years + 1   #Perchè si comincia dal PRIMO anno
    return diff