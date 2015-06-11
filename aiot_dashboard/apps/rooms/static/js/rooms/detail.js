var aiot = aiot || {};
aiot.room = aiot.room || {};
aiot.room.detail = {};

(function(ns) {

var flot_timeseries_by_type = {};

window.fts = flot_timeseries_by_type; // debug

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
    $.each(types, function(k, type) {
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

function add_events(events) {
    $.each(events, function(k, event) {
        var timeseries = get_timeseries_by_type(event.type);

        if (timeseries.data.length) {
            console.log('first', timeseries.data[0]);
            console.log('last', timeseries.data[timeseries.data.length -1]);
        }
        timeseries.data.push([event.epoch, event.value]);
        console.log('new last', timeseries.data[timeseries.data.length -1]);
    });

    var types = ['lux', 'moist', 'co2', 'db', 'temp'];
    plot_graph(types);
}

function initialize_room_event_stream(room_key, last_datetime) {
    var url = Urls.room_detail_events(room_key);
    url += '?last_datetime=' + encodeURIComponent(last_datetime);

    var source = new EventSource(url);

    source.onmessage = function(event) {
        var data = JSON.parse(event.data);
        add_events(data);
    };
}

ns.initialize = function(config) {
    add_events(config.events);

    if (config.stream) {
        initialize_room_event_stream(config.room_key, config.last_datetime);
    }
};

})(aiot.room.detail);
