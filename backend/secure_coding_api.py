"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from google.appengine.ext import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from messages import UserMessageCollection, UserMessage, ItemMessage, ItemMessageCollection, \
    BaseMessage, CommMessage, CommMessageCollection
from models import User, Item, Comm

package = 'SecureCoding'

WEB_CLIENT_ID = '142521807042.apps.googleusercontent.com'
LOCAL_CLIENT_ID = '142521807042-l2afethj1qsrj64hecteq6rdth0qngrm.apps.googleusercontent.com'
ANDROID_AUDIENCE = WEB_CLIENT_ID


hardcode = endpoints.api(name='hardcode', version='v1',
                        allowed_client_ids=[WEB_CLIENT_ID, LOCAL_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
                        audiences=[ANDROID_AUDIENCE],
                        scopes=[endpoints.EMAIL_SCOPE])

def check_signed_in():
    current_user = User.get_current_user()

    if not User.get_current_user():
        raise endpoints.UnauthorizedException('Invalid token.')
    else:
        return current_user

@hardcode.api_class(resource_name='items', path="items")
class Items(remote.Service):

    ##Item api
    ITEMS_RESOURCE = endpoints.ResourceContainer(
        ItemMessage)

    ITEMS_COLLECTION_RESOURCE = endpoints.ResourceContainer(
        ItemMessageCollection)

    @endpoints.method(ITEMS_RESOURCE, BaseMessage,
                      path='item/add', http_method='POST',
                      name='addItem')
    def add_item_post(self, request):
        check_signed_in()
        item = Item(
            title=request.title,
            description=request.description,
            expiration=request.expiration,
            price=request.price,
            owner=User.get_current_user())
        key = item.put()
        return BaseMessage(message="OK", code="OK", data=str(key.id()))

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, ItemMessageCollection,
                      path='item/{id}', http_method='GET',
                      name='getItem')
    def items_get(self, request):
        item = Item.get_by_id(request.id)
        #add filter for expiration
        if item:
            return Item.to_message_collection([item])
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))

    @endpoints.method(message_types.VoidMessage, ItemMessageCollection,
                      path='items', http_method='GET',
                      name='listItems')
    def list_items_get(self, request):
        return Item.to_message_collection(Item.query())

    @endpoints.method(ID_RESOURCE, BaseMessage,
                      path='item/del/{id}', http_method='POST',
                      name='delItem')
    def del_item_post(self, request):
        user = check_signed_in()

        item = Item.get_by_id(request.id)
        if item.owner != User.get_current_user():
            return BaseMessage(message="Missing rights",
                               code="ERROR",
                               data="You are not authorized to delete the Item.")
        if item:
            item.delete()
            return BaseMessage(message="OK", code="OK", data="Item successful deleted")
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))

    @endpoints.method(ID_RESOURCE, ItemMessage,
                      path='item/mod', http_method='POST',
                      name='modItem')
    def mod_item_post(self, request):
        pass

@hardcode.api_class(resource_name='users', path="users")
class Users(remote.Service):
    ##Item api
    USERS_RESOURCE = endpoints.ResourceContainer(
            UserMessage)

    USERS_COLLECTION_RESOURCE = endpoints.ResourceContainer(
            UserMessageCollection)

    #missing protection (Oauth2????)
    @endpoints.method(USERS_RESOURCE, BaseMessage,
                      path='user/add', http_method='POST',
                      name='addUsers')
    def add_user_post(self, request):
        #check if email already exists
        user = User(
            email=endpoints.get_current_user().email(),
            name=request.name,
            description=request.description,
            image_url=request.image_url,
            tag=request.tag,
            disabled=request.disabled)
        key = user.put()
        return BaseMessage(message="OK", code="OK", data=str(key.id()))

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, UserMessageCollection,
                      path='user/{id}', http_method='GET',
                      name='getUser')
    def users_get(self, request):
        user = User.get_by_id(request.id)
        if user:
            return User.to_message_collection([user])
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))

    @endpoints.method(message_types.VoidMessage, UserMessageCollection,
                      path='users', http_method='GET',
                      name='listUsers')
    def list_users_get(self, request):
        check_signed_in()
        return User.to_message_collection(User.query())

    @endpoints.method(ID_RESOURCE, BaseMessage,
                      path='user/del/{id}', http_method='POST',
                      name='delUser')
    def del_user_post(self, request):
        #delete Users Items?
        check_signed_in()
        user = User.get_by_id(request.id)

        if user and user == User.query(User.email == endpoints.get_current_user().email()).get():
            user.key.delete()
            return BaseMessage(message="OK", code="OK", data="User deleted")
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))

    @endpoints.method(ID_RESOURCE, UserMessage,
                      path='user/mod', http_method='POST',
                      name='modUser')
    def mod_user_post(self, request):
        pass


@hardcode.api_class(resource_name='search', path="search")
class Search(remote.Service):

    @endpoints.method(message_types.VoidMessage, UserMessageCollection,
                      path='search/query', http_method='GET',
                      name='query')
    def query_get(self, request):
        return User.to_message_collection(User.query())


@hardcode.api_class(resource_name='comms', path="users")
class Comms(remote.Service):
    ##Item api
    COMMS_RESOURCE = endpoints.ResourceContainer(
            CommMessage)

    COMMS_COLLECTION_RESOURCE = endpoints.ResourceContainer(
            CommMessageCollection)

    @endpoints.method(COMMS_RESOURCE, BaseMessage,
                      path='comm/add', http_method='POST',
                      name='addComm')
    def add_comm_post(self, request):
        check_signed_in()
        comm = Comm(
            subject=request.subject,
            sender=User.get_current_user().id(),
            receiver=request.receiver,
            content=request.content,
            item_id=request.item_id,
            item_title=request.item_title,
            price=request.price)
        key = comm.put()
        return BaseMessage(message="OK", code="OK", data=str(key.id()))

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, CommMessageCollection,
                      path='comm/{id}', http_method='GET',
                      name='getComm')
    def comm_get(self, request):
        user = check_signed_in()
        comm = Comm.get_by_id(request.id)
        #multiple receivers...

        if comm and (user == comm.sender or user == comm.receiver):
            return Comm.to_message_collection([comm])
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                                  (request.id,))

    @endpoints.method(message_types.VoidMessage, CommMessageCollection,
                      path='comms', http_method='GET',
                      name='listComm')
    def list_comms_get(self, request):
        #missing filter
        return Comm.to_message_collection(Comm.query())

    @endpoints.method(ID_RESOURCE, BaseMessage,
                      path='comm/del/{id}', http_method='POST',
                      name='delComm')
    def del_comm_post(self, request):
        #delete Users Items?
        user = check_signed_in()
        comm = Comm.get_by_id(request.id)

        if comm and comm.sender == User.query(User.email == endpoints.get_current_user()).get():
            comm.delete()
            return BaseMessage(message="OK", code="OK", data="User deleted")
        else:
            raise endpoints.NotFoundException('Item %s not found.' %
                                              (request.id,))


APPLICATION = endpoints.api_server([hardcode])