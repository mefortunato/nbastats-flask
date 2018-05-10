var data;
var teams;

var teamColors = {
    "LAL": [85,37,130], 
    "CHI": [206,17,65], 
    "LAC": [237,23,76], 
    "MIN": [0,80,131], 
    "DEN": [255,178,15], 
    "IND": [0,39,93], 
    "GSW": [253,185,39], 
    "PHX": [229,96,32], 
    "SAC": [114,76,159], 
    "DAL": [0,125,197], 
    "UTA": [0,43,92], 
    "BKN": [0,0,0], 
    "NOP": [0,43,92], 
    "ATL": [224,58,62], 
    "MEM": [35,55,91], 
    "SAS": [182,191,191], 
    "TOR": [206,17,65], 
    "HOU": [206,17,65], 
    "MIA": [152,0,46], 
    "ORL": [0,125,197], 
    "DET": [0,107,182], 
    "PHI": [237,23,76], 
    "POR": [0,0,0], 
    "CHA": [29,17,96], 
    "BOS": [0,131,72], 
    "WAS": [0,37,102], 
    "NYK": [245,132,38], 
    "CLE": [134,0,56], 
    "MIL": [0,71,27], 
    "OKC": [0,125,195]
}

$( document ).ready(function() {
    for (var i=1983; i<2018; i++) {
        if (i!=1998) {
            $('#year').append('<option>'+i+'</option>')
        }
    }
    var table = $('#stats').DataTable({
        "scrollX": "600px",
        "pageLength": 30,
        "bLengthChange": false,
        "searching": false,
        "bPaginate": false,
    });
    
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        Plotly.relayout('chart-div', {
            width: $('#chart-div').width()
        });
    });
    
    $('#table-tab').click(function() {
        $('#statistic-div').hide()
    });
    
    $('#graph-tab').click(function() {
        $('#statistic-div').show()
    });
    
    $('#statistic').change(function(event) {
        var statistic = $('#statistic').val();
        var colors = new Array();
        var statTeams = Object.keys(data[statistic])
        for (var team in statTeams) {
            if (teamColors.hasOwnProperty(statTeams[team])) {
                var c = teamColors[statTeams[team]];
            }
            else {
                var c = [0, 0, 0]
            }
            colors.push('rgba('+c[0]+','+c[1]+','+c[2]+',1)')
        }
        var stat_data = new Array({
            x: Object.keys(data[statistic]),
            y: Object.values(data[statistic]),
            type: 'bar',
            marker: {
                color: colors
            },
            transforms: [{
                type: 'sort',
                target: 'y',
                order: 'descending'
            }]
        })
        var layout = {
            width: $('#char-div').width(),
            height: 600,
            font: {
                family: 'Droid Serif'
            },
            xaxis: {
                title: 'Teams'
            },
            yaxis: {
                range: [0.95*Math.min.apply(Math, Object.values(data[statistic])), 1.05*Math.max.apply(Math, Object.values(data[statistic]))]
            }
        };
        Plotly.newPlot('chart-div', stat_data, layout);
    });
    
    $('#year').change(function(event) {
        $('#loader-table').show();
        var year = $('#year').val();
        $.get('/get-stats/'+year, function(json) {
            var tableData = new Array();
            data = JSON.parse(json['stats']);
            year = json['year'];
            stats = Object.keys(data);
            teams = Object.keys(data[stats[0]]);
            for (i=0; i<teams.length; i++) {
                var team = teams[i];
                var tempData = new Array();
                tempData.push(team);
                for (j=0; j<stats.length; j++) {
                    var stat = stats[j]
                    if (i == 0 && ($('#statistic option').length < stats.length)) {
                        $('#statistic').append('<option>'+stat+'</option>')
                    }
                    if (stat == 'TOTAL_WINS') {
                        tempData.push(data[stat][team].toFixed(0));
                    }
                    else {
                        tempData.push(data[stat][team].toFixed(2));
                    }
                }
                tableData.push(tempData);
            }
            
            var table = $('#stats').DataTable();
            table.data().clear()
            table.rows.add(tableData);
            table.draw();
            $('#statistic').change();
        }).always(function() {
            $('#loader-table').hide();
        });
        $('#year').blur()
    });
    
    $('#year').val(2017);
    $('#year').change();
    
    $('#next-stat').click(function() {
        $("#statistic > option:selected")
            .prop("selected", false)
            .next()
            .prop("selected", true);
        $("#statistic").change();
    });
    
    $('#next-year').click(function() {
        $("#year > option:selected")
            .prop("selected", false)
            .next()
            .prop("selected", true);
        $("#year").change();
    });
    
    $('#prev-year').click(function() {
        $("#year > option:selected")
            .prop("selected", false)
            .prev()
            .prop("selected", true);
        $("#year").change();
    });
    
    $('#prev-stat').click(function() {
        $("#statistic > option:selected")
            .prop("selected", false)
            .prev()
            .prop("selected", true);
        $("#statistic").change();
    });
});