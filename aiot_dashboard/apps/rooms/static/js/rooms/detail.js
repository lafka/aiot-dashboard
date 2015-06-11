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

function plot_graph(types) {
    var flot_timeseries = [];
    var yaxis = 1;
    $.each(types, function(i, type) {
        if (flot_timeseries_by_type[type]) {
            var timeseries = get_timeseries_by_type(type);
            timeseries.yaxis = yaxis++;
            flot_timeseries.push(timeseries);
        }
    });

    $.plot($('#graph'), flot_timeseries, {
        xaxis: {
            mode: 'time'
        }
    });
}

function on_event(event) {
    var timeseries = get_timeseries_by_type(event.type);
    timeseries.data.push([event.epoch, event.value]);
}

function on_after_events() {
    var types = ['lux', 'moist', 'co2', 'db', 'temp'];
    plot_graph(types);
}

ns.on_after_events = on_after_events;
ns.on_event = on_event;

})(aiot.rooms.detail);
