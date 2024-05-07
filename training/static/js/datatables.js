function buttonAction (e, dt, button, config) {
    // saves the state of the button's active class
    var isActive = button.hasClass('active')
    // removes active class for each buttons in dt and reset filter
    dt.buttons().nodes().removeClass('active')
    $(dt).dataTableExt.search.pop()

    /*
    dt.buttons().each(function (value, index) {
        $(value.node).removeClass('active')
        // $.fn.dataTable.ext.search.pop() // same as next
        $(dt).dataTableExt.search.pop()
    })
    */
    
    // adds class active to clicked button if it was not active and display matching rows
    if (!(isActive)) {
        button.addClass('active');
        // $.fn.dataTable.ext.search.push( // same as next
        $(dt).dataTableExt.search.push(
            function(settings, data, dataIndex) {
                if (button.attr('id') === 'not-done') {
                    return !$(dt.row(dataIndex).node()).hasClass('unsuccess') && !$(dt.row(dataIndex).node()).hasClass('success');
                }
                return $(dt.row(dataIndex).node()).hasClass(button.attr('id'));
            }
        );
    };
    dt.draw()
}

// dataTables configuration
var table = $('#custom-dt').DataTable({
    scrollY: '40em',
    // scroll bar
    scrollX: true,
    scrollCollapse: true,
    scroller: {
        rowHeight: 40
    },
    // pagination
    paging: false,
    // search bar
    bFilter: true,
    // info
    bInfo: false,
    // column 
    columnDefs: [
        { width: '30%', targets: -1 },
        { width: '22%', targets: '_all' }
    ],
    /*
    language: {
        zeroRecords: 'Aucune donnée à afficher',
        search: 'Rechercher : ',
    },
    */
    // display position
    layout: {
        topStart: 'buttons',
        topEnd: 'search',
        bottomStart: 'info'
    },
    // creates buttons
    buttons: {
        dom: {
            /*
            container: {
                className: 'btn-group flex-wrap mt-3 mt-md-0',
            },
            */
            // common classes for each button
            button: {
                className: 'btn switcher mb-3 mb-md-0',
            }
        },
        buttons: [
            {
                text: 'success',
                attr: {
                    id: 'success'
                },
                className: 'btn-outline-success',
                action: function (e, dt, button, config) {
                    buttonAction(e, dt, button, config)
                }
            },
            {
                text: 'unsuccess',
                attr: {
                    id: 'unsuccess'
                },
                className: 'btn-outline-danger',
                action: function (e, dt, button, config) {
                    buttonAction(e, dt, button, config)
                }
            },
            {
                text: 'not done',
                attr: {
                    id: 'not-done'
                },
                className: 'btn-outline-primary',
                action: function (e, dt, button, config) {
                    buttonAction(e, dt, button, config)
                }
            },
        ],
    }
});

DataTable.feature.register('info', function (settings, opts) {
    function createElementWithClass(elementName, className) {
        let element = document.createElement(elementName)
        element.setAttribute('class', className)
        return element
    }
    let container = createElementWithClass('div', 'mt-3');
    let p1 = createElementWithClass('p', 'd-inline-block me-3');
    p1.innerHTML = 'Tested: ' + $('.success, .unsuccess').length
    let p2 = createElementWithClass('p', 'd-inline-block me-3');
    p2.innerHTML = 'Successfull: ' + $('.success').length
    let p3 = createElementWithClass('p', 'd-inline-block me-3');
    p3.innerHTML = 'Not tested: ' + $('.not-done').length
    
    container.append(p1, p2, p3)
    return container;
});


$('#verb-count').text('(' + table.column(0).data().length + ' verbs)');

/*
// Functions that set action for each button of button-group
$('#success').on('click', function () {
    // Remove active class for the other buttons
    $('#unsuccess').removeClass('active')
    $('#not-done').removeClass('active')
    $.fn.dataTable.ext.search.pop()

    // Make the button switchable and add a filter function
    if ($(this).hasClass('active')) {
        $(this).removeClass('active');
        $.fn.dataTable.ext.search.pop()
    } else {
        $(this).addClass('active');
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                var table = $('#custom-dt').DataTable();
                return $(table.row(dataIndex).node()).hasClass('success');
            }
        );
    };
    // Display results
    var table = $('#custom-dt').DataTable();
    table.draw();
});

$('#unsuccess').on('click', function () {
    $('#success').removeClass('active')
    $('#not-done').removeClass('active')
    $.fn.dataTable.ext.search.pop()

    if ($(this).hasClass('active')) {
        $(this).removeClass('active');
        $.fn.dataTable.ext.search.pop()
    } else {
        $(this).addClass('active');
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                var table = $('#custom-dt').DataTable();
                return $(table.row(dataIndex).node()).hasClass('unsuccess');
            }
        );
    };
    var table = $('#custom-dt').DataTable();
    table.draw();
});


$('#not-done').on('click', function () {
    $('#success').removeClass('active')
    $('#unsuccess').removeClass('active')
    $.fn.dataTable.ext.search.pop()

    if ($(this).hasClass('active')) {
        $(this).removeClass('active');
        $.fn.dataTable.ext.search.pop()
    } else {
        $(this).addClass('active');
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                var table = $('#custom-dt').DataTable();
                return !$(table.row(dataIndex).node()).hasClass('unsuccess') && !$(table.row(dataIndex).node()).hasClass('success');
            }
        );
    };
    var table = $('#custom-dt').DataTable();
    table.draw();
});
*/