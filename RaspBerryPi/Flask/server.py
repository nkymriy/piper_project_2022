# -*- coding: utf-8 -*-
from flask import Flask, render_template 
import requests
import json
import datetime
import statistics
from collections import defaultdict
from env import (api_gateway_url)

app = Flask(__name__, static_folder='./templates/images')
lambda_url = 'https://iywez76781.execute-api.ap-northeast-1.amazonaws.com/lambda_001'

@app.route('/hello_world')
def hello_world():
	return 'Hello World'

@app.route('/')
def index():
	room_status = get_room_status()
	if len(room_status) == 0:
		return render_template('top.html', title='flask in NR')
	latest_time = datetime.datetime.strptime(str(room_status["timestamp"]), "%Y%m%d%H%M%S")
	return render_template('top.html', title='flask in NR', room_status=room_status, latest_time=latest_time)

def get_room_list():
	room_dict = requests.get(lambda_url).json()
	room_dict = defaultdict(list,room_dict)
	return room_dict["Items"]

def get_room_latest(room_list):
	if len(room_list) == 0 :
		return []
	latest_time = max([kv["timestamp"] for kv in room_list])
	latest_room = [kv for kv in room_list if kv["timestamp"] == latest_time]
	print(latest_room[0])
	return latest_room[0]

def get_room_status():
	room_list = get_room_list()
	if len(room_list) == 0:
		return []
	room_status = get_room_latest(room_list)
	temp_list = [kv["temp"] for kv in room_list]
	room_status["max_temp"] = max(temp_list)
	room_status["min_temp"] = min(temp_list)
	room_status["mean_temp"] = round(statistics.mean(temp_list), 2)

	huid_list = [kv["huid"] for kv in room_list]
	room_status["max_huid"] = max(huid_list)
	room_status["min_huid"] = min(huid_list)
	room_status["mean_huid"] = round(statistics.mean(huid_list), 2)
	return room_status

if __name__ == '__main__':
	app.debug = True
	app.run(host='192.168.0.253', port=8011)
