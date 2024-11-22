$(window).on('load', function () {
    $('#div_id_verbs label.form-label').insertBefore('#div_id_verbs .selector')
})
$(window).on('load resize', function() {
    if (window.innerWidth < 992) {
        $('.selector').addClass('stacked');
    } else {
        $('.selector').removeClass('stacked');
    }
});