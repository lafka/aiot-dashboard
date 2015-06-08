$(function() {
    var $box = $('#model');
    
    function initModelBox() {
        var token = $box.attr('data-token');

        $box.html('<div id="viewer-container" style="width: 100%; height: 100%;"></div>');
        
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
                
                // Hook into the SSE feed
/*                var source = new EventSource("{{ update_url }}");
                source.onmessage = function(event) {
                    var data = JSON.parse(event.data);

                    // Set color based on movement (red = movement, green = not movement)
                    var col = data.s_movement ? '#FF0000' : '#00FF00';

                    $('#viewer-container').viewer('color', col, data.room_key);
                    $('#viewer-container').viewer('show', data.room_key);
                };*/
            });
        }

    }
    
    initModelBox();
});