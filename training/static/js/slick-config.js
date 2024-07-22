/*
##################
#  Slick config  #
##################
*/

var settings = {
    dots: true,
    slidesToShow: 3,
    slidesToScroll: 3,
    infinite: false,
    responsive: [
        {
            breakpoint: 1400,
            settings: {
                dots: true,
                slidesToShow: 2,
                slidesToScroll: 2,
            }
        },
        {
            breakpoint: 992,
            settings: {
                dots: true,
                slidesToShow: 1,
                slidesToScroll: 1,
            }
        }
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
    ]
}

$(document).ready(function(){
    $('.default-tables__slick').slick(settings);
    $('.user-tables__slick').slick(settings);

    // Update slidesToShow based on the number of slides
    var defaultTableSlick = $('.default-tables__slick')[0].slick
    var userTableSlick = $('.user-tables__slick')[0].slick

    if (defaultTableSlick.slideCount < defaultTableSlick.options.slidesToShow) {
        defaultTableSlick.options.slidesToShow = defaultTableSlick.slideCount
    }
    if (userTableSlick.slideCount < userTableSlick.options.slidesToShow) {
        userTableSlick.options.slidesToShow = userTableSlick.slideCount
    }
});