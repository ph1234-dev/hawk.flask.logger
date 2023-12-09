$('input[type="checkbox"][name="is_lang_correct_checkbox"]').change(function (event) {
    let id = $(this).attr('id')
    let val = $(this).val()
    console.log(`Val:: ${val}`)
    let status = 0
    if ( val == "False"){
        status == "True"
    }else{
        status == "False"
    }

    console.log(`Id: ${id}\n\tValue:${val}\n\tChanging ${val} to ${status}`)
    $(this).val(status);

    const DEV_URL = 'http://127.0.0.1:5000/test/api/update/lang'
    $.ajax({
        url: DEV_URL,
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: JSON.stringify({
            id: id,
            status: status
        }),
        success: function (response) {
            console.log('\tRequest successful');
            $(this).prop('checked', status);
            console.log('\tUI Update successful');
        },
        error: function (xhr, status, error) {
            console.error('Request failed with status ' + status + ': ' + error);
            $(this).prop('checked', status);
        }
    });
})


$('input[type="checkbox"][name="is_reply_correct_checkbox"]').change(function (event) {
    let id = $(this).attr('id')
    let val = $(this).val()
    let status = 0

    status = (val == "False") ? "True" : "False"

    console.log(`Id: ${id}\n\tValue:${val}\n\tChanging ${val} to ${status}`)
    $(this).val(status);

    const DEV_URL = 'http://127.0.0.1:5000/test/api/update/reply'
    $.ajax({
        url: DEV_URL,
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: JSON.stringify({
            id: id,
            status: status
        }),
        success: function (response) {
            console.log('\tRequest successful');
            $(this).prop('checked', status);
            console.log('\tUI Update successful');
        },
        error: function (xhr, status, error) {
            console.error('Request failed with status ' + status + ': ' + error);
            $(this).prop('checked', status);
        }
    });
})