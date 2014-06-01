
google.appengine.secure.shop.listItems = function() {
  gapi.client.hardcode.items.listItems().execute(
      function(resp) {
        if (resp.code == 'OK') {
          resp.data = resp.data || [];
          for(item in resp.data){
            $('#content').append(google.appengine.secure.shop.renderItem(resp.data[item]))
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
        }
    });
}
