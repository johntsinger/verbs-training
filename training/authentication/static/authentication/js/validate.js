function addErrorAlreadyInUse (element, text) {
    let id = element.attr('id')
    if ($('error_exists_' + id).length) {
        return;
    }
    element.after(
        $('<p />', {
            id: 'error_exists_' + id,
            class: 'already-in-use-feedback'
        }).append(
            $('<strong />', {
                text: text
            })
        )
    );
    element.addClass('already-in-use');
}

function clearErrorAlreadyInUse (element) {
    let id = element.attr('id')
    $('#error_exists_' + id).remove();
    element.removeClass('already-in-use');
}

var getAjax = (element, url, data, errorMessage) => {
    return {
        url: url,
        data: data,
        dataType: 'json',
        success: function (response) {
            if (response.exists) {
                addErrorAlreadyInUse(
                    element,
                    text=errorMessage
                );
            } else {
                clearErrorAlreadyInUse(element);
            }
        }
    }
}

function getAjaxData (ids) {
    data = {}
    $.each(ids, function (key, value) {
        data[key] = $('#' + value).val()
    })
    return data
}

var defaultOptions = {
    doneTypingInterval: 1000,
    url: '',
    data: {},
    errorMessage: ''
}

$.fn.validate = function(newOptions) {
    var typingTimer;
    let element = this;
    newOptions = newOptions || {};
    let options = $.extend(true, {}, defaultOptions, newOptions);
    element.on('input', function () {
        clearTimeout(typingTimer);
        if (element.val()) {
            typingTimer = setTimeout(
                function () {
                    let data = getAjaxData(options.data)
                    $.ajax(
                        getAjax(
                            element=element,
                            url=options.url,
                            data=data,
                            errorMessage=options.errorMessage
                        )
                    );
                },
                options.doneTypingInterval
            );
        } else {
            clearErrorAlreadyInUse(element);
        }
    });
}

$('#id_username').validate({
    doneTypingInterval: 1000,
    url: '/validators/check-username/',
    data: {username: 'id_username'},
    errorMessage: 'This ursername is already taken.'
});

$('#id_password1').validate({
    doneTypingInterval: 1000,
    url: '/validators/check-password/',
    data: {
        password: 'id_password1',
        email: 'id_email',
        username: 'id_username'
    },
    errorMessage: 'test'
})

// $("#id_username").on('input', function () {
//     var input = $(this)
//     var username = $(this).val();
//     $.ajax({
//         url: '/validators/check-username/',
//         data: {
//             'username': username
//         },
//         dataType: 'json',
//         success: function (data) {
//             if (data.username_exists) {
//                 $('#id_username').after(
//                     $('<p />', {
//                         id: 'id_username_exists',
//                         class: 'username-exists'
//                     }).append(
//                         $('<strong />', {
//                             text: 'This ursername is already taken.'
//                         })
//                     )
//                 )
//                 input.addClass('username-invalid');
//                 $('#submit-form').prop("disabled", true);
//             } else {
//                 $('#id_username_exists').remove()
//                 input.removeClass('username-invalid');
//                 $('#submit-form').prop('disabled', false);
//             }
//         }
//     });
// });

// $("#id_password1").on('input', function () {
//     var input = $(this)
//     var password = $(this).val();
//     var username = $('#id_username').val()
//     var email = $('#id_email').val()
//     $.ajax({
//         url: '/validators/check-password/',
//         data: {
//             'password': password,
//             'username': username,
//             'email': email
//         },
//         dataType: 'json',
//         success: function (data) {
//             console.log(data)
//         }
//     });
// });