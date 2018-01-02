<<<<<<< HEAD

function makeAutocomplete(sel) {
    sel.autocomplete('/examples/autocomplete-products/', {
        delay: 200,
        formatItem: function(row) {
            return row[1];
        }
    });
}

$(function() {
    makeAutocomplete($('.autocomplete-me'));
})
=======

function makeAutocomplete(sel) {
    sel.autocomplete('/examples/autocomplete-products/', {
        delay: 200,
        formatItem: function(row) {
            return row[1];
        }
    });
}

$(function() {
    makeAutocomplete($('.autocomplete-me'));
})
>>>>>>> github/master
