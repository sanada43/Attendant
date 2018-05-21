#-*- coding: utf-8 -*-
import pprint
import requests

def main():
    #GETパラメータはparams引数に辞書で指定する

    response = requests.post(
			'http://172.30.10.132/XGWeb/Xgw0c01.asp',
	        json,
			headers=headers)
    #レスポンスオブジェクトのjsonメソッドを使うと、
    #JSONデータをPythonの辞書オブジェクトを変換して取得できる。
    print(response)
	
json={'PAGESTATUS': 'PUNCH2',
	'LoginID': '400777',
	'PassWord': 'a09415XX',
	'PROCESS': 'PUNCH2'}
	
headers={
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': '400777',
	'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'Content-Length': '65',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Cookie': 'ASPSESSIONIDACRQBSSD=FYFIYDOHJGHSAFYAQWDJPWOH',
	'Host': '172.30.10.132',
	'Origin': 'http://172.30.10.132',
	'Referer': 'http:/172.30.10.132/XGWeb/Xgw0c01.asp',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

	
if __name__== '__main__':
    main()