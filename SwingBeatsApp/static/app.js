$(function () {
    function appendZero(val) {
        if (parseInt(val) < 10) {
            return "0"+val;
        }
        else{
            return val;
        }
    }
    function populateReadings() {
        $.ajax({
            url: '/epic-iot/readings/',
            type: 'GET',
            success: function (response) {
                if (response.calories != 0) {
                    $('#calories').find('p').html(appendZero(response.calories));
                }
                else {
                    $('#calories').find('p').html("N/A");
                }
                if (response.steps != 0) {
                    $('#steps').find('p').html(appendZero(response.steps));
                }
                else {
                    $('#steps').find('p').html("N/A");
                }
                if (response.heart_rate != 0) {
                    if (response.hrThreshold == 1)
                    {
                        $('#heart_rate').find('p').css('color', 'red');    
                    }
                    else {
                        $('#heart_rate').find('p').css('color', 'black');  
                    }
                    $('#heart_rate').find('span.superscriptBPM').show();                    
                    $('#heart_rate').find('p').html(appendZero(response.heart_rate));
                }
                else {
                    $('#heart_rate').find('p').html("N/A");
                    $('#heart_rate').find('span.superscriptBPM').hide();
                }
            },
            error: function (x, e) {

            }
        });
    }
    setInterval(populateReadings, 5000);
    populateReadings();
});