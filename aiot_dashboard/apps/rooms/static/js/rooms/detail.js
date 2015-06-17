var aiot = aiot || {};
aiot.rooms = aiot.room || {};
aiot.rooms.detail = {};

(function(ns) {

var flot_timeseries_by_type = {};

function get_timeseries_by_type(type) {
    var timeseries = flot_timeseries_by_type[type];

    if (!timeseries) {
        timeseries = {
            label: type,
            data: []
        };

        flot_timeseries_by_type[type] = timeseries;
    }

    return $.extend({}, timeseries);
}

function plot_overview_graph() {
    var types = get_type_dict();
    var flot_timeseries = [];
    var yaxes = [];

    $.each(types, function(type, type_obj) {
        if (!flot_timeseries_by_type[type]) {
            return;
        }

        yaxes.push({
            color: type_obj.color
        });

        var timeseries = get_timeseries_by_type(type);
        timeseries.yaxis = yaxes.length;
        timeseries.color = type_obj.color;

        flot_timeseries.push(timeseries);
    });

    $graph_container = $('#graph');

    var plot = $graph_container.data('plot');

    if (plot) {
        plot.setData(flot_timeseries);
        plot.setupGrid();
        plot.draw();
    }
    else {
        $.plot($graph_container, flot_timeseries, {
            xaxis: {
                mode: 'time'
            },
            yaxis: {
                show: false
            }
        });
    }
}

function plot_detailed_graphs() {
    var types = get_type_dict();
    $.each(types, function(type, type_obj) {
        var sensor_timeseries = get_timeseries_by_type(type);
        sensor_timeseries.color = type_obj.color;

        $graph_container = $('#graph-' + type);
        var plot = $graph_container.data('plot');

        if (plot) {
            plot.setData([sensor_timeseries]);
            plot.setupGrid();
            plot.draw();
        }
        else {
            $.plot($graph_container, [sensor_timeseries], {
                xaxis: {
                    mode: 'time'
                },
                yaxis: {
                    show: true,
                    tickFormatter: function (value) {
                        if (type_obj.decimals) {
                            value = value.toFixed(2);
                        }
                        else {
                            value = '' + value;
                        }
                        return value + type_obj.unit_suffix;
                    }
                }
            });
        }
    });
}

function on_event(event) {
    var timeseries = get_timeseries_by_type(event.type);
    timeseries.data.push([event.epoch, event.value]);
}

function on_open() {
    /* Makes sure that we start with clean data, in case we get the same dataset again
     * (EventSource might do that if connection fails at some point, and then send the same
     *  request w/same URL, which would fetch the same dataset.)
     */
    flot_timeseries_by_type = {};
}

function get_type_dict() {
    return {
        'light': {
            unit_suffix: ' lux',
            color: '#edc240',
            decimals: false
        },
        'humidity': {
            unit_suffix: ' %',
            color: '#afd8f8',
            decimals: true
        },
        'co2': {
            unit_suffix: ' ppm',
            color: '#cb4b4b',
            decimals: false
        },
        'noise': {
            unit_suffix: ' dB',
            color: '#4da74d',
            decimals: true
        },
        'temperature': {
            unit_suffix: ' \u2103',
            color: '#9440ed',
            decimals: true
        }
    };
}

function on_after_events(events) {
    if (events.length) {
        plot_overview_graph();
        plot_detailed_graphs();
    }
}

ns.on_after_events = on_after_events;
ns.on_event = on_event;
ns.on_open = on_open;

})(aiot.rooms.detail);
