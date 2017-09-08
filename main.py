import discord, asyncio, time
import commands, level
from auth import BOT_TOKEN
client = discord.Client()

timer = 0


@client.event
@asyncio.coroutine
def on_ready():
	print("-----------------")
	print(client.user.name)
	print(client.user.id)
	print(client.user.display_name)
	print("-----------------")


@client.event
@asyncio.coroutine
def on_message(message):
	save()
	if message.content is "save" and message.author.id is client.user.id:
		level.save()
		commands.save()
		print("saved!")

	level.tick()
	level.process_message(message=message)
	if message.content.lower().startswith('!block'):
		yield from commands.block(message=message, client=client)
	elif message.content.lower().startswith('!unblock'):
		yield from commands.unblock(message=message, client=client)
	elif message.content.lower().startswith('!status'):
		yield from level.status(message=message, client=client)


def save():
	global timer
	if time.time() - timer > 3600:
		level.save()
		commands.save()
		timer = time.time()
		print("fuck me senpai")

if __name__ == "__main__":
	timer = time.time()
	commands.load()
	level.load()
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(client.start(BOT_TOKEN))
	except (KeyboardInterrupt, Exception):
		loop.close()
		client.logout()
		running = False
	finally:
		level.save()
		commands.save()
