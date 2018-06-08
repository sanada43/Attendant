#-*- coding: utf-8 -*-
import pprint
import requests

def goRPA():
    #GETパラメータはparams引数に辞書で指定する

    response = requests.get(
			'http://172.30.10.77:50080/rest/run/Default project/TimePro400777出_IP確認なし.robot',timeout=20)
    #レスポンスオブジェクトのjsonメソッドを使うと、
    #JSONデータをPythonの辞書オブジェクトを変換して取得できる。
    #response.encoding = 'utf-8'
    #print(response.text)
    return response
	
	
if __name__== '__main__':
    goRPA()