$(function() {
    var $box = $('#graphs');
    
    String.prototype.lpad = function(padString, length) {
        var str = this;
        while (str.length < length)
            str = padString + str;
        return str;
    }

    function initChartBox() {
        $box.html('<div id="graph" style="width: 100%; height: 90%;"></div>');
        
        var time_ticks = [];
        for(h = 7; h < 18; h++) {
        	time_ticks.push([h, ("" + h).lpad("0", 2) + ":00"]);
        }
        $box.data('updateFunc', function(data) {
            $(data).each(function(i) {
            	var rec = data[i];
            	if(rec['type'] !== 'power')
            		return;
            	
            	graph_data = [];
            	$(rec['circuits']).each(function(ci) {
            		var circuit = rec['circuits'][ci];

            		graph_data.push({
            			label: circuit['name'],
            			data: circuit['kwh']
            		});
            	});
            	graph_data.push({
            		label: 'Total',
            		data: rec['total']
            	});
            	graph_data.push({
            		label: 'Max',
            		data: [[7, rec['max_month']], [17, rec['max_month']]],
        			lines: {
        				fill: false
        			}
            	})
            	
                $.plot("#graph", graph_data, {
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
            });
        });
    }
    
    initChartBox();
});