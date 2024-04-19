function moveCursorOnFocus(element) {
    var temp_value=element.value;
    element.value='';
    element.value=temp_value
}

window.setTimeout(function() {
    $(".alert-auto-close").fadeTo(500, 0).slideUp(500, function(){
        $(this).alert('close'); 
    });
}, 5000);