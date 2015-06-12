$(function() {
    var $operations = $('#operations');
    var box_width = 0;
    var box_height = 0;
    var z_index = 100;
    var max_z_index = 200;
    var focus_offset = 100;

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
            
            i++;
        });
    }
    function initBoxHover() {
        $operations.find('.box').each(function() {
            var $box = $(this);

            $(this).mouseenter(function() {
                focusBox($box);
            });
            $(this).mouseleave(function() {
                unfocusBox($box);
            });
        });
    }
    function focusBox($box) {
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
        }, 500);
        $box.find('h2').animate({
            'font-size': 22
        }, 500);
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
        });
        $box.find('h2').animate({
            'font-size': 14
        }, 500);
    }
    
    $(window).resize(calcSizes);
    
    calcSizes();
    initBoxHover();
});