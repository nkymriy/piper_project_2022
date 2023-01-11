# インストールした discord.py を読み込む
import discord
import requests
from collections import defaultdict
import statistics
import json
from env import(DISCORD_TOKEN, api_gateway_url)

# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# 起動時に動作する処理
@client.event
async def on_ready():
	# 起動したらターミナルにログイン通知が表示される
	print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
	# メッセージ送信者がBotだった場合は無視する
	if message.author.bot:
		return
	if message.content == 'いま何度？':
		room = get_room_status()
		text = f'室温は{room["temp"]}℃で、湿度は{room["huid"]}%ですよ。'
		await message.channel.send(text)

def get_room_list():
	room_dict = requests.get(api_gateway_url).json()
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


# Botの起動とDiscordサーバーへの接続
client.run(DISCORD_TOKEN)