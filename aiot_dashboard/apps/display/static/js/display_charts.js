$(function() {
    var $box_kwh = $('#kwh_graph');
    var $box_prod = $('#prod_graph');
    var $box_max_kwh = $('#max_kwh_chart');
    var $all_boxes = $('#kwh_graph, #prod_graph');

    var time_ticks = [];

    String.prototype.lpad = function(padString, length) {
        var str = this;
        while (str.length < length) {
            str = padString + str;
        }
        return str;
    };

    function initGraphs() {
        $all_boxes.html('<div class="graph" style="width: 100%; height: 85%;"></div>');
        $box_prod.prepend("<h2>Power utilization</h2>");
        $box_kwh.prepend("<h2>Power consumption</h2>");

        for(h = 7; h < 18; h++) {
            time_ticks.push([h, ("" + h).lpad("0", 2) + ":00"]);
        }

        initKwhGraph();
        initProdGraph();
        initMaxKwhGauge();
    }

    function initKwhGraph() {
        $box_kwh.data('updateFunc', function(rec) {
            if (rec.type !== 'graph') {
                return;
            }

            graph_data = [];
            $(rec.circuits).each(function(ci) {
                var circuit = rec.circuits[ci];

                graph_data.push({
                    label: circuit.name,
                    data: circuit.kwh
                });
            });
            graph_data.push({
                label: 'Max',
                data: [[7, rec.max_month], [17, rec.max_month]],
                stack: false,
                lines: {
                    fill: false
                }
            });

            $.plot($box_kwh.find(".graph:first"), graph_data, {
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
                        return "" + val + " kW";
                    }
                },
                legend: {
                    show: true,
                    backgroundOpacity: 0.5
                }
            });
        });
    }
    function initProdGraph() {
        $box_prod.data('updateFunc', function(rec) {
            if(rec.type !== 'graph') {
                return;
            }

            graph_data = [];
            graph_data.push({
                data: rec.productivity
            });

            $.plot($box_prod.find(".graph:first"), graph_data, {
                series: {
                    stack: false,
                    lines: {
                        show: true,
                        fill: false
                    }
                },
                xaxis: {
                    ticks: time_ticks
                },
                legend: {
                    show: true,
                    backgroundOpacity: 0.5
                }
            });
        });
    }
    function initMaxKwhGauge() {
        $box_max_kwh.html('<div id="max_kwh_gauge" style="width: 100%; height: 90%;"></div>');
        var g = new JustGage({
            id: "max_kwh_gauge",
            value: 0,
            min: 0,
            max: 100,
            title: "Power consumption (kW)",
            minLabelMinFontSize: 20,
            maxLabelMinFontSize: 20
        });

        $box_max_kwh.data('updateFunc', function(rec) {
            if(rec.type !== 'current_kwh') {
                return;
            }

            g.refresh(rec.data.current, rec.data.max);
        });
    }

    initGraphs();
});
