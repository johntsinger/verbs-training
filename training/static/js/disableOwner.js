$(window).on('load', function() {
    const $ = django.jQuery;
    $('#id_type').change(function () {
        console.log($(this))
        if ($(this).val() === 'defaulttable') {
            $('#id_owner').val(null).trigger('change').prop('disabled', 'disabled');
            $('.select2-selection__placeholder').text('Disabled for Default Table.');
        } else {
            $('.select2-selection__placeholder').text('');
            $('#id_owner').prop('disabled', false)
        }
    })
    
})