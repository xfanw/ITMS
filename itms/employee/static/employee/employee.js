"use stric";


function delete_employee(employee_id, employee_name) {
    Swal.fire({
        title: `Delete Employee ${employee_id}`,
        html:  `
                <h4>Employee Name: ${employee_name}</h4>
                <div class='mt-3'><textarea id='comment' class='form-control' placeholder='Comment is required.'></textarea></div>
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
                show_json_message('error', 'Comments must be added to delete a Employee.')
            } else {
                show_l6_loader()
                $.ajax({
                    url: '/employee/delete_employee',
                    type: 'POST',
                    dataType: 'json',
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    data: {
                        'employee_id': employee_id,
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

function deactivate_employee(employee_id, employee_name) {
    Swal.fire({
        title: `Deactivate Employee ${employee_id}`,
        html:  `
                <h4>Employee Name: ${employee_name}</h4>
                <div class='mt-3'><textarea id='comment' class='form-control mt-2' placeholder='Comment is required.'>Employee Left Company.</textarea></div>
                `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: `Deactivate`,

    }).then(function (result) {
        if (result.isConfirmed) {
            var comment = $('#comment').val()
            if (comment.trim() === ''){
                // check is comment is added
                show_json_message('error', 'Comments must be added to delete a Employee.')
            } else {
                show_l6_loader()
                $.ajax({
                    url: '/employee/deactivate_employee',
                    type: 'POST',
                    dataType: 'json',
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    data: {
                        'employee_id': employee_id,
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

function activate_employee(employee_id, employee_name) {
    Swal.fire({
        title: `Activate Employee ${employee_id}`,
        html:  `
                <h4>Employee Name: ${employee_name}</h4>
                <div class='mt-3'><textarea id='comment' class='form-control mt-2' placeholder='Comment is required.'></textarea></div>
                `,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: `Activate`,

    }).then(function (result) {
        if (result.isConfirmed) {
            var comment = $('#comment').val()
            if (comment.trim() === ''){
                // check is comment is added
                show_json_message('error', 'Comments must be added to delete a Employee.')
            } else {
                show_l6_loader()
                $.ajax({
                    url: '/employee/activate_employee',
                    type: 'POST',
                    dataType: 'json',
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    data: {
                        'employee_id': employee_id,
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