var winId = '#9a9b8ae9-b112-47fb-b741-9012dc43c5bb';
var pmId = '#a9f4fea0-8129-4c0b-a3f0-3e103bf24a50';
var spreadId = '#0da47853-17b1-49b3-9945-acb16977e280';
var totalId = '#7b05768d-ce85-494e-98d9-299bd987c74f';

$(document).ready(function() {
    $('#insights-link').addClass('active');
    
    $('.toggle-buttons').click(function() {
        $('.toggle-buttons.active').removeClass('btn-info');
        $('.toggle-buttons.active').addClass('btn-light');
        $('.toggle-buttons.active').removeClass('active');
        $(this).removeClass('btn-light');
        $(this).addClass('btn-info active');
        $('.bk-root').hide();
    })
    
    $('#win-btn').click(function() {
        $(winId).show();
    })
    
    $('#pm-btn').click(function() {
        $(pmId).show();
    })
    
    $('#spread-btn').click(function() {
        $(spreadId).show();
    })
    
    $('#total-btn').click(function() {
        $(totalId).show();
    })
})