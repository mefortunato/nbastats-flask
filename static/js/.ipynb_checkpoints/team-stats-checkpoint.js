$( document ).ready(function() {
    for (var i=1983; i<2018; i++) {
        if (i!=1998) {
            $('#year').append('<option>'+i+'</option>')
        }
    }
    var table = $('#stats').DataTable({
        "scrollX": "600px",
        "pageLength": 30
    });
    $('#year').change(function(event) {
        $('#loader-table').show();
        var year = $('#year').val();
        $.get('/get-stats/'+year, function(json) {
            var tableData = new Array();
            data = JSON.parse(json['stats']);
            year = json['year'];
            stats = Object.keys(data);
            console.log(stats)
            teams = Object.keys(data[stats[0]]);
            for (i=0; i<teams.length; i++) {
                var team = teams[i];
                var tempData = new Array();
                tempData.push(team);
                //tempData['id'] = i;
                for (j=0; j<stats.length; j++) {
                    var stat = stats[j]
                    if (stat == 'TOTAL_WINS') {
                        tempData.push(data[stat][team].toFixed(0));
                    }
                    else {
                        tempData.push(data[stat][team].toFixed(2));
                    }
                }
                tableData.push(tempData);
            }
            console.log(tableData);
            
            var table = $('#stats').DataTable();
            table.data().clear()
            table.rows.add(tableData);
            table.draw();
        }).always(function() {
            console.log('done')
            $('#loader-table').hide();
        });
        $('#year').blur()
    });
    
    $('#year').val(2017);
    $('#year').change();
});