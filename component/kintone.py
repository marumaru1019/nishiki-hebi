import requests
import time
import logging

# import data into kinto db


def q_params(line_name, line_id, contents, category="non", sub1="", sub2=""):
    PARAMS = {
        "app": 1,
        "record": {
            "line_name": {
                "value": line_name
            },
            "line_id": {
                "value": line_id
            },
            "contents": {
                "value": contents
            },
            "category": {
                "value": category
            },
            "sub1": {
                "value": sub1
            },
            "sub2": {
                "value": sub2
            }
        }
    }
    return PARAMS


def selfintro_params(line_name, line_id, name, ID):
    PARAMS = {
        "app": 7,
        "record": {
            "line_name": {
                "value": line_name
            },
            "line_id": {
                "value": line_id
            },
            "name": {
                "value": name
            },
            "ID": {
                "value": ID
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
    print(RESP.text)


