var aiot = aiot || {};
aiot.rooms = aiot.rooms || {};
aiot.rooms.overview = {};

(function(ns) {

function on_event(event) {
    $('#data_list tbody').html(event.overview_trs_html);
}

ns.on_event = on_event;

})(aiot.rooms.overview);
