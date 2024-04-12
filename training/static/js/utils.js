function moveCursorOnFocus(element) {
    var temp_value=element.value;
    element.value='';
    element.value=temp_value
}