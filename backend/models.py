
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
            title=self.title,
            description=self.description,
            expiration=self.expiration,
            price=self.price,
            owner=self.owner,
            item_id=str(self.key.id()))

    @classmethod
    def to_message_collection(Item, items):
        itemMessages = []
        for item in items:
            itemMessages.append(item.to_message())

        return ItemMessageCollection(
            code="OK",
            message="OK",
            data=itemMessages)


class User(ndb.Model):
    email = ndb.StringProperty(indexed=False)
    name = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    image_url = ndb.StringProperty(indexed=False)
    tag = ndb.StringProperty(indexed=False)
    disabled = ndb.StringProperty(indexed=False)


class Comm(ndb.Model):
    subject = ndb.StringProperty(indexed=False)
    sender = ndb.StringProperty(indexed=False)
    receiver = ndb.StringProperty(indexed=False)
    timestamp = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    item_id = ndb.StringProperty(indexed=False)
    item_title = ndb.StringProperty(indexed=False)
    price = ndb.StringProperty(indexed=False)


class Transaction(ndb.Model):
    closed = ndb.StringProperty(indexed=False)
    buyer_confirmation = ndb.StringProperty(indexed=False)
    seller_confirmation = ndb.StringProperty(indexed=False)
    seller = ndb.StringProperty(indexed=False)
    item_id = ndb.StringProperty(indexed=False)
    price = ndb.StringProperty(indexed=False)
    item_title = ndb.StringProperty(indexed=False)
    transaction_id = ndb.StringProperty(indexed=False)
    feedback_item = ndb.StringProperty(indexed=False)
    feedback_seller = ndb.StringProperty(indexed=False)


class Feedback(ndb.Model):
    feedback_id = ndb.StringProperty(indexed=False)
    author = ndb.StringProperty(indexed=False)
    rating = ndb.StringProperty(indexed=False)
    comment = ndb.StringProperty(indexed=False)
    item_id = ndb.StringProperty(indexed=False)
    seller_uid = ndb.StringProperty(indexed=False)
    transaction_id = ndb.StringProperty(indexed=False)

