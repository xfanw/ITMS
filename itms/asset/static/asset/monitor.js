"use strict";

function add_monitor() {
    Swal.fire({
        title: `Add Monitor`,
        html:  `
        <form method='POST' action='/asset/add_monitor' id='add_monitor_form' class='col-md-12 row'>
            <div class='col-md-5 my-1'>
                <label>Asset Category:</label>
            </div>
            <div class='col-md-7 my-1'>
                <input name='asset_type' class='form-control col-md-9' value='Monitor' style="background-color:Gainsboro" readonly>
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
                <label><span class='text-danger'>*</span>Screen Size:</label>
            </div>
            <div class='col-md-7 my-1'>
                <select name='screen_size' class='form-control col-md-9'>
                    <option selected disabled>--Choose--</option>
                    <option value='19'>19 inches</option>
                    <option value='22'>22 inches</option>
                    <option value='23'>23 inches</option>
                    <option value='24'>24 inches</option>
                    <option value='27'>27 inches</option>
                    <option value='32'>32 inches</option>
                    <option value='34'>34 inches</option>
                    <option value='38'>38 inches</option>
                </select>
            </div>
            <div class='col-md-5 my-1'>
                <label><span class='text-danger'>*</span>Resolution:</label>
            </div>
            <div class='col-md-7 my-1'>
                <select name='resolution' class='form-control col-md-9'>
                    <option selected disabled>--Choose--</option>
                    <option value='1366 x 768'>1366 x 768 (HD)</option>
                    <option value='1920 x 1080'>1920 x 1080 (Full HD)</option>
                    <option value='2560 x 1440'>2560 x 1440 (Quad HD)</option>
                    <option value='3840 x 2160'>3840 x 2160 (Ultra HD)</option>
                    <option value='5120 x 2880'>5120 x 2880 (5K)</option>
                    <option value='7680 x 4320'>7680 x 4320 (8K)</option>
                </select>
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
            $('#add_monitor_form').submit();
        }
    }) // end Swal
}


function edit_monitor(asset_label, brand, model, serial_number, screen_size, resolution, purchase_date, purchase_cost, status) {
    Swal.fire({
        title: `Edit Monitor ${asset_label}`,
        html:  `
        <form method='POST' action='/asset/edit_monitor' id='edit_monitor_form' class='col-md-12 row'>
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
                <label>Screen Size:</label>
            </div>
            <div class='col-md-7 my-1'>
                <select id='screen_sizeSelect' name='screen_size' class='form-control col-md-9'>
                    <option value='19'>19 inches</option>
                    <option value='22'>22 inches</option>
                    <option value='23'>23 inches</option>
                    <option value='24'>24 inches</option>
                    <option value='27'>27 inches</option>
                    <option value='32'>32 inches</option>
                    <option value='34'>34 inches</option>
                    <option value='38'>38 inches</option>
                </select>
            </div>
            <div class='col-md-5 my-1'>
                <label>Resolution:</label>
            </div>
            <div class='col-md-7 my-1'>
                <select id='resolutionSelect' name='resolution' class='form-control col-md-9'>
                    <option value='1366 x 768'>1366 x 768 (HD)</option>
                    <option value='1920 x 1080'>1920 x 1080 (Full HD)</option>
                    <option value='2560 x 1440'>2560 x 1440 (Quad HD)</option>
                    <option value='3840 x 2160'>3840 x 2160 (Ultra HD)</option>
                    <option value='5120 x 2880'>5120 x 2880 (5K)</option>
                    <option value='7680 x 4320'>7680 x 4320 (8K)</option>
                </select>
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
        didOpen: () => {
            // Auto-select the value in the dropdown when Swal.fire is opened
            document.getElementById('screen_sizeSelect').value = screen_size;
            document.getElementById('resolutionSelect').value = resolution;
        }

    }).then(function (result) {
        if (result.isConfirmed) {
            $('#edit_monitor_form').submit();
        }
    }) // end Swal
}


function delete_monitor(id, asset_label, serial_number) {
    Swal.fire({
        title: `Delete Monitor ${asset_label}`,
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
                show_json_message('error', 'Comments must be added to delete a Monitor.')
            } else {
                show_l6_loader()
                $.ajax({
                    url: '/asset/delete_monitor',
                    type: 'POST',
                    dataType: 'json',
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    data: {
                        'monitor_id': id,
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