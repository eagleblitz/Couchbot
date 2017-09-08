import asyncio
from auth import OWNER_ID

blocked_channels = []


@asyncio.coroutine
def add(message, client):
	data = message.content.split(' ')
	x = 0
	try:
		for i in range(1, len(data)):
			x += int(data[i])
	except Exception:
		yield from client.send_message(message.channel, "Could not add numbers up. :dont_know_man:")
		return

	yield from client.send_message(message.channel, "Result: " + str(x))


@asyncio.coroutine
def block(message, client):
	if message.author.id == OWNER_ID:
		if message.channel not in blocked_channels:
			blocked_channels.append(message.channel)
			yield from client.send_message(message.channel, "Channel blocked!")
			return
	yield from client.send_message(message.channel, "Could not block channel! :dont_know_man:")


@asyncio.coroutine
def unblock(message, client):
	if message.author.id == OWNER_ID:
		if message.channel in blocked_channels:
			blocked_channels.remove(message.channel)
			yield from client.send_message(message.channel, "Channel unblocked!")
			return
	yield from client.send_message(message.channel, "Could not unblock channel! :dont_know_man:")


def isBlocked(channel):
	if channel in blocked_channels:
		return True
	return False
