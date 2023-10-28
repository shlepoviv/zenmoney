import time
import json

import requests

from src.bese_shcems import Diff
from src.conf_pars import read_config
from src.db_conect import get_db_tables,get_columns_in_tabele,get_data,\
                            get_insert_query,create_tables




def get_data_from_api(api_url:str,token:str,from_timestamp:time=None,
                       to_timestamp:time=None) -> json:
    header = {
        'Authorization': f'Bearer {token}'
    }

    query_data = {
        'currentClientTimestamp': to_timestamp if to_timestamp else time.time(),
        'serverTimestamp': from_timestamp if from_timestamp else 0
    }
    response = requests.post(api_url, headers=header,json=query_data,timeout=10)
    if response.ok:
        return response.json()
    return None

def validate_and_retern_dict(input_data:json) -> dict:
    return  Diff.model_validate(input_data).model_dump()


def write_all_data_in_db(input_data:dict) ->None:
    if not get_db_tables():
        create_tables()

    table = "serverTimestamp"
    if table in input_data:     
        columns = get_columns_in_tabele(table) 
        get_data(get_insert_query(table,columns),{table:input_data[table]})    
    
    tables = ["instrument","country","company","zenmoneyuser","account","transaction" ]

    for table in tables:
        if table in input_data:
            columns = get_columns_in_tabele(table)             
            data = []
            for odj in input_data[table]:
                data_obj ={}    
                for atr in odj:
                    if atr in columns:
                        data_obj[atr] = odj[atr]
                if data_obj:
                    data.append(data_obj)                
            get_data(get_insert_query(table,columns),data)
                



write_all_data_in_db(validate_and_retern_dict(get_data_from_api(**read_config('zenmoney'))))
