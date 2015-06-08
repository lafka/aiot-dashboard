$(function() {
    var $box = $('#model');
    var $legend = null;
    var mode = 0; // 0 = Occupied, 1 = Co2, 2 = Temp
    
    function setMode(new_mode) {
    	mode = new_mode;
    	
    	if(mode == 0) {
    		$legend.html('<ul><li><div class="color_block" style="background-color: #f00;"></div> opptatt</li><li><div class="color_block" style="background-color: #0f0;"></div> tom</li></ul>');
    	}
    }
    
    function initModelBox() {
        var token = $box.attr('data-token');

        $box.html('<div class="legend"></div><div id="viewer-container" style="width: 100%; height: 100%;"></div>');
        $legend = $box.find('.legend:first')
        
        // Load the Viewer API
        bimsync.load();
        bimsync.setOnLoadCallback(createViewer);

        // Callback that loads a viewer access token URL
        function createViewer() {
            var $viewer = $('#viewer-container');
            $viewer.viewer('loadurl', 'https://api.bimsync.com/1.0/viewer/access?token=' + token);

            // Make model translucent, otherwise we can't actually see much
            $viewer.bind('viewer.load', function() {
                $viewer.viewer('translucentall');
                
                $viewer.viewer('viewpoint', {
                    direction: {
                        x: -0.577,
                        y: 0.577,
                        z: -0.577
                    },
                    location: {
                        x: 82.85,
                        y: -106.40,
                        z: 110.775,
                    },
                    up: {
                        x: 0,
                        y: 0,
                        z: 1
                    },
                    fov: 50,
                    type: 'perspective'
                });

                setMode(0);
                
                $box.data('updateFunc', function(data) {
                    $.each(data, function(k, v) {
                        var room_key = k;

                        if(mode == 0) {
	                        // Set color based on occupied (red = movement, green = not movement)
	                        var col = v.occupied ? '#FF0000' : '#00FF00';
	
	                        $('#viewer-container').viewer('color', col, room_key);
	                        $('#viewer-container').viewer('show', room_key);
                        }
                    });
                });
            });
        }

    }
    
    initModelBox();
});