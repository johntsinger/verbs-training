/*
##################
#  Slick config  #
##################
*/

var settings = {
    dots: true,
    slidesToShow: 2,
    slidesToScroll: 2,
    infinite: false,
    responsive: [
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
});