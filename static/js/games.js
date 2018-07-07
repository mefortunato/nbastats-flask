var md = new MobileDetect(window.navigator.userAgent);

function redirect() {
    var date = $("#date").val();
    window.location = 'http://'+window.location.host+'/games/'+date;
}

$(document).ready(function() {
    if (md.mobile()) {
        $("#submit").removeClass('d-none');
    }
    $("#date").blur(function() {
        redirect();
    });
    $("form").submit(function(e) {
        e.preventDefault();
        $("#date").blur();
    });
    $('#games-link').addClass('active');
})