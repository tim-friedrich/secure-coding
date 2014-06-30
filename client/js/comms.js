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
        event.preventDefault();
        gapi.client.hardcode.comms.addComm({
            'subject': $('#subject_input').val(),
            'receiver': $('#recipients_input').val(),
            'content': $('#content_input').val(),
            'item_id': $('form').attr('data-id')
        }).execute(function(resp){
            if (resp.code == "OK"){
                window.location.replace('/')
            }
            else{
                alert("An Error has occurred while deleting the item. The request returned with code: "+resp.code+" "+resp.message)
            }
        })
    })
}

google.appengine.secure.shop.initInbox = function() {
    comm_list_element = '<li data-id="" class="list-group-item">\
                <span class="subject"></span>\
                <span class="comm_date pull-right"></span>\
              </li>'

    gapi.client.hardcode.comms.listComm().execute(function(resp){
        if(resp.code == 'OK'){
            for(var x=0; x < resp.data.length; x++){
                new_element = $(comm_list_element).clone();
                new_element.attr('data-id', resp.data[x].comm_id);
                new_element.find('.subject').text(resp.data[x].subject);
                new_element.find('.comm_date').text(resp.data[x].timestamp);
                $('#comm_list').append(new_element);
            }
            $("li").on('click', function(event){
                window.location.replace('/comms/'+$(event.target).attr('data-id'))
            })
        }
    })
    google.appengine.secure.shop.hideLoadingDialog();
}
