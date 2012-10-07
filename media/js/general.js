(function() {

    try {
        Typekit.load();
    } catch(e) {
    }

    var remembered = localStorage['visible_bugs'];
    if (remembered) {
        _.each(JSON.parse(remembered), function(v, k) {
            $('input[name=visible_bugs][value=' + v + ']').attr('checked', true);
        });
        refresh();
    } else {
        localStorage['visible_bugs'] = JSON.stringify(['1', '2', '3', '4', '5']);
        refresh();
    }

    $('input[name=visible_bugs]').on('change', function(e) {
        var $this = $(this),
            vals = _.map($('input[name=visible_bugs]:checked'), function(v) { return $(v).val(); });
        localStorage['visible_bugs'] = JSON.stringify(vals);
        refresh();
    }).trigger('change');

    function refresh() {
        var vals = _.map($('input[name=visible_bugs]:checked'), function(v) { return $(v).val(); });
        if (vals.indexOf('1') == -1) {
            $('.bug[data-status="NEW"], .bug[data-status="REOPENED"]').hide();
        } else {
            $('.bug[data-status="NEW"], .bug[data-status="REOPENED"]').show();
        }
        if (vals.indexOf('2') == -1) {
            $('.bug[data-status="RESOLVED"]:not([data-resolution="FIXED"])').hide();
        } else {
            $('.bug[data-status="RESOLVED"]:not([data-resolution="FIXED"])').show();
        }
        if (vals.indexOf('3') == -1) {
            $('.bug[data-resolution="FIXED"]').hide();
        } else {
            $('.bug[data-resolution="FIXED"]').show();
        }
        if (vals.indexOf('4') == -1) {
            //$('.bug[data-status="RESOLVED"][data-resolution="FIXED"]').hide();
        } else {
            $('.bug[data-status="RESOLVED"][data-resolution="FIXED"]').show();
        }
        if (vals.indexOf('5') == -1) {
            //$('.bug[data-status="VERIFIED"]').hide();
        } else {
            $('.bug[data-status="VERIFIED"]').show();
        }
    }

})();
