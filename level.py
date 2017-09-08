import asyncio, json, time, random
import discord.utils
import math
from commands import is_blocked
user_data = []
level_data = []
# level_data: {"Name"="<name>", "LevelPoints" = <points>}
FILE_PATH = "level_data.json"

LEVEL_MAX = 100
LEVEL_RANKS = ["Newbie", "Rookie", "General", "Lieutenant", "Major", "Colonel", "Commandant", "Captain", "Master", "God"]
LEVEL_RANK_SHORT = ["Nb", "Rk", "Gen", "Lt", "Mj", "Col", "Com", "Capt", "Mst", "God"]
LEVEL_EXPERIENCE_NEEDED = 350
LEVEL_RANDOM_VALUE_MIN = 15
LEVEL_RANDOM_VALUE_MAX = 40
LEVEL_TIMER = 300

clock = 0


def load():
	import os
	if os.path.exists(FILE_PATH):
		content = open(FILE_PATH, "r").read()
		data = json.loads(content)
		if data:
			global level_data
			level_data = data

	global clock
	clock = time.time()


def save():
	f = open(FILE_PATH, "w")
	data = json.dumps(level_data)
	f.write(data)
	f.close()


def process_message(message):
	if is_blocked(message.channel):
		return
	if message.content.startswith("!status"):
		return
	for user in user_data:
		if message.author.id in user["id"]:
			user["nof"] += 1
			return
	user_data.append({"id": message.author.id, "nof": 1})


def tick():
	global clock, LEVEL_TIMER, level_data
	if time.time() - clock >= LEVEL_TIMER:
		for user in user_data:
			if user["nof"] > 0:
				userID = user["id"]
				found = False
				for leveluser in level_data:
					if "id" in leveluser and userID == leveluser["id"]:
						leveluser["exp"] += random.randint(LEVEL_RANDOM_VALUE_MIN, LEVEL_RANDOM_VALUE_MAX)
						found = True

				if not found:
					level_data.append({"id": user["id"], "exp": random.randint(LEVEL_RANDOM_VALUE_MIN, LEVEL_RANDOM_VALUE_MAX)})
		clock = time.time()
		user_data.clear()


@asyncio.coroutine
def status(message, client):
	if is_blocked(message.channel):
		return

	if not message.server:
		yield from client.send_message(message.author, "You can't do that here, you must send from a server.")
		return

	if message.content.lower() == "!status" or message.content.lower() == "!status ":
		values = get_data(message.author.id)
		yield from print_status(client=client, name=message.author.name, author=message.author, values=values)
	else:
		if message.mentions:
			values = get_data(message.mentions[0].id)
			yield from print_status(client=client, name=message.mentions[0].name, author=message.author, values=values)
			return

		data = message.content.split(" ")
		name = data[1]
		for i in range(2, len(data)):
			name += " " + data[i]

		member = discord.utils.get(message.server.members, name=name)
		if member:
			values = get_data(member.id)
			yield from print_status(client=client, name=member.name, author=message.author, values=values)
			return
		else:
			member = discord.utils.get(message.server.members, nick=name)
			if member:
				values = get_data(member.id)
				yield from print_status(client=client, name=member.name, author=message.author, values=values)
				return
	yield from client.send_message(message.channel, "Member not found!")


@asyncio.coroutine
def print_status(client, name, author, values):
	yield from client.send_message(
		author, "--------------------------------------\nStatus of **" +
		name + "**:\nLevel _" + values[0] + "_, Rank _" + values[1] + "_\n" +
		"Current exp: " + values[2] + "/" + str(LEVEL_EXPERIENCE_NEEDED)
		+ "\n--------------------------------------"
	)


def get_data(clientid):
	global level_data
	data = []
	for user in level_data:
		if 'id' in user and user['id'] == clientid:
			data.append(str(math.floor(user["exp"] / LEVEL_EXPERIENCE_NEEDED)))
			rank = int(math.floor(int(data[0]) / 10))
			if rank >= 9 : rank = 9
			data.append(LEVEL_RANKS[rank])
			data.append(str(user["exp"] - int(data[0]) * LEVEL_EXPERIENCE_NEEDED))
			return data
	data.append("1")
	data.append(LEVEL_RANKS[0])
	data.append("0")
	return data
