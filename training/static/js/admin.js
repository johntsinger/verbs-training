// Adds dependent fields to result add form
// <select> must be ordered: [A, B, C, ...] -> B depends of A value, C depends of B value, ...
// Selects A to get B values, B to get C values, ...

window.addEventListener("load", function() {
    const $ = django.jQuery;
    $.fn.dependentSelect2 = function() {
        let selectElements = this // array of elements
        $.each(this, function(i, element) {
            // Gets the previous element; return undefined for the first element
            let previousElement = selectElements[i - 1]
            // Clears value if previous field change and trigger change on cascade
            if (previousElement) {
                $(previousElement).change(function () {
                    $(element).val(null).trigger("change");
                });
            }
            $(element).select2({
                ajax: {
                    data: (params) => {
                        data = {
                            term: params.term,
                            page: params.page,
                            // URL data required by Django
                            app_label: element.dataset.appLabel,
                            model_name: element.dataset.modelName,
                            field_name: element.dataset.fieldName,
                        };
                        // Add all previous elements value to URL data; uses element id as key
                        $.each(selectElements, function(j, element) {
                            prev = selectElements[i - (j + 1)]
                            if ($(prev).val()) {
                                data[prev.id] = $(prev).val()
                            } else {
                                return false
                            }
                        })
                        // if (previousElement) {
                        //     data[previousElement.id] = $(previousElement).val();
                        // }
                        return data;
                    },
                },
                // Adds a placeholder if the value on which this select depends has not been chosen
                templateSelection: function (data) {
                    if (data.id === '' && !$(previousElement).val() && previousElement) {
                        return "Select a " + previousElement.name + " first.";
                    }
                    return data.text;
                },
                // Displays the search box only if the number of results >= 10
                minimumResultsForSearch: 10
            });
        })
    }

    // Initialize custom Select2
    $("select").dependentSelect2();
});