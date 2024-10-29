/*
#######################
#  DataTables config  #
#######################
*/

// Formatting function for childrows
function format(d) {
    // `d` is the original data object for the row
    let subrow = '';
    if (d.info) {
        subrow += (
            '<tr>' +
                '<td class="childrow-first-col border-top-0"></td>' +
                '<td colspan="4">' +
                    '<h6 class="fw-bold">Info</h6>' +
                    d.info +
                '</td>' +
            '</tr>'
        );
    }
    if (d.examples) {
        subrow += (
            '<tr>' +
                '<td class="childrow-first-col border-top-0"></td>' +
                '<td colspan="4">' +
                    '<h6 class="fw-bold">Examples</h6>' +
                    d.examples +
                '</td>' +
            '</tr>'
        );
    }
    return $(subrow).toArray()
}

// dataTables configuration
var table = $('#custom-dt').DataTable({
    initComplete: function () {
        // display table, hidden by css #custom-dt display: none to avoid FOUC
        var api = this.api();
        $('#custom-dt').show();
        api.columns.adjust();
    },
    // scroll bar
    scrollY: '40em',
    scrollX: true,
    scrollCollapse: true,
    // pagination
    paging: false,
    language: {
        entries: {
            _: 'verbs',
            1: 'verb'
        },
        info: 'Showing _TOTAL_ of _MAX_ _ENTRIES-MAX_',
        infoFiltered: '',
        infoEmpty: 'No verbs to show'
    },
    // column
    columnDefs: [
        {width: '4%', targets: 0},
        {width: '16%', targets: '_all'}
    ],
    columns: [
        {
            className: 'dt-control dt-first-col',
            orderable: false,
            data: null,
            defaultContent: ''
        },
        {data: 'infinitive'},
        {
            data: 'simple past',
            render: function (data, type, row, meta) {
                return data.split(',').join('</br>');
            }
        },
        {
            data: 'past participle',
            render: function (data, type, row, meta) {
                return data.split(',').join('</br>');
            }
        },
        {
            data: 'translation',
            render: function (data, type, row, meta) {
                return data.split(',').join('</br>');
            }
        },
        {
            data: 'is success',
            visible: false,
            orderable: false,
        },
        {
            data: 'info',
            visible: false,
            orderable: false,
        },
        {
            data: 'examples',
            visible: false,
            orderable: false,
        },
    ],
    order: [],
    // display position
    layout: {
        topStart: 'buttons',
        topEnd: 'search',
        bottomStart: 'info'
    },
    // creates buttons
    buttons: {
        dom: {
            // common classes for each button
            button: {
                className: 'btn mb-3 mb-md-0',
            },
        },
        buttons: [
            {
                text: function (dt, button, config) {
                    return 'success (' + dt.rows('.success').count() + ')';
                },
                attr: {
                    id: 'success',
                    'arial-label': 'Switch success filter'
                },
                className: 'btn-outline-success',
            },
            {
                text: function (dt, button, config) {
                    return 'unsuccess (' + dt.rows('.unsuccess').count() + ')';
                },
                attr: {
                    id: 'unsuccess',
                    'arial-label': 'Switch unsuccess filter'
                },
                className: 'btn-outline-danger',
            },
            {
                text: function (dt, button, config) {
                    return 'not-tested (' + dt.rows('.not-tested').count() + ')';
                },
                attr: {
                    id: 'not-tested',
                    'arial-label': 'Switch not tested filter'
                },
                className: 'btn-outline-secondary',
            },
        ],
    }
});

// Define buttons actions
table.buttons().action(function (e, dt, button, config) {
    // if user not authenticated redirect to login page
    if (!(isAuthenticated === 'true')) {
        location.href = loginUrl;
        return;
    }

    // saves the state of the button's active class
    let isActive = button.hasClass('active');
    // removes active class for each buttons in dt and reset filter
    dt.buttons().nodes().removeClass('active'); // $.fn.dataTable.ext.search.pop()
    $(dt).dataTableExt.search.pop();
    
    // adds class active to clicked button if it was not active and display matching rows
    if (!(isActive)) {
        button.addClass('active');
        // $.fn.dataTable.ext.search.push( // same as next
        $(dt).dataTableExt.search.push(
            function(settings, data, dataIndex) {
                return $(dt.row(dataIndex).node()).hasClass(button.attr('id'));
            }
        );
    }
    dt.draw();
})


/*
// Open all child rows
table.rows().every(function () {
    this.child(format(this.data())).show();
    $(this.node()).addClass('shown');
});
*/

/*
// Add all child rows on load
table.rows().every(function () {
    this.child(format(this.data()))
});
*/

// Add event listener for opening and closing details
table.on('click', 'tbody td.dt-control', function () {
    var tr = $(this).closest('tr');
    var row = table.row(tr);
 
    if (row.child.isShown()) {
        // This row is already open - close it
        row.child.hide();
        tr.removeClass('shown');
    }
    else {
        // Open this row
        row.child(format(row.data())).show();  // add child row on click
        tr.addClass('shown');
    }
});

// Add event listener to expand row when enter key is pressed
$('.dt-control').keypress(function(event){
    if(event.keyCode == 13) {
        $(this).click();
    }
});