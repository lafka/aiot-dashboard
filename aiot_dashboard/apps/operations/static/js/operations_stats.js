$(function() {
    var $box = $('#stats');
    var $box_list = null;

    function getOrCreateRoom(key) {
        if($box_list.find('li[data-rec-id=' + key + ']').length === 0) {
            var boxHtml = '<li data-rec-id="' + key + '">';
            boxHtml += '<div class="room_name"></div>';
            boxHtml += '<div class="deviations">';
            boxHtml += '<div class="temperature"><span></span></div>';
            boxHtml += '<div class="co2"><span></span></div>';
            boxHtml += '<div class="humidity"><span></span></div>';
            boxHtml += '<div class="quality_index"><i class="fa fa-exclamation-triangle"></i><span></span></div>';
            boxHtml += '<div class="power_consumption"><i class="fa fa-bolt"></i><span></span></div>';
            boxHtml += '</div>';
            boxHtml += '</li>';
            $box_list.append(boxHtml);
        }
        return $box_list.find('li[data-rec-id=' + key + ']:first');
    }

    function updateRoom(room, data) {
        room.find('.room_name').html(data.name);
        room.find('.quality_index span').html(data.quality_index);
        room.find('.power_consumption span').html("<nobr>" + data.power_consumption.toFixed(0) + " W</nobr>");
        room.attr('data-quality-index', data.quality_index);
        $.each(data.deviations, function(k, v) {
            room.find('.' + k).find('span').html(v);
        });
    }

    function initStatsBox() {
        $box.append('<h2>Rooms</h2><ul></ul>');
        $box_list = $box.find('ul:first');

        $box.data('updateFunc', function(rec) {
            if(rec.type == 'room') {
                var room_key = rec.key;
                var room = getOrCreateRoom(room_key);

                updateRoom(room, rec);
            }

            // Sort
            $box_list_li = $box_list.children('li');
            $box_list_li.sort(function(a,b){
                var an = a.getAttribute('data-quality-index'),
                    bn = b.getAttribute('data-quality-index');

                if(an < bn) {
                    return 1;
                }
                if(an > bn) {
                    return -1;
                }
                return 0;
            });

            $box_list_li.detach().appendTo($box_list);
        });
    }

    initStatsBox();
});
