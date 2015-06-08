$(function() {
    var $box = $('#stats');
    var $box_list = null;
    
    function getOrCreateRoom(key) {
        if($box_list.find('li[data-rec-id=' + key + ']').length === 0) {
            var boxHtml = '<li data-rec-id="' + key + '"><div class="room_stat">';
            boxHtml += '<div class="room_name"></div>';
            
            boxHtml += '<div class="icons">';
            boxHtml += '<div class="occupied_icon off"><i class="fa fa-users"></i></div>';
            boxHtml += '<div class="productivity"><i class="fa fa-wrench"></i><span></span></div>';
            boxHtml += '<div class="deviations">';
            boxHtml += '<div class="temperature">0</div>';
            boxHtml += '<div class="co2">0</div>';
            boxHtml += '<div class="humidity">0</div>';
            boxHtml += '</div></div>';
            boxHtml += '</div></li>';
            $box_list.append(boxHtml);
        }
        return $box_list.find('li[data-rec-id=' + key + ']:first');
    }
    
    function updateRoom(room, data) {
        room.find('.room_name').html(data.name);
        
        if(data.occupied) {
            room.find('.occupied_icon').removeClass('off').addClass('on');
        } else {
            room.find('.occupied_icon').removeClass('on').addClass('off');
        }
        
        room.find('.productivity span').html(data.productivity);
        $.each(data.deviations, function(k, v) {
            room.find('.' + k).html(v);
        });
    }
    
    function initStatsBox() {
        $box.html('<ul></ul>');
        $box_list = $box.find('ul:first');
        
        var source = new EventSource(Urls.display_stats_update());
        source.onmessage = function(event) {
            var data = JSON.parse(event.data);

            $.each(data, function(k, v) {
                var room_key = k;
                var room = getOrCreateRoom(room_key);
                
                updateRoom(room, v);
            });
        };

    }
    
    initStatsBox();
});