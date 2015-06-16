$(function() {
    var $box = $('#graphs');

    var time_ticks = [];

    String.prototype.lpad = function(padString, length) {
        var str = this;
        while (str.length < length) {
            str = padString + str;
        }
        return str;
    };

    var mode = -1; // 0 = kWm, 1 = Deviations, 2 = Deviations per Room

    function setMode(new_mode) {
        mode = parseInt(new_mode);
        
        var $button = $box.find('.buttons ul .btn').eq(mode);
        $box.find('.buttons ul .active').removeClass('active');
        $button.addClass('active');
        
        $box.find('.graph').hide();
        $box.find('.graph').each(function() {
        	if(mode == parseInt($(this).attr('data-mode'))) {
        		$(this).show();
        		$(this).trigger('plot');
        	}
        });
    }

    function initGraphs() {
        $box.append('<div class="buttons"><ul></ul></div>');

        for(h = 0; h < 24; h++) {
            time_ticks.push([h, ("" + h).lpad("0", 2) + ":00"]);
        }

        initKwhGraph();
        initDeviationsTotalGraph();
        initButtons();

    	$box.data('updateFunc', function(rec) {
            if (rec.type !== 'graph') {
                return;
            }
            $box.find('.graph').each(function() {
            	$(this).data('updateFunc')(rec);
            });
    	});
        
        setMode(0);
    }
    
    function initButtons() {
        var $buttons = $box.find('.buttons');
        $box.find('.buttons ul').append('<li><button class="btn btn-default btn_kwm" data-mode="0"><i class="fa fa-bolt"></i> kWm</button></li>');
        $box.find('.buttons ul').append('<li><button class="btn btn-default btn_deviations" data-mode="1"><i class="fa fa-exclamation-triangle"></i> Deviations</button></li>');
        
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
        	if(mode !== undefined)
        		setMode(mode);
        });
    }
    
    function initKwhGraph() {
    	$box.append('<div class="kwm_graph graph" data-mode="0" style="width: 100%; height: 85%; margin-top: 40px; display: none;"></div>')
    	var $kwm_graph = $box.find(".kwm_graph:first");
    	
    	$kwm_graph.data('updateFunc', function(rec) {
            var graph_data = [];
            $(rec.circuits).each(function(ci) {
                var circuit = rec.circuits[ci];
                var vals = [];
                $(circuit.kwh).each(function(i) {
                	vals.push([circuit.kwh[i][0], circuit.kwh[i][1] * 60]);
                });
                
                graph_data.push({
                    label: circuit.name,
                    data: vals
                });
            });
            graph_data.push({
                label: 'Max',
                data: [[0, rec.max_month * 60], [24, rec.max_month * 60]],
                stack: false,
                lines: {
                    fill: false
                }
            });

            $kwm_graph.unbind('plot');
            $kwm_graph.bind('plot', function() {
                $.plot($kwm_graph, graph_data, {
                    series: {
                        stack: true,
                        lines: {
                            show: true,
                            fill: true,
                            steps: true
                        }
                    },
                    xaxis: {
                        ticks: time_ticks
                    },
                    yaxis: {
                        tickFormatter: function formatter(val, axis) {
                            return "" + val + " kWm";
                        }
                    },
                    legend: {
                        show: true,
                        backgroundOpacity: 0.5
                    }
                });            	
            });
            $kwm_graph.trigger('plot');
        });
    }
    
    function initDeviationsTotalGraph() {
    	$box.append('<div class="deviations_graph graph" data-mode="1" style="width: 100%; height: 85%; margin-top: 40px; display: none;"></div>')
    	var $dev_graph = $box.find(".deviations_graph:first");
    	
    	$dev_graph.data('updateFunc', function(rec) {
            var graph_data = [];
            $(rec.circuits).each(function(ci) {
                var circuit = rec.circuits[ci];
                var vals = [];
                $(circuit.kwh).each(function(i) {
                	vals.push([circuit.kwh[i][0], circuit.kwh[i][1] * 60]);
                });
                
                graph_data.push({
                    label: circuit.name,
                    data: vals
                });
            });

            $dev_graph.unbind('plot');
            $dev_graph.bind('plot', function() {
                $.plot($dev_graph, graph_data, {
                    series: {
                        stack: true,
                        lines: {
                            show: true,
                            fill: true,
                            steps: true
                        }
                    },
                    xaxis: {
                        ticks: time_ticks
                    },
                    yaxis: {
                        tickFormatter: function formatter(val, axis) {
                            return "" + val + " kWm";
                        }
                    },
                    legend: {
                        show: true,
                        backgroundOpacity: 0.5
                    }
                });            	
            });
            $dev_graph.trigger('plot');
        });    	
    }


    initGraphs();
});
