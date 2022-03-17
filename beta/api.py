import requests
import time
import hashlib
from shinemonitor import main_solar
baseurl = "https://web.shinemonitor.com/public/"


lingua = 'pt_BR'
# global vars
company_key = "&company-key=bnrl_frRFjEz8Mkn"
baseurl = "https://web.shinemonitor.com/public/"
signurl = "?sign="
salrurl = "&salt="
planturl = "&plantid="
tokenurl = "&token="
par = "&par=ENERGY_TODAY,ENERGY_MONTH,ENERGY_YEAR,ENERGY_TOTAL,ENERGY_PROCEEDS,ENERGY_CO2,CURRENT_TEMP,CURRENT_RADIANT,BATTERY_SOC,ENERGY_COAL,ENERGY_SO2"
queryPlantsInfo = "&action=queryPlantsInfo"
queryPlantInfo = "&action=queryPlantInfo"
queryPlantCurrentData = "&action=queryPlantCurrentData"
langstr = ['&i18n=', '&lang=']


def get_sal():
    return str(int(time.time()))


def auth(u, s):
    sal = get_sal()
    auth = "&action=auth&usr=" + u + company_key
    passsha1 = hashlib.sha1(s.encode()).hexdigest()
    sign = hashlib.sha1(((sal + passsha1 + auth).encode())).hexdigest()
    urlauth = baseurl + signurl + sign + salrurl + sal + auth
    r = requests.get(urlauth).json().get("dat")
    return r


def get_pid(x):
    sal = get_sal()
    auth_ = x
    # print(auth_)
    secret = str(auth_.get("secret"))
    token = str(auth_.get("token"))
    action = queryPlantsInfo + langstr[0] + lingua + langstr[1] + lingua
    sign = hashlib.sha1((sal + secret + token + action).encode()).hexdigest()
    urlpid = baseurl + signurl + sign + salrurl + sal + tokenurl + token + action
    pid = requests.get(urlpid).json().get("dat").get("info")[0].get("pid")
    return pid


def get_plant_info(x):
    sal = get_sal()
    auth_ = x
    secret = str(auth_.get("secret"))
    token = str(auth_.get("token"))
    pid = str(get_pid(x))
    action = queryPlantInfo + planturl + pid + langstr[0] + lingua + langstr[1] + lingua
    sign = hashlib.sha1((sal + secret + token + action).encode()).hexdigest()
    urlplantinfo = baseurl + signurl + sign + salrurl + sal + tokenurl + token + action
    r = requests.get(urlplantinfo).json()
    return r.get("dat")


def get_solar(x):
    sal = get_sal()
    auth_ = x
    dict_final = {}
    secret = str(auth_.get("secret"))
    token = str(auth_.get("token"))
    pid = str(get_pid(x))
    action = queryPlantCurrentData + planturl + pid + par
    sign = hashlib.sha1((sal + secret + token + action).encode()).hexdigest()
    final_url = baseurl + signurl + sign + salrurl + sal + tokenurl + token + action
    r = requests.get(final_url).json().get("dat")
    for x in r:
        title = x.get("key")
        val = x.get("val")
        dict_final[title] = val
    return dict_final


def main_solar(u, s, y):
    autenticao = auth(u, s)
    if autenticao != None:
        if y == 1:
            return get_solar(autenticao)
        elif y == 0:
            return get_plant_info(autenticao)
        else:
            print("error")
