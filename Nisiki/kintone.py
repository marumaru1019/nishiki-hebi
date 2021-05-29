import requests
import time
import logging

APPID = 1

# import data into kinto db
def make_params(name, contents, line_id, category):
    PARAMS = {
        "app": APPID,
        "record": {
            "name": {
                "value": name
            },
            "contents": {
                "value": contents
            },
            "line_id": {
                "value": line_id
            },
            "category": {
                "value": category
            }
        }
    }
    return PARAMS


def post_kintone(url, api_token, params):
    headers = {"X-Cybozu-API-Token": api_token,
               "Content-Type": "application/json"}
    resp = requests.post(url+"record.json", json=params, headers=headers)

    return resp

def input_data(kintone_endpoint, api_token, params):
    RESP = post_kintone(kintone_endpoint, api_token, params)
    time.sleep(0.5)
    logging.info("create data!")