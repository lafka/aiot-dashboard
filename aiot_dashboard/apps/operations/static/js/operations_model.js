$(function() {
    var $box = $('#model');
    var $legend = null;
    var mode = 0; // 0 = Occupied, 1 = Time usage, 2 = Quality

    function setMode(new_mode) {
        mode = parseInt(new_mode, 10);

        // Refresh immediately if we have stored records
        if($box.data('lastRoomRecs') !== undefined) {
            $.each($box.data('lastRoomRecs'), function(k, v) {
                $box.data('updateFunc')(v);
            });
        }

        var $button = $box.find('.buttons ul .btn').eq(mode);
        $box.find('.buttons ul .active').removeClass('active');
        $button.addClass('active');

        $legend.animate({
            'margin-left': '-300px'
        }, 500);
        setTimeout(function() {
            $legend.html('<div class="icon"></div><ul></ul>');
            if(mode === 0) { // Occupied
                $legend.find('.icon').html("<i class='fa fa-users'></i>");
                $legend.find('ul')
                    .append('<li><div class="color_block" style="background-color: #f00;"></div> available</li>')
                    .append('<li><div class="color_block" style="background-color: #0f0;"></div> occupied</li>');
            } else if(mode == 1) {
            } else {
                $legend.find('.icon').html("<i class='fa fa-wrench'></i>");
                $legend.find('ul')
                    .append('<li><div class="color_block" style="background-color: #0f0;"></div> < 30</li>')
                    .append('<li><div class="color_block" style="background-color: #ff0;"></div> 30 - 70</li>')
                    .append('<li><div class="color_block" style="background-color: #f00;"></div> > 70</li>');
            }

            $legend.animate({
                'margin-left': '10px'
            }, 500);
        }, 501);
    }

    function initButtons() {
        var $buttons = $box.find('.buttons');
        $box.find('.buttons ul').append('<li><button class="btn btn-default btn_kwm" data-mode="0"><i class="fa fa-users"></i> Availability</button></li>');
        $box.find('.buttons ul').append('<li><button class="btn btn-default btn_worst" data-mode="1"><i class="fa fa-arrow-down"></i> Worst 5</button></li>');
        $box.find('.buttons ul').append('<li><button class="btn btn-default btn_productivity" data-mode="2"><i class="fa fa-wrench"></i> Productivity</button></li>');
        $box.find('.buttons ul').append('<li><button class="btn btn-default btn_bim"><i class="fa fa-arrow-right"></i> Go to TotalBIM</button></li>');

        $buttons.find('.btn').css('margin-left', '-' + $buttons.width() + 'px');
        setTimeout(function() {
            var i = 0;
            $buttons.find('.btn').each(function() {
                var $this = $(this);

                setTimeout(function() {
                    $this.animate({
                        'margin-left': '0px'
                    }, 1000);
                }, i * 200);
                i++;
            });
        }, 1000);

        $buttons.find('.btn').click(function() {
            var mode = $(this).attr('data-mode');
            if(mode !== undefined) {
                setMode(mode);
            }
        });
    }

    function initModelBox() {
        var token = $box.attr('data-token');

        var max_width = $box.data('max_width');
        var max_height = $box.data('max_height');
        var w_offset = (max_width - $box.width())/2;
        var h_offset = (max_height - $box.height())/2;

        $box.append('<div class="spinner"><i class="fa fa-spin fa-spinner"></i></div><div class="buttons"><ul></ul></div><div class="legend"></div><div id="viewer-container" style="position: relative; width: ' + max_width + 'px; height: ' + max_height + 'px; margin: auto;"></div>');
        $legend = $box.find('.legend:first');
        $legend.css('margin-left', '-300px');

        // Load the Viewer API
        bimsync.load();
        bimsync.setOnLoadCallback(function() {
            var $viewer = $('#viewer-container');
            $viewer.css('top', '-' + h_offset + 'px');
            $viewer.css('left', '-' + w_offset + 'px');
            $viewer.viewer('loadurl', 'https://api.bimsync.com/1.0/viewer/access?token=' + token);

            // Make model translucent, otherwise we can't actually see much
            $viewer.bind('viewer.load', function() {
                $('#model .spinner').remove();

                // Buttons
                initButtons();

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
                        z: 110.775
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
                $box.data('updateFunc', function(rec) {
                    if(rec.type !== 'room') {
                        return;
                    }

                    var room_key = rec.key;

                    var lastRoomRecs = $box.data('lastRoomRecs');
                    if(lastRoomRecs === undefined) {
                        lastRoomRecs = {};
                    }

                    lastRoomRecs[room_key] = rec;
                    $box.data('lastRoomRecs', lastRoomRecs);

                    if(mode === 0) {
                        // Set color based on occupied (red = movement, green = not movement)
                        col = rec.occupied ? '#FF0000' : '#00FF00';

                        $('#viewer-container').viewer('color', col, room_key);
                        $('#viewer-container').viewer('show', room_key);
                    } else if(mode == 1) {
                        col = rec.worse_5 ? '#f00' : '#0f0';

                        $('#viewer-container').viewer('color', col, room_key);
                        if(rec.worse_5) {
                            $('#viewer-container').viewer('show', room_key);
                        }
                        else {
                            $('#viewer-container').viewer('hide', room_key);
                        }
                    } else {
                        p = parseInt(rec.productivity, 10);
                        col = p < 30 ? '#0f0' : '#ff0';
                        if(p > 70) {
                            col = '#f00';
                        }

                        $('#viewer-container').viewer('color', col, room_key);
                        $('#viewer-container').viewer('show', room_key);
                    }
                });
            });
        });
    }

    initModelBox();
});
