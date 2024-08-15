"use strict";

function add_cost_center(){
    let bu_select = `<select class='form-control col-md-9' name='bu_name'><option selected disabled>-- Select BU --</option>`
    for (var bu_name of bu_name_list){
        bu_select += `<option>${bu_name}</option>`        
    }
    bu_select += `</select>`

    Swal.fire({
        title: `Add Cost Center`,

        html:  `
        <form method='POST' action='/department/add_cost_center' id='add_cc_form' class='col-md-12 row'>
            <div class='col-md-5 my-3'>
                <label>CC Code:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='cc_code' class='form-control col-md-9'>
            </div>
            <div class='col-md-5 my-3'>
                <label>CC Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='cc_name' class='form-control col-md-9'>
            </div>
            <div class='col-md-5 my-3'>
                <label>CC Manager:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='cc_manager' class='form-control col-md-9'>
            </div>
            <div class='col-md-5 my-3'>
                <label>BU Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                ${bu_select}
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        confirmButtonText: `Confirm`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#add_cc_form').submit();
        }
    }) // end Swal
}

function edit_cost_center(cc_code, cc_name, cc_manager, curr_bu_name){
    let bu_select = `<select class='form-control col-md-9' name='bu_name'>`
    for (var bu_name of bu_name_list){
        if (curr_bu_name === bu_name){
            bu_select += `<option selected>${bu_name}</option>` 
        } else{
            bu_select += `<option>${bu_name}</option>`  
        }
    }
    bu_select += `</select>`

    Swal.fire({
        title: `Edit Cost Center ${cc_code}`,

        html:  `
        <form method='POST' action='/department/edit_cost_center' id='edit_cc_form' class='col-md-12 row'>
            <div class='col-md-5 my-3'>
                <label>CC Code:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='cc_code' class='form-control col-md-9' value='${cc_code}' readonly>
            </div>
            <div class='col-md-5 my-3'>
                <label>CC Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='cc_name' class='form-control col-md-9' value='${cc_name}'>
            </div>
            <div class='col-md-5 my-3'>
                <label>CC Manager:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='cc_manager' class='form-control col-md-9' value='${cc_manager}'>
            </div>
            <div class='col-md-5 my-3'>
                <label>BU Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                ${bu_select}
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        confirmButtonText: `Confirm`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#edit_cc_form').submit();
        }
    }) // end Swal
}