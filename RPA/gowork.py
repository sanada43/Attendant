#-*- coding: utf-8 -*-
import pprint
import requests

def main():
    #GETパラメータはparams引数に辞書で指定する

    response = requests.get(
			'http://172.30.10.77:50080/rest/run/Default project/TimePro400777出_IP確認なし.robot')
    #レスポンスオブジェクトのjsonメソッドを使うと、
    #JSONデータをPythonの辞書オブジェクトを変換して取得できる。
    print(response)
	
	
if __name__== '__main__':
    main()