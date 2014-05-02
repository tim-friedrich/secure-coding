
from google.appengine.ext import endpoints
from google.appengine.ext import ndb
from messages import ItemMessage, ItemMessageCollection

class Item(ndb.Model):    
    title = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    expiration = ndb.StringProperty(indexed=False)
    price = ndb.StringProperty(indexed=False)
    owner = ndb.StringProperty(indexed=False)

    def to_message(self):
        return ItemMessage(
            title = self.title,
            description = self.description,
            expiration = self.expiration,
            price = self.price,
            owner = self.owner,
            item_id = str(self.key.id()))

    @classmethod
    def to_message_collection(Item, items):
        itemMessages = []
        for item in items:
            itemMessages.append(item.to_message())

        return ItemMessageCollection(
            code = "OK",
            message = "OK",
            data = itemMessages)