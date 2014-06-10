
google.appengine.secure.shop.listItems = function() {
  gapi.client.hardcode.items.listItems().execute(
      function(resp) {
        if (resp.code == 'OK') {
          resp.data = resp.data || [];
          for(var i=0; i<resp.data.length; i++){
            $('#content').append(google.appengine.secure.shop.renderItem(resp.data[i]))
          };
        }
      });
};

google.appengine.secure.shop.renderItem = function(item){
    var item_template =
        '<a href="/items/'+item['item_id']+'"><div class="item_detail">\
		    <div class="title"></div>\
			<div class="description"></div>\
			<div class="price"></div>\
			<div class="footer">\
				<div class="sellerName"></div>\
				<div class="creationTime"></div>\
			</div>\
		</div></a>';
    new_item = $(item_template).clone();
    new_item.find('.title').text(item['title']);
    new_item.find('.description').text(item['description']);
    new_item.find('.price').text(item['price']+" $");
    new_item.find('.sellerName').text(item['owner']['email']);
    new_item.find('.creationTime').text(item['created_at']);
    return new_item
};

google.appengine.secure.shop.loadItem = function(){
    var request = {}

    gapi.client.hardcode.items.getItem({ id: $('#item').attr('data-id') }).execute(function(resp){
        $content = $('#content');
        if (resp.code == "OK"){
            item = resp.data[0];
            $content.find('#title').text(item['title']);
            $content.find('#description').text(item['description']);
            $content.find('#price').text(item['price']+" $");
            $content.find('#seller').text(item['owner']['email']);
            $content.find('#created_at').text(item['created_at']);

            if(!google.appengine.secure.shop.currentUser || item['owner']['email'] != google.appengine.secure.shop.currentUser.email){
                $('#editItem').hide();
                $('#deleteItem').hide();
            }
            else{
                $('#deleteItem').on('click', function(event){
                    gapi.client.hardcode.items.delItem({ id: $('#item').attr('data-id') }).execute(function(resp){
                        if (resp.code == "OK"){
                            window.location.replace('/items/myItems')
                        }
                        else{
                            alert("An Error has occurred while deleting the item. The request returned with code: "+resp.code+" "+resp.message)
                        }
                    })
                })
            }
        }
    });
}

google.appengine.secure.shop.initAddOrEditItem = function(){
    $form = $('form');
    $('#item_expiration').datepicker();
    gapi.client.hardcode.items.getItem({ id: $('form').attr('data-id') }).execute(function(resp){

        if (resp.code == "OK"){
            item = resp.data[0];
            $form.find('#item_name').val(item['title']);
            $form.find('#item_description').val(item['description']);
            $form.find('#item_price').val(item['price']);
            $form.find('#item_expiration').val(item['expiration'])
        }
    });
    $('#submit_button').on('click', function(event){
        event.preventDefault();
        item = {
                item_id: $form.attr('data-id'),
                'title': $form.find('#item_name').val(),
                'description': $form.find('#item_description').val(),
                'price': $form.find('#item_price').val(),
                'expiration': $form.find('#item_expiration').val()
                }
        if(!item.item_id){
            gapi.client.hardcode.items.addItem(item
                ).execute(function(resp){
                        if(resp.code != "OK"){
                            alert("An Error has occurred while adding the item. The request returned with code: "+resp.code+" "+resp.message)
                        }
                        else{
                            window.location.replace('/items/'+resp.data)
                        }
                    });
                }
        else{
            item.item_id =
            gapi.client.hardcode.items.modItem(item
                ).execute(function(resp){
                    if(resp.code != "OK"){
                        alert("An Error has occurred while adding the item. The request returned with code: "+resp.code+" "+resp.message)
                    }
                    else{
                        window.location.replace('/items/'+resp.data)
                    }

                });
        }
        return false;
    });
};

google.appengine.secure.shop.listOwnItems = function() {
  gapi.client.hardcode.items.listItems().execute(
      function(resp) {
        if (resp.code == 'OK') {
          resp.data = resp.data || [];
          for(item in resp.data){
            if (resp.data[item]['owner']['email'] == google.appengine.secure.shop.currentUser.email){
                $('#content').append(google.appengine.secure.shop.renderItem(resp.data[item]))
            }
          };
        }
      });
};