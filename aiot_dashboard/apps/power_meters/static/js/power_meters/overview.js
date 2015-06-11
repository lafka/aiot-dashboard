var aiot = aiot || {};
aiot.power_meters = aiot.power_meters || {};
aiot.power_meters.overview = {};

(function(ns) {

function on_event(power_meter_states) {
    var $list = $('#data_list');

    $list.find('.record').remove();

    $.each(power_meter_states, function(k, power_meter_state) {
        rowHtml = "<tr class='record'>";

        $list.find('th').each(function() {
            col = $(this).attr('data-col');
            if (col == 'name') {
                rowHtml += "<td><a href=\"" + power_meter_state.url + "\">" + power_meter_state[col] + "</a></td>";
            }
            else if (col == 'movement') {
                var val = power_meter_state[col]? 'Y' : 'N';
                rowHtml += "<td>" + val + "</td>";
            }
            else {
                rowHtml += "<td>" + power_meter_state[col] + "</td>";
            }
        });
        rowHtml += "</tr>";
        $list.append(rowHtml);
    });
}

ns.on_event = on_event;

})(aiot.power_meters.overview);
