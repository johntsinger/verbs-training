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

// dataTables configuration
var table = $("#custom-dt").DataTable({
    initComplete: function () {
        // display table, hidden by css #custom-dt display: none to avoid FOUC
        var api = this.api();
        api.columns.adjust();
        $("#custom-dt").show();
        // Remove conflicting button classes and add desired class
        // $('#export .dt-buttons button').removeClass('btn-secondary').addClass('btn btn-outline-secondary');
        // remove btn-group class to prevent broder radius top-left and bottom-left to be cleared
        $(".dt-buttons").removeClass("btn-group").addClass("d-flex flex-column flex-md-row gap-3");
        // searchPanes keyboard navigation
        $("#custom-dt_wrapper button").attr("tabindex", "0");
        $("#sp-layout .dt-buttons button").keydown(function(event) {
            if(event.keyCode == 13) {
                if($("#sp-layout .dt-buttons .dropdown-menu").length === 1) {
                    $("#sp-layout .dt-button-background").click();
                } else{
                    $(this).click();
                }
                $(this).focus();
                event.preventDefault();
            }
        }).removeClass('btn-secondary').addClass('btn btn-outline-secondary');
        $(".dt-scroll-head thead tr th:not(:first-child)").attr("tabindex", "0");
        // add space between searchPanes div and search on small screen
        $("#searchpanes-search").addClass("gap-3");
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
    // display position
    layout: {
        top2: {
            id: "export",
            features: {
                buttons: [
                    {
                        extend: "pdf",
                        text: "Export to PDF",
                        title: "Irregular Verbs",
                        filename: "irregular_verbs",
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
                                }
                            }
                        }
                    }
                ]
            }
        },
        topStart: {
            rowId: "searchpanes-search",
            id: "sp-layout",
            features: {
                buttons: [
                    {
                        extend: "searchPanes",
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
    // column
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
    // creates buttons
    // buttons: {
    //     dom: {
    //         // common classes for each button
    //         button: {
    //             className: "btn mb-3 mb-md-0",
    //         },
    //     },
    //     buttons: [
    //         {
    //             text: "Disable colors",
    //             attr: {
    //                 id: "colors",
    //                 "arial-label": "Enable / Disable row colors"
    //             },
    //             className: "btn-outline-primary colors active",
    //         },
    //         {
    //             text: function (dt, button, config) {
    //                 return "success (" + dt.rows(".success").count() + ")";
    //             },
    //             attr: {
    //                 id: "success",
    //                 "arial-label": "Switch success filter"
    //             },
    //             className: "btn-outline-success filter",
    //         },
    //         {
    //             text: function (dt, button, config) {
    //                 return "unsuccess (" + dt.rows(".unsuccess").count() + ")";
    //             },
    //             attr: {
    //                 id: "unsuccess",
    //                 "arial-label": "Switch unsuccess filter"
    //             },
    //             className: "btn-outline-danger filter",
    //         },
    //         {
    //             text: function (dt, button, config) {
    //                 return "not-tested (" + dt.rows(".not-tested").count() + ")";
    //             },
    //             attr: {
    //                 id: "not-tested",
    //                 "arial-label": "Switch not tested filter"
    //             },
    //             className: "btn-outline-secondary filter",
    //         },
    //     ],
    // }
});

// // Define buttons actions
// table.buttons().action(function (e, dt, button, config) {
//     // if user not authenticated redirect to login page
//     if (!(isAuthenticated === "true")) {
//         location.href = loginUrl;
//         return;
//     }

//     // button colors
//     if (button.attr("id") === "colors") {
//         // button.toggleClass("active")
//         $("tbody.colored").toggleClass("active");
//         if ($("tbody.colored").hasClass("active")) {
//             button.text("Disable colors")
//             button.addClass("active")
//         } else {
//             button.text("Enable colors")
//             button.removeClass("active")
//         }
//     //buttons filter
//     } else {
//         // saves the state of the button"s active class
//         let isActive = button.hasClass("active");
//         // removes active class for each buttons in dt and reset filter
//         dt.buttons(".filter").nodes().removeClass("active"); // $.fn.dataTable.ext.search.pop()
//         $(dt).dataTableExt.search.pop();

//         // adds class active to clicked button if it was not active and display matching rows
//         if (!(isActive)) {
//             button.addClass("active");
//             // $.fn.dataTable.ext.search.push( // same as next
//             $(dt).dataTableExt.search.push(
//                 function(settings, data, dataIndex) {
//                     return $(dt.row(dataIndex).node()).hasClass(button.attr("id"));
//                 }
//             );
//         }
//     }
//     dt.draw();
// })

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

// Add event listener to expand row when enter key is pressed
$(".dt-control").keypress(function(event){
    if(event.keyCode == 13) {
        $(this).click();
    }
});