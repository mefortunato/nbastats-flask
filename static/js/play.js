var home_win = null;
var home_spread = null;
var home_total = null;

var total_games = 0;

var user = {win:0, spread:0, total:0};
var bs = {win:0, spread:0, total:0};

var game_info = null

function render_info(json) {
    console.log(json)
    $('#date').text(json['date'])
    $('#home-logo').attr("src", json['logos'][0]);
    $('#away-logo').attr("src", json['logos'][1]);
    var info = Object.values(json['info'])[0];
    game_info = info;
    $('#spread').text(info['home_abrv'] + ' ' + info['spread']);
    $('#o-u').text(info['total']);
    $('#home-abrv-win').text(info['home_abrv']);
    $('#home-abrv-spread').text(info['home_abrv']);
    home_win = info['win'];
    home_spread = info['spread_cover'];
    home_total = info['total_cover'];
}

function update_scores(user_win, user_spread, user_total) {
    total_games += 1;
    if (user_win == game_info['win']) {
        user['win'] += 1;
        $('#slider-win').css('background-color', 'rgba(0, 155, 0, 0.5)');
    }
    else {
        $('#slider-win').css('background-color', 'rgba(155, 0, 0, 0.5)');
    }
    if (user_spread == game_info['spread_cover']) {
        user['spread'] += 1;
        $('#slider-spread').css('background-color', 'rgba(0, 155, 0, 0.5)');
    }
    else {
        $('#slider-spread').css('background-color', 'rgba(155, 0, 0, 0.5)');
    }
    if (user_total == game_info['total_cover']) {
        user['total'] += 1;
        $('#slider-total').css('background-color', 'rgba(0, 155, 0, 0.5)');
    }
    else {
        $('#slider-total').css('background-color', 'rgba(155, 0, 0, 0.5)');
    }
    
    if (game_info['win_pred'] == game_info['win']) {
        bs['win'] += 1;
    }
    if (game_info['spread_pred'] == game_info['spread_cover']) {
        bs['spread'] += 1;
    }
    if (game_info['total_pred'] == game_info['total_cover']) {
        bs['total'] += 1;
    }
    render_scores();
}

function render_scores() {
    $('#user-win-correct').text(user['win'])
    $('#user-spread-correct').text(user['spread'])
    $('#user-total-correct').text(user['total'])
    
    $('#user-win-total').text(total_games)
    $('#user-spread-total').text(total_games)
    $('#user-total-total').text(total_games)
    
    $('#bs-win-correct').text(bs['win'])
    $('#bs-spread-correct').text(bs['spread'])
    $('#bs-total-correct').text(bs['total'])
    
    $('#bs-win-total').text(total_games)
    $('#bs-spread-total').text(total_games)
    $('#bs-total-total').text(total_games)
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
        render_info(json);
    });
    
    $('#submit').click(function(e) {
        e.preventDefault();
        var user_win = $('#user-pick-win')[0].checked;
        var user_spread = $('#user-pick-spread')[0].checked;
        var user_total = $('#user-pick-total')[0].checked;
        update_scores(user_win, user_spread, user_total);
        $('#home-pts').text(game_info['pts']);
        $('#away-pts').text(game_info['pts_a']);
        $('#submit').prop("disabled",true);
    })
    
    $('#next').click(function(e) {
        e.preventDefault();
        $('#user-pick-win')[0].checked=false;
        $('#user-pick-spread')[0].checked=false;
        $('#user-pick-total')[0].checked=false;
        $('#home-pts').text('');
        $('#away-pts').text('');
        $('#slider-win').css('background-color', '#ccc');
        $('#slider-spread').css('background-color', '#ccc');
        $('#slider-total').css('background-color', '#ccc');
        fetch('/random-game/').then((resp) => resp.json()).then(json => {
            render_info(json);
        });
        $('#submit').prop("disabled",false);
    })
})