$(function() {
    var $box_kwh = $('#kwh_graph');
    var $box_prod = $('#prod_graph');
    
    String.prototype.lpad = function(padString, length) {
        var str = this;
        while (str.length < length)
            str = padString + str;
        return str;
    }

    function initGraphs() {
        $box_kwh.html('<div class="graph" style="width: 100%; height: 90%;"></div>');
        $box_prod.html('<div class="graph" style="width: 100%; height: 90%;"></div>');
        
        var time_ticks = [];
        for(h = 7; h < 18; h++) {
        	time_ticks.push([h, ("" + h).lpad("0", 2) + ":00"]);
        }
        $box_kwh.data('updateFunc', function(data) {
            $(data).each(function(i) {
            	var rec = data[i];
            	if(rec['type'] !== 'power')
            		return;
            	
            	kwh_graph_data = [];
            	prod_graph_data = [];
            	$(rec['circuits']).each(function(ci) {
            		var circuit = rec['circuits'][ci];

            		kwh_graph_data.push({
            			label: circuit['name'],
            			data: circuit['kwh']
            		});
            		prod_graph_data.push({
            			label: circuit['name'],
            			data: circuit['productivity']
            		});
            	});
            	kwh_graph_data.push({
            		label: 'Total',
            		data: rec['total']
            	});
            	kwh_graph_data.push({
            		label: 'Max',
            		data: [[7, rec['max_month']], [17, rec['max_month']]],
        			lines: {
        				fill: false
        			}
            	})
            	
                $.plot($box_kwh.find(".graph:first"), kwh_graph_data, {
                	series: {
        				stack: true,
        				lines: {
        					show: true,
        					fill: true,
        				},
        			},
        			xaxis: {
        				ticks: time_ticks
        			},
        			yaxis: {
        				tickFormatter: function formatter(val, axis) {
        				    return "" + val + " kWh";
        				}
        			},
        			legend: {
        				show: true,
        				backgroundOpacity: 0.5,
        			}
                });
                $.plot($box_prod.find(".graph:first"), prod_graph_data, {
                	series: {
        				stack: false,
        				lines: {
        					show: true,
        					fill: false,
        				},
        			},
        			xaxis: {
        				ticks: time_ticks
        			},
        			legend: {
        				show: true,
        				backgroundOpacity: 0.5,
        			}
                });
            });
        });
    }
    
    initGraphs();
});