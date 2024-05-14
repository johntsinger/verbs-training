// Formatting function for row details - modify as you need
function format(d) {
    // `d` is the original data object for the row
    let htmlClass = '';
    if (d['is success'] === 'True') {
        htmlClass = 'success';
    } else if (d['is success'] === 'False') {
        htmlClass = 'unsuccess';
    } else {
        htmlClass = 'not-done';
    }
    return $(
        '<tr class=' + htmlClass + '>' +
            '<td>' +
            '' +
            '</td>'+
            '<td>' +
            d['infinitive'] +
            '</td>' +
            '<td>' +
            d['simple past'].split('/').join('</br>') +
            '</td>' +
            '<td>' +
            d['past participle'].split('/').join('</br>') +
            '</td>' +
            '<td>' +
            d['translation'].split('/').join('</br>') +
            '</td>' +
        '</tr>'
    ).toArray();
}

// dataTables configuration
var table = $('#custom-dt').DataTable({
    initComplete: function () {
        // display table, hidden by css #custom-dt display: none to avoid FOUC
        var api = this.api();
        $('#custom-dt').show();
        api.columns.adjust();
    },
    autoWidth: false,
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
        {width: '5%', targets: 0}
    ],
    columns: [
        {
            className: 'dt-control',
            orderable: false,
            data: null,
            defaultContent: ''
        },
        {data: 'infinitive'},
        {
            data: 'simple past',
            render: function (data, type, row, meta) {
                return data.split('/').join('</br>');
            }
        },
        {
            data: 'past participle',
            render: function (data, type, row, meta) {
                return data.split('/').join('</br>');
            }
        },
        {
            data: 'translation',
            render: function (data, type, row, meta) {
                return data.split('/').join('</br>');
            }
        },
        {
            data: 'is success',
            visible: false,
            orderable: false,
        }
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
                    id: 'success'
                },
                className: 'btn-outline-success',
            },
            {
                text: function (dt, button, config) {
                    return 'unsuccess (' + dt.rows('.unsuccess').count() + ')';
                },
                attr: {
                    id: 'unsuccess'
                },
                className: 'btn-outline-danger',
            },
            {
                text: function (dt, button, config) {
                    return 'not-tested (' + dt.rows('.not-tested').count() + ')';
                },
                attr: {
                    id: 'not-tested'
                },
                className: 'btn-outline-primary',
            },
        ],
    }
});

table.buttons().action(function (e, dt, button, config) {
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
        row.child(format(row.data())).show();
        tr.addClass('shown');
    }
});

// Add event listener to expand row when enter key is pressed
$('.dt-control').keypress(function(event){
    if(event.keyCode == 13){
        $(this).click();
    }
});