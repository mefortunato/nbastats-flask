var homeWin = null;
var homeSpread = null;
var homeTotal = null;

var totalGames = 0;

var user = {win:0, spread:0, total:0};
var bs = {win:0, spread:0, total:0};

var gameInfo = null

var bsPredText = '<b><span style="color:#38a553">B</span><span style="color:#3a64a8">S</span></b> pred: ';

function renderInfo(json) {
    console.log(json)
    $('#date').text(json['date'])
    $('#home-logo').attr("src", json['logos'][0]);
    $('#away-logo').attr("src", json['logos'][1]);
    var info = Object.values(json['info'])[0];
    gameInfo = info;
    $('#spread').text(info['home_abrv'] + ' ' + info['spread']);
    $('#o-u').text(info['total']);
    $('#home-abrv-win').text(info['home_abrv']);
    $('#home-abrv-spread').text(info['home_abrv']);
    homeWin = info['win'];
    homeSpread = info['spread_cover'];
    homeTotal = info['total_cover'];
}

function updateScores(userWin, userSpread, userTotal) {
    totalGames += 1;
    if (userWin == gameInfo['win']) {
        user['win'] += 1;
        $('#slider-win').css('background-color', 'rgba(0, 155, 0, 0.5)');
    }
    else {
        $('#slider-win').css('background-color', 'rgba(155, 0, 0, 0.5)');
    }
    if (userSpread == gameInfo['spread_cover']) {
        user['spread'] += 1;
        $('#slider-spread').css('background-color', 'rgba(0, 155, 0, 0.5)');
    }
    else {
        $('#slider-spread').css('background-color', 'rgba(155, 0, 0, 0.5)');
    }
    if (userTotal == gameInfo['total_cover']) {
        user['total'] += 1;
        $('#slider-total').css('background-color', 'rgba(0, 155, 0, 0.5)');
    }
    else {
        $('#slider-total').css('background-color', 'rgba(155, 0, 0, 0.5)');
    }
    
    if (gameInfo['win_pred'] == gameInfo['win']) {
        bs['win'] += 1;
        $('#bs-pred-win').append(
            bsPredText+(100*gameInfo['win_pred_proba']).toFixed(2)+'% &#10004;'
        );
    }
    else {
        $('#bs-pred-win').append(
            bsPredText+(100*gameInfo['win_pred_proba']).toFixed(2)+'% &#10006;'
        );
    }
    if (gameInfo['spread_pred'] == gameInfo['spread_cover']) {
        bs['spread'] += 1;
        $('#bs-pred-spread').append(
            bsPredText+(100*gameInfo['spread_pred_proba']).toFixed(2)+'% &#10004;'
        );
    }
    else {
        $('#bs-pred-spread').append(
            bsPredText+(100*gameInfo['spread_pred_proba']).toFixed(2)+'% &#10006;'
        );
    }
    if (gameInfo['total_pred'] == gameInfo['total_cover']) {
        bs['total'] += 1;
        $('#bs-pred-total').append(
            bsPredText+(100*gameInfo['total_pred_proba']).toFixed(2)+'% &#10004;'
        );
    }
    else {
        $('#bs-pred-total').append(
            bsPredText+(100*gameInfo['total_pred_proba']).toFixed(2)+'% &#10006;'
        );
    }
    renderScores();
}

function renderScores() {
    $('#user-win-correct').text((100*user['win']/totalGames).toFixed(2)+'%');
    $('#user-spread-correct').text((100*user['spread']/totalGames).toFixed(2)+'%');
    $('#user-total-correct').text((100*user['total']/totalGames).toFixed(2)+'%');
    
    $('#bs-win-correct').text((100*bs['win']/totalGames).toFixed(2)+'%');
    $('#bs-spread-correct').text((100*bs['spread']/totalGames).toFixed(2)+'%');
    $('#bs-total-correct').text((100*bs['total']/totalGames).toFixed(2)+'%');
}

$(document).ready(function() {
    $('#play-link').addClass('active');
    
    $('input').click(function() {
        var cat = this.id.substring(10);
        if (this.checked) {
            $('#slider-'+cat).css('background-color', '#999')
        }
        else {
            $('#slider-'+cat).css('background-color', '#ccc')
        }
    })
    
    fetch('/random-game/').then((resp) => resp.json()).then(json => {
        renderInfo(json);
    });
    
    $('#submit').click(function(e) {
        e.preventDefault();
        var userWin = $('#user-pick-win')[0].checked;
        var userSpread = $('#user-pick-spread')[0].checked;
        var userTotal = $('#user-pick-total')[0].checked;
        updateScores(userWin, userSpread, userTotal);
        $('#home-pts').text(gameInfo['pts']);
        $('#away-pts').text(gameInfo['pts_a']);
        $('#submit').prop("disabled",true);
    })
    
    $('#next').click(function(e) {
        e.preventDefault();
        $('#user-pick-win')[0].checked=false;
        $('#user-pick-spread')[0].checked=false;
        $('#user-pick-total')[0].checked=false;
        $('#home-pts').text('');
        $('#away-pts').text('');
        $('#bs-pred-win').text('');
        $('#bs-pred-spread').text('');
        $('#bs-pred-total').text('');
        $('#slider-win').css('background-color', '#ccc');
        $('#slider-spread').css('background-color', '#ccc');
        $('#slider-total').css('background-color', '#ccc');
        fetch('/random-game/').then((resp) => resp.json()).then(json => {
            renderInfo(json);
        });
        $('#submit').prop("disabled",false);
    })
})