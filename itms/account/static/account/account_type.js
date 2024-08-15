"use strict";

function add_account_type(){
    hide_json_message();
    Swal.fire({
        title: `Add New Account Type`,
        html:  `
        <form method='POST' action='/account/add_account_type' id='add_account_form' class='col-md-12 row'>
            <div class='col-md-5 my-3'>
                <span class='text-danger'>*</span><label>Account Type Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='account_type' class='form-control col-md-9'>
            </div>
            <div class='col-md-5 my-3'>
                <span class='text-danger'>*</span><label>Person In Charge:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='person_in_charge' class='form-control col-md-9'>
            </div>
            <div class='col-md-5 my-3'>
                <span class='text-danger'>*</span><label>PIC Email:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input type='email' name='pic_email' class='form-control col-md-9'>
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        confirmButtonText: `Confirm`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#add_account_form').submit();
        }
    }) // end Swal
}

function edit_account_type(account_type, person_in_charge, pic_email){
    hide_json_message();
    Swal.fire({
        title: `Edit Acount Type ${account_type}`,

        html:  `
        <form method='POST' action='/account/edit_account_type' id='edit_account_form' class='col-md-12 row'>
            <div class='col-md-5 my-3'>
                <label>Account Type Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='account_type' class='form-control col-md-9' value='${account_type}' readonly>
            </div>
            <div class='col-md-5 my-3'>
                <label>Person In Charge:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='person_in_charge' class='form-control col-md-9' value='${person_in_charge}'>
            </div>
            <div class='col-md-5 my-3'>
                <label>PIC Email:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input type='email' name='pic_email' class='form-control col-md-9' value='${pic_email}'>
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        confirmButtonText: `Confirm`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#edit_account_form').submit();
        }
    }) // end Swal
}