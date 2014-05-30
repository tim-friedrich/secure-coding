
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
        '<div class="item_detail">\
		    <div class="title"></div>\
			<div class="description"></div>\
			<div class="price"></div>\
			<div class="footer">\
				<div class="sellerName"></div>\
				<div class="creationTime"></div>\
			</div>\
		</div>';
    new_item = $(item_template).clone();
    new_item.find('.title').text(item['title']);
    new_item.find('.description').text(item['description']);
    new_item.find('.price').text(item['price']+" $");
    new_item.find('.sellerName').text(item['owner']['email']);
    new_item.find('.creationTime').text(item['created_at']);
    return new_item
};
