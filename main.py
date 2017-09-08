import discord, asyncio
import commands, level
from auth import BOT_TOKEN
client = discord.Client()


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
	level.tick()
	level.process_message(message=message)
	if message.content.lower().startswith('!block'):
		yield from commands.block(message=message, client=client)
	elif message.content.lower().startswith('!unblock'):
		yield from commands.unblock(message=message, client=client)
	elif message.content.lower().startswith('!status'):
		yield from level.status(message=message, client=client)


if __name__ == "__main__":
	commands.load()
	level.load()
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(client.start(BOT_TOKEN))
	except (KeyboardInterrupt, Exception):
		loop.close()
		client.logout()
	finally:
		level.save()
		commands.save()
