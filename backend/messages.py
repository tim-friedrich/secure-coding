import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote


class ItemMessage(messages.Message):
    title = messages.StringField(2)
    description = messages.StringField(3)
    expiration = messages.StringField(4)
    price = messages.StringField(5)
    owner = messages.StringField(6)
    item_id = messages.StringField(7)

class ItemMessageCollection(messages.Message):
	message = messages.StringField(1)
	code = messages.StringField(2)
	data = messages.MessageField(ItemMessage, 3, repeated=True)

class BaseMessage(messages.Message):
	message = messages.StringField(1)
	code = messages.StringField(2)
	data = messages.StringField(3)