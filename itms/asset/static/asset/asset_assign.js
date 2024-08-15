"use strict";

function assign_asset(employee_id, name){
    hide_json_message();
    Swal.fire({
        title: `Assign Asset `,

        html:  `
        <form method='POST' action='/asset/assign_asset_action' id='assign_asset_form' class='col-md-12 row'>
            <input name='employee_id' hidden value='${employee_id}'></input>
            <div class='col-md-5 my-3'>
                <label>Employee Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='name' class='form-control col-md-9' value='${name}' autocomplete='off' style="background-color:Gainsboro" readonly>
            </div>
            <div class='col-md-5 my-3'>
                <label><span class='text-danger'>*</span>Asset Label:</label>
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
            $('#assign_asset_form').submit();
        }
    }) // end Swal
    
}