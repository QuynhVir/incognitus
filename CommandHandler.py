import function

def message(sender, message):
	if message == "bot":
		function.sendButton(sender)
	else:
		function.forwardMessage(sender, message)

def postback(sender, payload):
	if payload == "start":
		if function.checkUser(sender):
			function.findRelationship(sender)
		else:
			if function.checkStatus(sender):
				function.sendMessage(sender, "Sorry, you can't start new conversation, you must end this conversation first")
			else:
				function.addUser(sender)
				function.findRelationship(sender)
	if payload == "stop":
		if function.checkUser(sender):
			function.sendMessage(sender, "Sorry, you don't have any conversation to end")
		else:
			if function.checkStatus(sender):
				function.deleteRelationship(sender)
			else:
				function.sendMessage(sender, "Sorry, you don't have any conversation to end")






