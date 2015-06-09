// Hooks into a single SSE feed and sends the updates to all 4 components
$(function() {
    
    var source = new EventSource(Urls.display_data_update());
    source.onmessage = function(event) {
        var data = JSON.parse(event.data);

        $('.box').each(function() {
            if($(this).data('updateFunc') !== undefined)
                $(this).data('updateFunc')(data);
        });
    };
});