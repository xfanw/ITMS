"use strict";

$(function(){
    $('#part_1_header').click()
})

function reset_user_password(user_id){
    hide_json_message()
    $.ajax({
        url: '/admin_itms/admin_reset_password',
        type: 'POST',
        dataType: 'json',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {
            'user_id': user_id,
            'password' :'Foxconn1',
        },
        success: function (response) {
            if (response.status === 'success'){
                show_json_message(response.status, response.msg)
            } else {
                show_json_message(response.status, response.msg)
            }
            

        },
        error: function () {
            show_json_message('error', 'Connection Error.')
        },
    }) // end ajax
}