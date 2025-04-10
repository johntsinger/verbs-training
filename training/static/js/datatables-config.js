/*
#######################
#  DataTables config  #
#######################
*/

// Formatting function for childrows
function format(d) {
    // `d` is the original data object for the row
    let subrow = "";
    if (d.info) {
        subrow += (
            "<tr>" +
                "<td class='childrow-first-col border-bottom-0'></td>" +
                "<td colspan='4'>" +
                    "<h6 class='fw-bold'>Info</h6>" +
                    d.info +
                "</td>" +
            "</tr>"
        );
    }
    if (d.examples) {
        subrow += (
            "<tr>" +
                "<td class='childrow-first-col'></td>" +
                "<td colspan='4'>" +
                    "<h6 class='fw-bold'>Examples</h6>" +
                    d.examples +
                "</td>" +
            "</tr>"
        );
    }
    return $(subrow).toArray()
}

var table = $("#custom-dt").DataTable({
    initComplete: function () {
        // display table, hidden by css #custom-dt display: none to avoid FOUC
        var api = this.api();
        api.columns.adjust();
        $("#custom-dt").show();
        // add flex and spaces to datatable wrapper
        $("#custom-dt_wrapper").addClass("d-flex flex-column gap-4 mt-4");
        // remove btn-group class to prevent broder radius top-left and bottom-left to be cleared
        $(".dt-buttons").removeClass("btn-group").addClass("d-flex flex-column flex-md-row gap-4");
        // searchPanes keyboard navigation
        $("#filter").on("keydown", function(event) {
            if(event.keyCode == 13) {
                if($("#layout-top-start .dt-buttons .dropdown-menu").length) {
                    // trigger a click on background if the dropdown menu is displayed to close it
                    $("#layout-top-start .dt-button-background").click();
                } else {
                    $(this).click();
                }
                $(this).focus();
                event.preventDefault();
            }
        });
        // keyboard thead th navigation
        $(".dt-scroll-head thead tr th:not(:first-child)").attr("tabindex", "0");
        // disable colors and filter buttons if user is not authenticated
        $("#colors, #filter").prop("disabled", !(isAuthenticated === "true"));
    },
    scrollX: true,
    scrollCollapse: true,
    paging: false,
    info: false,
    tabIndex: -1,
    language: {
        searchPanes: {
            collapse: { 0: "Filter Options", _: "Filter Options (%d)" }
        },
        entries: {
            _: "verbs",
            1: "verb"
        },
        info: "Showing _TOTAL_ of _MAX_ _ENTRIES-MAX_",
        infoFiltered: "",
        infoEmpty: "No verbs to show"
    },
    layout: {
        top2: {
            id: "layout-top2",
            features: {
                buttons: [
                    {
                        extend: "pdf",
                        text: "Export to PDF",
                        title: "Irregular Verbs",
                        filename: "irregular_verbs",
                        attr: {
                            id: "pdf",
                            tabindex: "0",
                            "aria-label": "Export to pdf",
                        },
                        exportOptions: {
                            orthogonal: "pdf",
                            columns: [1, 2, 3, 4, 7],
                            // stripNewlines: false,
                            format: {
                                header: function(data, columnIdx) {
                                    if (columnIdx == 4) {
                                        return "Examples";
                                    } else {
                                        return data;
                                    }
                                },
                            }
                        },
                        customize: function(doc) {
                            doc.defaultStyle.alignment = "center";
                            // doc.content[1].table.widths = ["auto", "auto", "auto", "auto", "*"]
                        }
                    },
                    {
                        extend: "print",
                        text: "Print the table",
                        title: "<h1 class='text-center pb-5'>Irregular Verbs</h1>",
                        autoPrint: false,
                        attr: {
                            id: "print",
                            tabindex: "0",
                            "aria-label": "Show a printable version of the table",
                        },
                        exportOptions: {
                            columns: [1, 2, 3, 4, 7],
                            stripHtml: false,
                            format: {
                                header: function(data, columnIdx) {
                                    if (columnIdx == 4) {
                                        return "Examples";
                                    } else {
                                        return data;
                                    }
                                },
                            },
                        },
                    },
                ],
            },
        },
        topStart: {
            // rowId and rowClass used for topStart and topEnd parent element
            rowId: "layout-top",
            rowClass: "row mt-2 justify-content-between gap-4",
            // id of topStart
            id: "layout-top-start",
            features: {
                buttons: [
                    {
                        text: "Enable colors",
                        attr: {
                            id: "colors",
                            class: "btn btn-light border",
                            tabindex: "0",
                            "data-bs-toggle": "button",
                            "arial-label": "Enable / Disable row colors"
                        },
                        action: function (e, dt, node, config) {
                            let tbody = $("#custom-dt tbody");
                            tbody.toggleClass("colored");
                            let isColored = tbody.hasClass("colored");
                            this.text(isColored ? "Disable colors" : "Enable colors");
                        },
                    },
                    {
                        extend: "searchPanes",
                        attr: {
                            id: "filter",
                            class: "btn btn-light border",
                            tabindex: "0",
                            "aria-label": "Open / Close search panes"
                        },
                        config: {
                            controls: false,
                            collapse: false,
                            columns: [5],
                            dtOpts: {
                                select: {
                                    style: "multi"
                                },
                            },
                        },
                    },
                ],
            }
        },
        topEnd: "search",
    },
    columnDefs: [
        {
            searchPanes: {
                className: "test-custom-class",
                header: "Verb status",
                options: [
                    {
                        label: "Successfull",
                        value: function (rowData, rowIdx) {
                            return rowData["is success"] === "True";
                        },
                        order: 1,
                    },
                    {
                        label: "Failed",
                        value: function (rowData, rowIdx) {
                            return rowData["is success"] === "False";
                        },
                        order: 2,
                    },
                    {
                        label: "Not done",
                        value: function (rowData, rowIdx) {
                            return rowData["is success"] === "None";
                        },
                        order: 3,
                    },
                ],
            },
            targets: [5],
        },
    ],
    columns: [
        {
            className: "dt-control dt-first-col",
            orderable: false,
            data: null,
            defaultContent: ""
        },
        {data: "infinitive"},
        {
            data: "simple past",
            render: function (data, type, row, meta) {
                if (type === "pdf") {
                    return data
                }
                return data.split(",").join("</br>");
            }
        },
        {
            data: "past participle",
            render: function (data, type, row, meta) {
                if (type === "pdf") {
                    return data
                }
                return data.split(",").join("</br>");
            }
        },
        {
            data: "translation",
            render: function (data, type, row, meta) {
                if (type === "pdf") {
                    return data
                }
                return data.split(",").join("</br>");
            }
        },
        {
            data: "is success",
            visible: false,
            orderable: false,
        },
        {
            data: "info",
            visible: false,
            orderable: false,
        },
        {
            data: "examples",
            visible: false,
            orderable: false,
        },
    ],
    order: [],
});

// Add event listener for opening and closing details
table.on("click", "tbody td.dt-control", function () {
    var tr = $(this).closest("tr");
    var row = table.row(tr);

    if (row.child.isShown()) {
        // This row is already open - close it
        row.child.hide();
        tr.removeClass("shown");
    }
    else {
        // Open this row
        row.child(format(row.data())).show();  // add child row on click
        tr.addClass("shown");
    }
});

// Change buttons action if user is not authenticated to redirect on the login page
if (isAuthenticated === "false") {
    table.buttons().action(function (e, dt, button, config) {
        location.href = loginUrl;
        return;
    })
}

// Add event listener to expand row when enter key is pressed
$(".dt-control").on("keypress", function(event){
    if(event.keyCode == 13) {
        $(this).click();
    }
});

// Toggle the active class on the button when clicked
$("#filter").on('click', function() {
    $(this).toggleClass('active');
    // Remove the active class when the searchPanes container is hidden
    $(document).on('click', function(event) {
        if (!$(event.target).closest('.dtsp-panes, #filter').length) {
            $('#filter').removeClass('active');
        }
    })
});

