"use strict";

function assign_account(action, id, employee, account_type, account){
    hide_json_message();
    Swal.fire({
        title: `${action} Account `,

        html:  `
        <form method='POST' action='/account/assign_account_action' id='assign_account_form' class='col-md-12 row'>
            <input name='account_id' hidden value='${id}'></input>
            <div class='col-md-5 my-3'>
                <label>Employee Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='employee' class='form-control col-md-9' value='${employee}' readonly>
            </div>
            <div class='col-md-5 my-3'>
                <label>Account Type:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='account_type' class='form-control col-md-9' value='${account_type}' readonly>
            </div>
            <div class='col-md-5 my-3'>
                <label>Account:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='account' class='form-control col-md-9' value='${account}'>
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        confirmButtonText: `Confirm`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#assign_account_form').submit();
        }
    }) // end Swal
}

function delete_account(action, id, employee, account_type, account){
    hide_json_message();
    Swal.fire({
        title: `${action} Account `,

        html:  `
        <form method='POST' action='/account/delete_account_action' id='delete_account_form' class='col-md-12 row'>
            <input name='account_id' hidden value='${id}'></input>
            <div class='col-md-5 my-3'>
                <label>Employee Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='employee' class='form-control col-md-9' value='${employee}' readonly>
            </div>
            <div class='col-md-5 my-3'>
                <label>Account Type:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='account_type' class='form-control col-md-9' value='${account_type}' readonly>
            </div>
            <div class='col-md-5 my-3'>
                <label>Account:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='account' class='form-control col-md-9' value='${account}' readonly>
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        confirmButtonText: `Confirm Delete`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#delete_account_form').submit();
        }
    }) // end Swal
}