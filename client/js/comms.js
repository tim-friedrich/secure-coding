google.appengine.secure.shop.initAddComm = function() {
    item_id = $('form').attr('data-id')
    if(item_id){
        gapi.client.hardcode.items.getItem({ id: item_id }).execute(function(resp){
            $('#item_title_input').text(resp.data[0].title);
            $('#item_price_input').text(resp.data[0].price);
            $('#recipients_input').val(resp.data[0].owner.user_id+";")
        });
    }
    else{
        $('#item_title_input').hide();
        $('#item_price_input').hide();
    }
    $('button').on('click', function(event){
        gapi.client.hardcode.comms.addComm({
            'subject': $('#subject_input').val(),
            'receiver': $('#recipients_input').val(),
            'content': $('#content_input').val(),
            'item_id': $('form').attr('data-id')
        }).execute(function(resp){
            if (resp.code == "OK"){
                window.location.replace('/') //later to comms
            }
            else{
                alert("An Error has occurred while deleting the item. The request returned with code: "+resp.code+" "+resp.message)
            }
        })
    })
}
