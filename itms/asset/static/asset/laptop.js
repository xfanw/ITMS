"use strict";

function add_laptop() {
    Swal.fire({
        title: `Add Laptop`,
        html:  `
        <form method='POST' action='/asset/add_laptop' id='add_laptop_form' class='col-md-12 row'>
            <div class='col-md-5 my-1'>
                <label>Asset Category:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='asset_type' class='form-control col-md-9' value='Laptop' style="background-color:Gainsboro" readonly>
            </div>
            <div class='col-md-5 my-1'>
                <label><span class='text-danger'>*</span>Asset Label:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='asset_label' class='form-control col-md-9' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label><span class='text-danger'>*</span>SN:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='serial_number' class='form-control col-md-9' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Brand:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='brand' class='form-control col-md-9' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Model:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='model' class='form-control col-md-9' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Processor:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='processor' class='form-control col-md-9' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Ram:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input type='number' name='ram' min='0' class='form-control col-md-9' autocomplete='off' placeholder='GB'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Storage:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input type='number' name='storage' min='0' class='form-control col-md-9' autocomplete='off' placeholder='GB'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Purchase Date:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input type='date' name='purchase_date' class='form-control col-md-9' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Purchase Cost:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input type='number' name='purchase_cost' min='0' class='form-control col-md-9' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Status:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='status' class='form-control col-md-9' value='IDLE' style="background-color:Gainsboro" readonly>
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        confirmButtonText: `Confirm`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#add_laptop_form').submit();
        }
    }) // end Swal
}


function edit_laptop(asset_label, brand, model, serial_number, processor, ram, storage, purchase_date, purchase_cost, status) {
    Swal.fire({
        title: `Edit Laptop ${asset_label}`,
        html:  `
        <form method='POST' action='/asset/edit_laptop' id='edit_laptop_form' class='col-md-12 row'>
            <div class='col-md-5 my-1'>
                <label><span class='text-danger'>*</span>Asset Label:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='asset_label' class='form-control col-md-9' value='${asset_label}' autocomplete='off' style="background-color:Gainsboro" readonly>
            </div>
            <div class='col-md-5 my-1'>
                <label><span class='text-danger'>*</span>SN:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='serial_number' class='form-control col-md-9' value='${serial_number}' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Brand:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='brand' class='form-control col-md-9' value='${brand}' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Model:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='model' class='form-control col-md-9' value='${model}' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Processor:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='processor' class='form-control col-md-9' value='${processor}' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Ram:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input type='number' name='ram' min='0' class='form-control col-md-9' value='${ram}' autocomplete='off' placeholder='GB'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Storage:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input type='number' name='storage' min='0' class='form-control col-md-9' value='${storage}' autocomplete='off' placeholder='GB'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Purchase Date:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input type='date' name='purchase_date' class='form-control col-md-9' value='${purchase_date}' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Purchase Cost:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input type='number' name='purchase_cost' min='0' class='form-control col-md-9' value='${purchase_cost}' autocomplete='off'>
            </div>
            <div class='col-md-5 my-1'>
                <label>Status:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='status' class='form-control col-md-9' value='${status}' autocomplete='off' style="background-color:Gainsboro" readonly>
            </div>
        </form>
        `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        confirmButtonText: `Confirm`,
        width:'40%',

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#edit_laptop_form').submit();
        }
    }) // end Swal
}


function delete_laptop(id, asset_label, serial_number) {
    Swal.fire({
        title: `Delete Laptop ${asset_label}`,
        html:  `
                <h4>(SN: ${serial_number})</h4>
                <textarea id='comment' class='form-control' placeholder='Comment is required.'></textarea>
                `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: `Delete`,

    }).then(function (result) {
        if (result.isConfirmed) {
            var comment = $('#comment').val()
            if (comment.trim() === ''){
                // check is comment is added
                show_json_message('error', 'Comments must be added to delete a Laptop.')
            } else {
                show_l6_loader()
                $.ajax({
                    url: '/asset/delete_laptop',
                    type: 'POST',
                    dataType: 'json',
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    data: {
                        'laptop_id': id,
                        'comment': comment,
                    },
                    success: function (response) {
                        hide_l6_loader()

                        show_json_message(response.status, response.msg)
                        if (response.status === 'success'){
                            setTimeout(function () {
                                location.reload()
                            }, 1000);
                        }
                    },
                    error: function () {
                        hide_l6_loader()
                        show_json_message('error', 'Connection Error.')
                    },
                }); // end ajax
            }
        }
    }) // end Swal
}