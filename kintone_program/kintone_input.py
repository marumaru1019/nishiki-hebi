import requests
#import time

URL="https://61r93edyrsd5.cybozu.com/k/v1/"
APPID=1
APPID2=7
API_TOKEN="uxuJRsQ7jkunko02d9nVQnDSyIJtDmEe2xSGXFEp,pDfygdA7GUMQ7iTLEkljfaww5EDiKkjOOFcor4bM"
API_TOKEN2="pDfygdA7GUMQ7iTLEkljfaww5EDiKkjOOFcor4bM"

def make_params(line_name,line_id,contents,category="non",sub1="",sub2="",name="",ID=""):
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

def post_kintone(url,api_token,params):
    headers={"X-Cybozu-API-Token":api_token,"Content-Type":"application/json"}
    resp=requests.post(url+"record.json",json=params,headers=headers)

    return resp

if __name__=="__main__":
    
    """test data"""
    test_num=2
    line_name=["A.taiki","A.taiki","test300"]
    contents=["","ユニシスちゃん","test3です"]
    line_id=["Abetaiki0427","Abetaiki0427","test300id"]
    category=["自己紹介","","自己紹介"]
    name=["阿部泰希","名前名前","名前名前３"]
    ID=["uni20220427","",""]
    
    
    for i in range(test_num):
        print("========{0}========".format(i+1))
        PARAMS,url_flag=make_params(line_name=line_name[i],line_id=line_id[i],contents=contents[i],category=category[i],name=name[i],ID=ID[i])
        print(PARAMS)
        print("url_flag:{0}".format(url_flag))
        
        if(url_flag==1):
            print(API_TOKEN2)
            RESP=post_kintone(URL,API_TOKEN2,PARAMS)
            print(RESP.text)
            
        else:
            print("ok")
            RESP=post_kintone(URL,API_TOKEN,PARAMS)
            print(RESP.text)
        #time.sleep(3)
    print("=======end=========")