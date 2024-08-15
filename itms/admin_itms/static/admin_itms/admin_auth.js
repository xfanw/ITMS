"use strict";

$(function(){
    $('#part_1_header').click()
})

function admin_add_user_auth(user_id){
    $.ajax({
        url: '/admin_itms/admin_add_user_auth',
        type: 'GET',
        dataType: 'json',
        data: {
            'user_id': user_id,
            'auth_group' :curr_auth_group,
        },
        success: function (response) {
            if (response.status === 'success'){
                show_json_message(response.status, response.msg)
                setTimeout(function () {
                    location.reload()
                }, 1500);

            } else {
                show_json_message(response.status, response.msg)
            }
            

        },
        error: function () {
            show_json_message('error', 'Connection Error.')
        },
    }) // end ajax
}

function admin_remove_user_auth(user_id){
    $.ajax({
        url: '/admin_itms/admin_remove_user_auth',
        type: 'GET',
        dataType: 'json',
        data: {
            'user_id': user_id,
            'auth_group' :curr_auth_group,
        },
        success: function (response) {
            if (response.status === 'success'){
                show_json_message(response.status, response.msg)
                setTimeout(function () {
                    location.reload()
                }, 1500);

            } else {
                show_json_message(response.status, response.msg)
            }
            

        },
        error: function () {
            show_json_message('error', 'Connection Error.')
        },
    }) // end ajax
}