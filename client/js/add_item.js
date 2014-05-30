/**
 * Created by tim on 5/30/14.
 */
google.appengine.secure.shop.load = function(){
    $('#submit_button').on('click', function(event){
        event.preventDefault();
        gapi.client.hardcode.items.addItem(
            {
                'title': $('form').find('#item_name').val(),
                'description': $('form').find('#item_description').val(),
                'price': $('form').find('#item_price').val()
            }
        ).execute(function(resp){
                if(resp.code != "OK"){
                    alert("An Error has occurred while adding the item. The request returned with code: "+resp.code+" "+resp.message)
                }
            });
        return false;
    });
};