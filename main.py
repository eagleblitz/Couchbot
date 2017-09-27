import discord, asyncio, time
import commands, level, permission
import config, logging
client = discord.Client()

timer = 0


@client.event
@asyncio.coroutine
def on_ready():
	logging.debug("-----------------")
	logging.debug(client.user.name)
	logging.debug(client.user.id)
	logging.debug(client.user.display_name)
	logging.debug("-----------------")


@client.event
@asyncio.coroutine
def on_message(message):
	save()
	if message.content is "save" and message.author.id is client.user.id:
		level.save()
		commands.save()
		permission.save()
		logging.debug("Saving...")

	level.tick()
	level.process_message(message=message)
	if message.content.lower().startswith('!block') and permission.has_permission(message.author.id) == 0:
		yield from commands.block(message=message, client=client)
	elif message.content.lower().startswith('!unblock') and permission.has_permission(message.author.id) == 0:
		yield from commands.unblock(message=message, client=client)
	elif message.content.lower().startswith('!status'):
		yield from level.status(message=message, client=client)

	elif message.content.lower().startswith('!givexp') and permission.has_permission(message.author.id) <= 1:
		yield from level.give_exp(message=message, client=client)

	elif message.content.lower().startswith('!takexp') and permission.has_permission(message.author.id) <= 1:
		yield from level.take_exp(message=message, client=client)

	elif message.content.lower().startswith('!setxp') and permission.has_permission(message.author.id) <= 1:
		yield from level.set_exp(message=message, client=client)

	elif message.content.lower().startswith('!top') and permission.has_permission(message.author.id) <= 3:
		yield from level.top(message=message, client=client)


def save():
	global timer
	if time.time() - timer > 3600:
		level.save()
		commands.save()
		timer = time.time()
		print("fuck me senpai")

if __name__ == "__main__":
	logging.basicConfig(filename=config.LOG_PATH, filemode='w', level=logging.DEBUG)
	timer = time.time()
	commands.load()
	level.load()
	permission.load()
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(client.start(config.BOT_TOKEN))
	except (KeyboardInterrupt, Exception):
		loop.close()
		client.logout()
		running = False
	finally:
		level.save()
		commands.save()
