/*
##################
#  Slick config  #
##################
*/

var settings = {
    dots: true,
    arrows: true,
    slidesToShow: 3,
    slidesToScroll: 3,
    infinite: false,
    dotsClass: "slick-dots",
    responsive: [
        {
            breakpoint: 992,
            settings: {
                dots: true,
                slidesToShow: 2,
                slidesToScroll: 2,
            }
        },
        {  
            breakpoint: 476,
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

var defaulttableSettings = {
    ...settings,
    appendDots: $("#default-tables .slider-controls .dots-container"),
    prevArrow: $("#default-tables .slider-controls .prev-container .prev"),
    nextArrow: $("#default-tables .slider-controls .next-container .next")
}

var usertableSettings = {
    ...settings,
    appendDots: $("#user-tables .slider-controls .dots-container"),
    prevArrow: $("#user-tables .slider-controls .prev-container .prev"),
    nextArrow: $("#user-tables .slider-controls .next-container .next")
}

$(document).ready(function(){
    $('.default-tables__slick').slick(defaulttableSettings);
    $('.user-tables__slick').slick(usertableSettings);
});