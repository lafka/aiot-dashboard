$(function() {
    var $box = $('#graphs');

    var time_ticks = [];

    String.prototype.lpad = function(padString, length) {
        var str = this;
        while (str.length < length) {
            str = padString + str;
        }
        return str;
    };

    var mode = -1; // 0 = kW, 1 = Deviations, 2 = Deviations per Room

    function setMode(new_mode) {
        mode = parseInt(new_mode, 10);

        var $button = $box.find('.buttons ul .btn').eq(mode);
        $box.find('.buttons ul .active').removeClass('active');
        $button.addClass('active');

        $box.find('.graph').hide();
        $box.find('.graph').each(function() {
            if(mode == parseInt($(this).attr('data-mode'), 10)) {
                $(this).show();
                $(this).trigger('plot');
            }
        });
    }

    function initGraphs() {
        $box.append('<div class="buttons"><ul></ul></div>');

        for(h = 0; h < 24; h+=2) {
            time_ticks.push([h, ("" + h).lpad("0", 2) + ":00"]);
        }

        initKwhGraph();
        initDeviationsTotalGraph();
        initDeviationsPerRoomGraph();
        initButtons();

        $box.data('updateFunc', function(rec) {
            if (rec.type !== 'graph') {
                return;
            }
            $box.find('.graph').each(function() {
                $(this).data('updateFunc')(rec);
            });
        });

        setMode(0);
    }

    function initButtons() {
        var $buttons = $box.find('.buttons');
        $box.find('.buttons ul').append('<li><button class="btn btn-default btn_kwm" data-mode="0"><i class="fa fa-bolt"></i> kW</button></li>');
        $box.find('.buttons ul').append('<li><button class="btn btn-default btn_deviations" data-mode="1"><i class="fa fa-exclamation-triangle"></i> Total Deviations</button></li>');
        $box.find('.buttons ul').append('<li><button class="btn btn-default btn_deviations_room" data-mode="2"><i class="fa fa-bar-chart"></i> Room Deviations</button></li>');

        $buttons.find('.btn').css('margin-left', '-' + $buttons.width() + 'px');
        setTimeout(function() {
            var i = 0;
            $buttons.find('.btn').each(function() {
                var $this = $(this);

                setTimeout(function() {
                    $this.animate({
                        'margin-left': '0px'
                    }, 200);
                }, i * 200);
                i++;
            });
        }, 1000);

        $buttons.find('.btn').click(function() {
            var mode = $(this).attr('data-mode');
            if(mode !== undefined) {
                setMode(mode);
            }
        });
    }

    function initKwhGraph() {
        $box.append('<div class="kwm_graph graph" data-mode="0" style="width: 100%; height: 85%; margin-top: 40px; display: none;"></div>');
        var $kwm_graph = $box.find(".kwm_graph:first");

        $kwm_graph.data('updateFunc', function(rec) {
            var graph_data = [];
            $(rec.circuits).each(function(ci) {
                var circuit = rec.circuits[ci];
                var vals = [];
                $(circuit.kwh).each(function(i) {
                    vals.push([circuit.kwm[i][0], circuit.kwm[i][1] * 60]);
                });

                graph_data.push({
                    label: circuit.name,
                    data: vals
                });
            });
            graph_data.push({
                label: 'Max',
                data: [[0, rec.max_month], [24, rec.max_month]],
                stack: false,
                lines: {
                    fill: false
                }
            });

            $kwm_graph.unbind('plot');
            $kwm_graph.bind('plot', function() {
                $.plot($kwm_graph, graph_data, {
                    series: {
                        stack: true,
                        lines: {
                            show: true,
                            fill: true,
                            steps: true
                        }
                    },
                    xaxis: {
                        ticks: time_ticks
                    },
                    yaxis: {
                        tickFormatter: function formatter(val, axis) {
                            return "" + val + " kWh";
                        }
                    },
                    legend: {
                        show: true,
                        backgroundOpacity: 0.5
                    }
                });
            });
            $kwm_graph.trigger('plot');
        });
    }

    function initDeviationsTotalGraph() {
        $box.append('<div class="deviations_graph graph" data-mode="1" style="width: 100%; height: 85%; margin-top: 40px; display: none;"></div>');
        var $dev_graph = $box.find(".deviations_graph:first");

        $dev_graph.data('updateFunc', function(rec) {
            var graph_data = [];

            graph_data.push({
                label: 'total',
                data: rec.deviations.total
            });

            $dev_graph.unbind('plot');
            $dev_graph.bind('plot', function() {
                $.plot($dev_graph, graph_data, {
                    series: {
                        stack: true,
                        lines: {
                            show: true,
                            fill: true,
                            steps: true
                        }
                    },
                    xaxis: {
                        ticks: time_ticks
                    },
                    legend: {
                        show: false
                    }
                });
            });
            $dev_graph.trigger('plot');
        });
    }

    function initDeviationsPerRoomGraph() {
        $box.append('<div class="dpr_graph graph" data-mode="2" style="width: 100%; height: 85%; margin-top: 40px; display: none;"></div>');
        var $dpr_graph = $box.find(".dpr_graph:first");

        $dpr_graph.data('updateFunc', function(rec) {
            var graph_data = [];

            graph_data.push({
                label: 'rooms',
                data: rec.deviations.rooms
            });

            $dpr_graph.unbind('plot');
            $dpr_graph.bind('plot', function() {
                $.plot($dpr_graph, graph_data, {
                    series: {
                        stack: false,
                        lines: {
                            show: false
                        },
                        bars: {
                            show: true,
                            barWidth: 0.6,
                            align: "center"
                        }
                    },
                    xaxis: {
                        mode: "categories",
                        tickLength: 0
                    },
                    yaxis: {
                    },
                    legend: {
                        show: false
                    }
                });
            });
            $dpr_graph.trigger('plot');
        });
    }

    initGraphs();
});
