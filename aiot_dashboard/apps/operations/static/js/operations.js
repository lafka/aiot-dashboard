$(function() {
    var $operations = $('#operations');
    var box_width = 0;
    var box_height = 0;
    var z_index = 100;
    var max_z_index = 200;
    var focus_offset = 100;
    var $focused_box = null;

    function calcSizes() {
        // Get the operations panel as big as we can
        var height = $(window).height() - ($('#top').outerHeight(true) + $('footer').outerHeight(true)) - 30;
        var width = $operations.width();
        $operations.height(height);
        
        var box_count = $operations.find('.box').length;
        var rows = box_count / 2;
        box_width = width/2;
        box_height = height/rows;
        var i = 0;
        $operations.find('.box').each(function() {
            var $box = $(this);
            $box.width(box_width - 16);
            $box.height(box_height - 16);
            
            var top = Math.floor(i/2) * box_height;
            var left = (i % 2) * box_width;
            $box.css('top', '' + top + 'px');
            $box.css('left', '' + left + 'px');
            $box.data('top', top);
            $box.data('left', left);
            $box.css('font-size', '10px');
            
            $box.data('max_width', $operations.width() - focus_offset);
            $box.data('max_height', $operations.height() - focus_offset);
            
            i++;
        });
        $focused_box = null;
    }
    function initBoxHover() {
        $operations.find('.box').each(function() {
            var $box = $(this);

            var clickHandler = function(e) {
                if( e.target !== this ) 
                    return;

                if($focused_box === null || $box.attr('id') != $focused_box.attr('id')) {
                    unfocusOtherBoxes($box);
                    focusBox($box);
                } else {
                    $focused_box = null;
                    unfocusBox($box);
                }
            };
            
            $(this).prepend("<div class='focusbox'><i class='fa fa-chevron-circle-down'></i></div>");
            $(this).click(clickHandler);
            $(this).find('.focusbox i').click(clickHandler);
        });
    }
    function unfocusOtherBoxes($box) {
        $operations.find('.box').each(function() {
            if($box.attr('id') != $(this).attr('id'))
                unfocusBox($(this));
        });
    }
    function focusBox($box) {
        $focused_box = $box;
        $box.css('z-index', z_index);
        z_index += 1;
        if(z_index > max_z_index)
            z_index = 100;

        $box.animate({
            'width': $operations.width() - focus_offset,
            'height': $operations.height() - focus_offset,
            'top': $box.data('top') > 0 ? focus_offset : 0,
            'left': $box.data('left') > 0 ? focus_offset : 0,
            'font-size': 14
        }, 500, function() {
            $box.find('.graph').trigger('plot');
        });
        $box.find('h2').animate({
            'font-size': 22
        }, 500);
        $box.find('#viewer-container').each(function() {
            if($(this).data('original_top') === undefined)
                $(this).data('original_top', $(this).position().top);
            if($(this).data('original_left') === undefined)
                $(this).data('original_left', $(this).position().left);
            $(this).animate({
                'top': '0px',
                'left': '0px'
            }, 500);
        });
        $box.find('.focusbox i').removeClass('fa-chevron-circle-down');
        $box.find('.focusbox i').addClass('fa-chevron-circle-up');
        
        graphResizer($box);
    }
    function unfocusBox($box) {
        $box.animate({
            'width': box_width,
            'height': box_height,
            'top': $box.data('top'),
            'left': $box.data('left'),
            'font-size': 10
        }, 500, function() {
            $(this).css('z-index', '1');
            $box.find('.graph').trigger('plot');
        });
        $box.find('h2').animate({
            'font-size': 14
        }, 500);
        $box.find('#viewer-container').each(function() {
            $(this).animate({
                'top': '' + $(this).data('original_top') + 'px',
                'left': '' + $(this).data('original_left') + 'px'           
            }, 500);
        });
        $box.find('.focusbox i').removeClass('fa-chevron-circle-up');
        $box.find('.focusbox i').addClass('fa-chevron-circle-down');
        graphResizer($box);
    }
    function graphResizer($box) {
        function updatePlots() {
            $box.find('.graph').trigger('plot');
        }
        for(n = 0; n < 500; n += 100) {
            setTimeout(updatePlots, n);
        }
    }
    
    $(window).resize(calcSizes);
    
    calcSizes();
    initBoxHover();
});