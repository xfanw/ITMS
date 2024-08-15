"use strict";

function add_business_unit(){
    let bg_select = `<select class='form-control col-md-9' name='bg_name'><option selected disabled>-- Select BG --</option>`
    for (var bg_name of bg_name_list){
        bg_select += `<option>${bg_name}</option>`        
    }
    bg_select += `</select>`

    Swal.fire({
        title: `Add Business Unit`,

        html:  `
        <form method='POST' action='/department/add_business_unit' id='add_bu_form' class='col-md-12 row'>
            <div class='col-md-5 my-3'>
                <label><span class='text-danger'>*</span>BU Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='bu_name' class='form-control col-md-9' autocomplete='off'>
            </div>
            <div class='col-md-5 my-3'>
                <label>BU Manager:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='bu_manager' class='form-control col-md-9' autocomplete='off'>
            </div>
            <div class='col-md-5 my-3'>
                <label><span class='text-danger'>*</span>BG Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                ${bg_select}
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        confirmButtonText: `Confirm`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#add_bu_form').submit();
        }
    }) // end Swal
}


function edit_business_unit(bu_name, bu_manager, curr_bg_name){
    let bg_select = `<select class='form-control col-md-9' name='bg_name'>`
    for (var bg_name of bg_name_list){
        if (curr_bg_name === bg_name){
            bg_select += `<option selected>${bg_name}</option>` 
        } else{
            bg_select += `<option>${bg_name}</option>`  
        }
    }
    bg_select += `</select>`

    Swal.fire({
        title: `Edit Business Unit ${bu_name}`,

        html:  `
        <form method='POST' action='/department/edit_business_unit' id='edit_bu_form' class='col-md-12 row'>
            <div class='col-md-5 my-3'>
                <label>BU Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='bu_name' class='form-control col-md-9' value='${bu_name}' readonly>
            </div>
            <div class='col-md-5 my-3'>
                <label>BU Manager:</label>
            </div>
            <div class='col-md-7 my-3'>
                <input name='bu_manager' class='form-control col-md-9' value='${bu_manager}'>
            </div>
            <div class='col-md-5 my-3'>
                <label><span class='text-danger'>*</span>BG Name:</label>
            </div>
            <div class='col-md-7 my-3'>
                ${bg_select}
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        confirmButtonText: `Confirm`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#edit_bu_form').submit();
        }
    }) // end Swal
}