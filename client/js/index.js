google.appengine.secure.shop.enableButtons = function() {
    $('#searchButton').on('click', function(event){
        event.preventDefault()
        google.appengine.secure.shop.search();
    })
};

google.appengine.secure.shop.search = function(){
    google.appengine.secure.shop.showLoadingDialog();
    console.log("Searching for: " + $('#query').val());
    gapi.client.hardcode.search.query({
        'query': $('#query').val()
    }).execute(function(resp){
        console.log(resp);
        $('tbody').children().remove()
        if (resp.code == "OK" && resp.data != null){
            for(i=0; i < resp.data.length; i++){
                item = resp.data[i];
                $("tbody").append('' +
                    '<tr data-id="'+item.item_id+'">' +
                        '<td>'+item.title+'</td>' +
                        '<td>'+item.description+'</td>' +
                        '<td>'+item.price+'$</td>' +
                    '</tr>');
            }
            $('tbody').find('tr').on('click', function(event){
                window.location.replace('/items/'+$(event.target).parent().attr('data-id'))
            })
        } else {
            $("tbody").append('' +
                    '<tr>' +
                        '<td colspan="3">Sorry, no items found matching your querry.</td>' +
                    '</tr>');
        }
        google.appengine.secure.shop.hideLoadingDialog();
    });
}