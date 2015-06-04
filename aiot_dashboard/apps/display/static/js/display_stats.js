$(function() {
	var $box = $('#stats');
	var $box_list = null;
	
	function getOrCreateRoom(key) {
		if($box_list.find('li[data-rec-id=' + key + ']').length == 0) {
			$box_list.append('<li data-rec-id="' + key + '"><div class="room_name"></div></li>');
		}
		return $box_list.find('li[data-rec-id=' + key + ']:first');
	}
	
	function updateRoom(room, data) {
		console.log(data);
		room.find('.room_name').html(data.name);
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