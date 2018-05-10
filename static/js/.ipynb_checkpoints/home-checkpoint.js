$( document ).ready(function() {
    $.get('/get-pye-error/', function(json) {
        var mean = JSON.parse(json['mean']);
        var std = JSON.parse(json['std']);
        var x = Object.keys(mean).map(function(v) {return Number(v)})
        var y = x.map(function(k) {return mean[k]})
        var yerr = x.map(function(k) {return std[k]})
        var data = new Array({
            x:x, 
            y:y, 
            error_y: {
              type: 'data',
              array: yerr,
              visible: true
            }
        });
        var layout = {
            width: $('#char-div-1').width(),
            height: 600,
            title: 'Figure 1. Absolute Average PYE Error',
            font: {
                family: 'Droid Serif'
            },
            xaxis: {
                title: 'Games Played',
                linecolor: 'black',
                linewidth: 2,
                mirror: true,
                range: [0, 83]
            },
            yaxis: {
                title: 'PYE Error',
                linecolor: 'black',
                linewidth: 2,
                mirror: true,
                range: [0, Math.max.apply(Math, yerr)+Math.max.apply(Math, y)+0.2]
            }
        };

        Plotly.newPlot('chart-div-1', data, layout);
    });
    
    $.get('/get-proj-pye-error/', function(json) {
        var mean = JSON.parse(json['mean']);
        var std = JSON.parse(json['std']);
        var x = Object.keys(mean).map(function(v) {return Number(v)})
        var y = x.map(function(k) {return mean[k]})
        var yerr = x.map(function(k) {return std[k]})
        var data = new Array({
            x:x, 
            y:y, 
            error_y: {
              type: 'data',
              array: yerr,
              visible: true
            }
        });
        var layout = {
            width: $('#char-div-2').width(),
            height: 600,
            title: 'Figure 2. Absolute Projected Average PYE Error',
            font: {
                family: 'Droid Serif'
            },
            xaxis: {
                title: 'Games Played',
                linecolor: 'black',
                linewidth: 2,
                mirror: true,
                range: [0, 83]
            },
            yaxis: {
                title: 'PYE Error',
                linecolor: 'black',
                linewidth: 2,
                mirror: true,
                range: [0, Math.max.apply(Math, yerr)+Math.max.apply(Math, y)+0.2]
            }
        };

        Plotly.newPlot('chart-div-2', data, layout);
    });
});