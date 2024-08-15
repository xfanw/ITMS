"use strict";

function replace_asset(employee_id, name, asset_type, old_asset_label){
    hide_json_message();
    Swal.fire({
        title: `Replace Asset ${asset_type}`,

        html:  `
        <form method='POST' action='/asset/replace_asset_action' id='replace_asset_form' class='col-md-12 row'>
            <input name='employee_id' hidden value='${employee_id}'></input>
            <div class='col-md-5 my-3'>
                <label>Employee Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='name' class='form-control col-md-9' value='${name}' autocomplete='off' style="background-color:Gainsboro" readonly>
            </div>
            <div class='col-md-5 my-3'>
                <label>Previous Asset Label:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='old_asset_label' class='form-control col-md-9' value='${old_asset_label}' autocomplete='off' readonly>
            </div>
            <div class='col-md-5 my-3'>
                <label><span class='text-danger'>*</span>New Asset Label:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='asset_label' class='form-control col-md-9' placeholder="Please Scan" autocomplete='off'>
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        confirmButtonText: `Confirm`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#replace_asset_form').submit();
        }
    }) // end Swal
    
}


function delete_asset(employee_id, name, asset_type, asset_label){
    hide_json_message();
    Swal.fire({
        title: `Delete Assigned ${asset_type} `,

        html:  `
        <form method='POST' action='/asset/delete_asset_action' id='delete_asset_form' class='col-md-12 row'>
            <input name='employee_id' hidden value='${employee_id}'></input>
            <input name='asset_type' hidden value='${asset_type}'></input>
            <div class='col-md-5 my-3'>
                <label>Employee Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='name' class='form-control col-md-9' value='${name}' autocomplete='off' style="background-color:Gainsboro" readonly>
            </div>
            <div class='col-md-5 my-3'>
                <label>Asset Label:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='asset_label' class='form-control col-md-9' value='${asset_label}' autocomplete='off' readonly>
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        confirmButtonText: `Confirm`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#delete_asset_form').submit();
        }
    }) // end Swal
}