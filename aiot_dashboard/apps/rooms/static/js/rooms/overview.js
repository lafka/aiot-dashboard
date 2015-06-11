var aiot = aiot || {};
aiot.rooms = aiot.room || {};
aiot.rooms.overview = {};

(function(ns) {

function on_event(room_states) {
    var $list = $('#data_list');

    $list.find('.record').remove();

    $.each(room_states, function(k, room_state) {
        rowHtml = "<tr class='record'>";

        $list.find('th').each(function() {
            col = $(this).attr('data-col');
            if (col == 'name') {
                rowHtml += "<td><a href=\"" + room_state.url + "\">" + room_state[col] + "</a></td>";
            }
            else if (col == 'movement') {
                var val = room_state[col]? 'Y' : 'N';
                rowHtml += "<td>" + val + "</td>";
            }
            else {
                rowHtml += "<td>" + room_state[col] + "</td>";
            }
        });
        rowHtml += "</tr>";
        $list.append(rowHtml);
    });
}

ns.on_event = on_event;

})(aiot.rooms.overview);
