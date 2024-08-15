"use strict";

$(function(){
    $('#part_1_header').click()
})

$('#group_name').change(function(){
    if($(this).val() === 'new_auth_group'){
        Swal.fire({
            title: `New Auth Group Name`,
            html:  `<form id='new_auth_group_form' action='/admin_itms/admin_create_group_auth' >
                    <input class='form-control mt-2' name='new_group_name'>
                    </form>
                    `,
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: `Create`,
            allowOutsideClick: false
    
        }).then(function (result) {
            if (result.isConfirmed) {
                $('#new_auth_group_form').submit()
            }
        }); // end swal

    } else {
        $('form').submit()
    }
})

function admin_add_group_auth(perm_id){
    $.ajax({
        url: '/admin_itms/admin_add_group_auth',
        type: 'GET',
        dataType: 'json',
        data: {
            'perm_id': perm_id,
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

function admin_remove_group_auth(perm_id){
    $.ajax({
        url: '/admin_itms/admin_remove_group_auth',
        type: 'GET',
        dataType: 'json',
        data: {
            'perm_id': perm_id,
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