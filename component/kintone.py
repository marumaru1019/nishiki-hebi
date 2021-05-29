import requests
import time
import logging

# import data into kinto db
def q_params(name, contents, line_id, category):
    PARAMS = {
        "app": 1,
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


def q_post(url, api_token, params):
    headers = {"X-Cybozu-API-Token": api_token,
               "Content-Type": "application/json"}
    resp = requests.post(url+"record.json", json=params, headers=headers)

    return resp

def q_input(kintone_endpoint, api_token, params):
    RESP = q_post(kintone_endpoint, api_token, params)
    time.sleep(0.5)
    logging.info("create data!")