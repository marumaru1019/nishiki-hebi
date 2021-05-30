import requests
import time
import logging

URL="https://61r93edyrsd5.cybozu.com/k/v1/"
APPID=1
APPID2=7
API_TOKEN="uxuJRsQ7jkunko02d9nVQnDSyIJtDmEe2xSGXFEp,pDfygdA7GUMQ7iTLEkljfaww5EDiKkjOOFcor4bM"
API_TOKEN2="pDfygdA7GUMQ7iTLEkljfaww5EDiKkjOOFcor4bM"

# import data into kinto db
def q_params(line_name,line_id,contents,category="non",sub1="",sub2="",name="",ID=""):
    url_flag=0
    if(category=="自己紹介"):
        print("self-intro")
        PARAMS=selfintro_params(line_name,line_id,name,ID)
        url_flag=1
    else:
        PARAMS={
                "app":APPID,
                "record":{
                        "line_name":{
                                "value":line_name
                                },
                        "line_id":{
                                "value":line_id
                                },
                        "contents":{
                                "value":contents
                                },
                        "category":{
                                "value":category
                                },
                        "sub1":{
                                "value":sub1
                                },
                        "sub2":{
                                "value":sub2
                                }
                        }
                }
    return PARAMS,url_flag

def selfintro_params(line_name,line_id,name,ID):
    PARAMS={
            "app":APPID2,
            "record":{
                    "line_name":{
                            "value":line_name
                            },
                    "line_id":{
                            "value":line_id
                            },
                    "name":{
                            "value":name
                            },
                    "ID":{
                            "value":ID
                            }
                    }
            }
    return PARAMS

def ret_API_data(api_flag=0):
    if(api_flag):
        return URL,APPID2,API_TOKEN2
    else:
        return URL,APPID,API_TOKEN
        
def q_post(url, api_token, params):
    headers = {"X-Cybozu-API-Token": api_token,
               "Content-Type": "application/json"}
    resp = requests.post(url+"record.json", json=params, headers=headers)

    return resp

def q_input(kintone_endpoint, api_token, params):
    RESP = q_post(kintone_endpoint, api_token, params)
    time.sleep(0.5)
    logging.info(RESP.text)
    logging.info("create data!")