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

    function initGraphs() {
        $box.append('<div class="graph" style="width: 100%; height: 85%; margin-top: 30px;"></div>');

        for(h = 0; h < 24; h++) {
            time_ticks.push([h, ("" + h).lpad("0", 2) + ":00"]);
        }

        initKwhGraph();
    }
    
    function initKwhGraph() {
        $box.data('updateFunc', function(rec) {
            if (rec.type !== 'graph') {
                return;
            }

            graph_data = [];
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

            $box.unbind('plot');
            $box.bind('plot', function() {
                $.plot($box.find(".graph:first"), graph_data, {
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
            $box.trigger('plot');
        });
    }


    initGraphs();
});
