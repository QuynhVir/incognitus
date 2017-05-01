import requests
import config
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def sendButton(user_id):
    headers = {'content-type': 'application/json'}
    payload = '{"recipient": {"id": '+user_id+'}, "message":{"attachment":{"type":"template","payload":{"template_type":"button","text":"What do you want to do next?","buttons":[{"type":"postback","title":"Start Chatting","payload":"start"},{"type":"postback","title":"End Conversation","payload":"stop"}]}}}}'
    payload = payload.encode('utf-8')
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + config.TOKEN, data=payload, headers=headers)

def checkUser(user_id):
	return r.sismember('users', user_id)

def checkStatus(user_id):
	return r.exists(user_id)

def getRelationship(user_id):
	return r.get(user_id)

def addRelationship(user1, user2):
	r.set(user1, user2)
	r.set(user2, user1)
	r.srem('users', user1)
	r.srem('users', user2)

def deleteRelationship(user_id):
	partner = getRelationship(user_id)
	r.delete(user_id)
	r.delete(partner)

def addUser(user_id):
	r.sadd('users', user_id)

def sendMessage(user_id, msg):
	headers = {'content-type': 'application/json'}
	payload = '{"recipient": {"id": '+user_id+'},"message": {"text": "'+msg+'"}}'
	payload = payload.encode('utf-8')
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + config.TOKEN, data=payload, headers=headers)

def forwardMessage(user_id, msg):
	relation = getRelationship(user_id)
	if relation:
		sendMessage(relation, msg)

def findRelationship(user_id):
	if r.scard('users') == 1:
		sendMessage(user_id, "Sorry, no stranger available now")
	else:
		while True:
			partner = r.srandmember('users')
			if partner != user_id:
				break
		addRelationship(user_id, partner)
		sendMessage(user_id, "You have been connected with the stranger")
		sendMessage(partner, "You have been connected with the stranger")















