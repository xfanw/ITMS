"use stric;"

// json message
function show_json_message(status, msg){
    $('#json-message').show()
    $('#json_message_status').removeClass().addClass('modal-content-'+status)
    $('#json_message_msg').html(msg)
}

function hide_json_message(){
    $('#json-message').hide()
}
function closeBottomSection(){
    $('#bottomSection').hide()
}

// loader
function show_l6_loader(show_text=false){
    $('#loader-modal-L6').show()
    if (show_text){
        $('#loader-modal-L6-text').show()
    }
}

function hide_l6_loader(){
    $('#loader-modal-L6').hide()
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// multiple select drop down
$('#anchor').click( function () {
    var items = $('#anchor_items')
    if (items.is(":hidden")) {
        items.show();
    } else {
        items.hide();
    }
})


//add loader for form submit action
$('form').submit(function(){
    if (!(window.location.href.indexOf("login") > -1)) {
        show_l6_loader()
    }
})

$(function () {
    window.onpageshow = function(event) {
        if (event.persisted) {
            window.location.reload();
        }
    };
});

$('input').attr("autocomplete", "off");

String.prototype.toTitleCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};
// download file and then refresh page
function download_file_and_refresh(form_id, url){
    let request = new XMLHttpRequest();
        request.open('POST', url, true);
        request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
        request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        request.responseType = 'blob';
    
        request.onload = async function (e) {
            if (request.status === 200) {
                let filename = "";
                let disposition = request.getResponseHeader('Content-Disposition');
                // check if filename is given
                if (disposition && disposition.indexOf('attachment') !== -1) {
                    let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    let matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
                }
                let blob = request.response;
                if (window.navigator.msSaveOrOpenBlob) {
                    window.navigator.msSaveBlob(blob, filename);
                }
                else {
                    if (blob.type === 'application/json'){
                        let json_reponse = JSON.parse(await blob.text())
                        show_json_message(json_reponse.status, json_reponse.msg)
                    } else {
                        let downloadLink = window.document.createElement('a');
                        downloadLink.href = window.URL.createObjectURL(blob);
                        downloadLink.download = filename;
                        document.body.appendChild(downloadLink);
                        downloadLink.click();
                        document.body.removeChild(downloadLink);
                        window.location.reload()
                    }
                }
            } else {
                show_json_message('error', 'Download Connection Error.')
            }
        };
        request.send($('#'+form_id).serialize());
        $('#loader-modal-L6').hide();
}

/* drag/move */

var row;
function start(){
    row = event.target;
    $( ".move-y" ).draggable({ axis: "y" });
}
function dragover(){
    var e = event;
    e.preventDefault();
    target_tr = e.target.parentNode
    let children= Array.from(target_tr.parentNode.children);

    if (target_tr.tagName == 'TD')
        target_tr = target_tr.parentNode;

    if(children.indexOf(target_tr)>children.indexOf(row))
        target_tr.after(row);
    else
        target_tr.before(row);
}

// parse dict into options
function build_select_from_dict(field_name, opt_dict, default_value, col_width){
    var select_div = `<select name='${field_name}' class='form-control ${col_width}'>`
    for (var key in opt_dict){
        if (key == default_value){
            select_div +=`<option value=${key} selected>${opt_dict[key] }</option>`
        } else {
            select_div +=`<option value=${key}>${opt_dict[key] }</option>`
        }
    }
    select_div +='</select>'
    return select_div
}

function build_select_from_list(field_name, opt_list, default_value, col_width){
    var select_div = `<select name='${field_name}' class='form-control ${col_width}'>`
    for (var item of opt_list){
        if (item == default_value){
            select_div +=`<option selected>${item}</option>`
        } else {
            select_div +=`<option>${item}</option>`
        }
    }
    select_div +='</select>'
    return select_div
}
