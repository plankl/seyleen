document.addEventListener('DOMContentLoaded', function () {
    var countdownTimer = document.getElementById('countdown-timer');
    // Setze das Datum deiner Hochzeit in UTC-Zeit
    var countdownDateUTC = new Date("05/24/2024 00:00:00 GMT+0000").getTime();
    
    var berlinOffset = 2; // Berliner Zeit hat eine UTC-Verschiebung von +2 Stunden

    var x = setInterval(function() {
        var berlinNow = new Date().getTime() + (berlinOffset * 3600000); // Hinzufügen der Verschiebung für Berlin
        var distance = countdownDateUTC - berlinNow;

        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));

        countdownTimer.innerHTML = days + " Tage " + hours + " Stunden "
        + minutes + " Minuten ";

        if (distance < 0) {
            clearInterval(x);
            countdownTimer.innerHTML = "Wir haben geheiratet!";
        }
    }, 1000);
});
