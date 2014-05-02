"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from messages import ItemMessage, ItemMessageCollection, BaseMessage
from models import Item

package = 'SecureCoding'

WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


hardcode = endpoints.api(name='hardcode', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])

@hardcode.api_class(resource_name='itemsApi', path="items")
class ItemsApi(remote.Service):


    ##Item api
    ITEMS_RESOURCE = endpoints.ResourceContainer(
            ItemMessage)

    ITEMS_COLLECTION_RESOURCE = endpoints.ResourceContainer(
            ItemMessageCollection)

    #missing protection
    @endpoints.method(ITEMS_RESOURCE, BaseMessage,
                      path='item/add', http_method='POST',
                      name='items.addItem')
    def addItem_post(self, request):
        item=Item(
        	title=request.title,
        	description=request.description,
        	expiration=request.expiration,
        	price=request.price,
        	owner=request.owner)
        key = item.put()
        return BaseMessage(message="OK", code="OK", data=str(key.id()))

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))
    @endpoints.method(ID_RESOURCE, ItemMessageCollection,
                      path='item/{id}', http_method='GET',
                      name='items.getItem')
    def items_get(self, request):
    	#richtige id eintragen
    	item = Item.get_by_id(request.id)
    	if (item):
    		return Item.to_message_collection([item])
    	else:
    		raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))

    @endpoints.method(message_types.VoidMessage, ItemMessageCollection,
                      path='items', http_method='GET',
                      name='items.listItems')
    def listItems_get(self, request):
        return Item.to_message_collection(Item.query())


    @endpoints.method(ID_RESOURCE, BaseMessage,
                      path='item/del/{id}', http_method='POST',
                      name='items.delItem')
    def delItem_post(self, request):
        item = Item.get_by_id(request.id)
    	
    	if (item):
    		item.delete()
    		return BaseMessage(message="OK", code="OK", data=str(key.id()))
    	else:
    		raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))

    @endpoints.method(ID_RESOURCE, ItemMessage,
                      path='item/mod', http_method='POST',
                      name='items.modItem')
    def modItem_post(self, request):
        pass


APPLICATION = endpoints.api_server([hardcode])