import commands, json

FILE_NAME = "rights.json"

PERMISSIONS = ["OWNER", "ADMIN", "HELPER"]

owners = []
admins = []
helpers = []


def load():
	f = open(FILE_NAME)
	data = json.loads(f.read())
	data = data[0]
	f.close()
	global owners, admins, helpers
	owners = data["owner"]
	admins = data["admin"]
	helpers = data["helper"]


def save():
	content = [{"owner": owners}, {"admin": admins}, {"helper": helpers}]
	f = open(FILE_NAME)
	data = json.dumps(content)
	f.write(data)
	f.close()


def has_permission(client_id):
	for owner in owners:
		if owner == client_id:
			return 0
	for admin in admins:
		if admin == client_id:
			return 1
	for helper in helpers:
		if helper == client_id:
			return 2
	return 3


def add_permission(client_id, level):
	if level == 0:
		owners.append(client_id)
	elif level == 1:
		admins.append(client_id)
	elif level == 2:
		helpers.append(client_id)
