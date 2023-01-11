# -*- coding: utf-8 -*-
import time
import json
import requests
from env import (api_gateway_url)

def main():
	try:
		while True:
			tempture_json = json.load(open("tempture.json","r"))
			request_json = {"body":tempture_json}
			print(request_json)
			try: 
				response = requests.post(api_gateway_url, json=request_json)
				if 'json' in response.headers.get('content-type'):
					print("test1")
					print(response)
					result = response.json()
				else:
					print("test")
					result = response.text
				print(result)
			except Exception as ex:
				print(ex)
				pass
			time.sleep(300)
	except Exception as ex:
		print(ex)
		pass

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass
	finally:
		pass