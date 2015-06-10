var aiot = aiot || {};
aiot.room = aiot.room || {};
aiot.room.detail = {};

(function(ns) {

ns.initialize_room_event_stream = function(room_key, last_datetime) {
    var url = Urls.room_detail_events(room_key);
    url += '?last_datetime=' + encodeURIComponent(last_datetime);

    var source = new EventSource(url);

    source.onmessage = function(event) {
        var data = JSON.parse(event.data);
        console.log(data);

        $.each(data, function(k, v) {
            console.log(k, v);
        });
    };
};

ns.initialize = function(config) {
    //produce_flot_thing(config.events);

    if (config.stream) {
        ns.initialize_room_event_stream(config.room_key, config.last_datetime);
    }
};

})(aiot.room.detail);
