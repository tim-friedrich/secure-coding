google.appengine.secure.shop.loadUser = function(){
    var request = {}

    gapi.client.hardcode.users.getUser({ id: $('#user').attr('data-id') }).execute(function(resp){
        $user = $('#user');
        if (resp.code == "OK"){
            user = resp.data[0];
            $content = $('#content');
            $content.find('#name').text(user.name);
            $content.find('#email').text(user.email);
            $content.find('#description').text(user.description);
            $content.find('#user_image').attr('src', user.image_url);
        }
    });
}

google.appengine.secure.shop.initSettingsPage = function(){
    gapi.client.hardcode.users.getUser({ id: $('#user').attr('data-id') }).execute(function(resp){
        $user = $('#user');
        if (resp.code == "OK"){
            user = resp.data[0];
            $content = $('#content');
            $content.find('#user_name').val(user.name);
            $content.find('#user_description').val(user.description);
            $content.find('#user_image').val(user.image_url);
        }
    });

    $('#submit_button').on('click', function(event){
        event.preventDefault();
        gapi.client.hardcode.users.modUser(
            {
                'name': $('form').find('#user_name').val(),
                'user_id': $('#user').attr('data-id'),
                'description': $('form').find('#user_description').val(),
                'image_url': $('form').find('#user_image').val()
            }
        ).execute(function(resp){
                if(resp.code != "OK"){
                    alert("An Error has occurred while adding the item. The request returned with code: "+resp.code+" "+resp.message)
                }
                else{
                    window.location.replace('/users/'+$('#user').attr('data-id'))
                }
            });
        return false;
    });
}