$(function() {
    var $box = $('#alert');
    var warning_shown = 0;
    var show_warning_for = 0;

    function showWarning(show_for) {
        if($('#gauge_warning').length > 0) {
            $('#gauge_warning').fadeIn('slow');
        } else {
            $box.prepend('<div id="gauge_warning"><h3><i class="fa fa-exclamation-triangle"></i> Warning</h3>Power consumption is close to setting a new maximum this hour</div>');
            $('#gauge_warning').fadeIn('slow');
        }
        $box.trigger('update_layout');

        warning_shown = new Date().getTime();
        if(show_for === undefined) {
            show_for = 2 * 5000;
        }
        show_warning_for = show_for;
    }

    function checkWarning() {
        if($('#gauge_warning:visible').length > 0 && warning_shown > 0 && show_warning_for > 0) {
            if(new Date().getTime() > warning_shown + show_warning_for) {
                $('#gauge_warning').fadeOut();
            }
        }
        setTimeout(function() {
            checkWarning();
        }, 1000);
    }
    checkWarning();

    function initMaxKwhGauge() {
        $box.append('<div class="buttons"><ul></li></div><div id="max_kwh_gauge" style="width: 100%; height: 90%;"></div>');
        var g = new JustGage({
            id: "max_kwh_gauge",
            value: 0,
            min: 0,
            max: 100,
            title: "Energiforbruk nå (kW)",
            minLabelMinFontSize: 16,
            maxLabelMinFontSize: 16,
            relativeGaugeSize: true
        });

        $box.data('updateFunc', function(rec) {
            if(rec.type !== 'current_kwh') {
                return;
            }

            g.refresh(rec.data.current, rec.data.max);
        });

        $box.bind('update_layout', function() {
            var w = $box.width();
            $('#gauge_warning').width(w / 2).css('left', '' + ((w - (w/2)) - 10) + 'px');
        });

        initButtons();
    }

    function initButtons() {
        var $buttons = $box.find('.buttons');
        $box.find('.buttons ul').append('<li><button class="btn btn-default btn_warning" data-mode="0"><i class="fa fa-exclamation-triangle"></i> Simulate Warning</button></li>');

        $buttons.find('.btn').css('margin-left', '-' + $buttons.width() + 'px');
        setTimeout(function() {
            var i = 0;
            $buttons.find('.btn').each(function() {
                var $this = $(this);

                setTimeout(function() {
                    $this.animate({
                        'margin-left': '0px'
                    }, 1000);
                }, i * 200);
                i++;
            });
        }, 1000);

        $buttons.find('.btn_warning').click(function() {
            showWarning(20000);
        });
    }

    initMaxKwhGauge();
});
