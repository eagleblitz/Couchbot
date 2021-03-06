import asyncio, json
from permission import has_permission
blocked_channels = []

FILE_PATH = "blocked_channels.json"


@asyncio.coroutine
def block(message, client):
	if has_permission(message.author.id) == 0:
		if message.channel.id not in blocked_channels:
			blocked_channels.append(message.channel.id)
			yield from client.send_message(message.channel, "Channel blocked!")
			return
		else: yield from client.send_message(message.channel, "Channel already blocked.")
	else: yield from client.send_message(message.channel, "Could not block channel!")


@asyncio.coroutine
def unblock(message, client):
	if has_permission(message.author.id) == 0:
		if message.channel.id in blocked_channels:
			blocked_channels.remove(message.channel.id)
			yield from client.send_message(message.channel, "Channel unblocked!")
			return
		else: yield from client.send_message(message.channel, "Channel already unblocked.")
	else: yield from client.send_message(message.channel, "Could not unblock channel!")


def is_blocked(channel):
	if channel.id in blocked_channels:
		return True
	return False


def load():
	import os
	if os.path.exists(FILE_PATH):
		content = open(FILE_PATH, "r").read()
		data = json.loads(content)
		if data:
			global blocked_channels
			blocked_channels = data[0]["blocked"]
			print(blocked_channels)


def save():
	f = open(FILE_PATH, "w")
	global blocked_channels
	content = [{"blocked": blocked_channels}]
	data = json.dumps(content)
	f.write(data)
	f.close()
