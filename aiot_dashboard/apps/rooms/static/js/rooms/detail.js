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

    return timeseries;
}

function plot_graph() {
    var types = get_type_dict();
    var flot_timeseries = [];
    var yaxes = [];

    $.each(types, function(type, type_obj) {
        if (!flot_timeseries_by_type[type]) {
            return;
        }

        yaxes.push({
            tickFormatter: function (value) {
                return value + type_obj.unit_suffix;
            },
            color: type_obj.color
        });

        var timeseries = get_timeseries_by_type(type);
        timeseries.yaxis = yaxes.length;
        timeseries.color = type_obj.color;

        flot_timeseries.push(timeseries);
    });

    $.plot($('#graph'), flot_timeseries, {
        xaxis: {
            mode: 'time'
        },
        yaxis: {
            show: false
        },
        zoom: {
            interactive: true
        },
        pan: {
            interactive: true
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
            color: '#edc240'
        },
        'humidity': {
            unit_suffix: ' %',
            color: '#afd8f8'
        },
        'co2': {
            unit_suffix: ' ppm',
            color: '#cb4b4b'
        },
        'noise': {
            unit_suffix: ' dB',
            color: '#4da74d'
        },
        'temperature': {
            unit_suffix: ' \u2103',
            color: '#9440ed'
        }
    };
}

function on_after_events(events) {
    if (events.length) {
        plot_graph();
    }
}

ns.on_after_events = on_after_events;
ns.on_event = on_event;
ns.on_open = on_open;
ns.plot_graph = plot_graph;

})(aiot.rooms.detail);
