// Funktion zur Validierung des Formulars für die Essensumfrage
function validateFoodForm() {
    // Überprüfen, ob alle erforderlichen Felder ausgefüllt sind
    var name = document.getElementById("name").value;
    var vorspeise = document.getElementById("vorspeise").value;
    var hauptspeise = document.getElementById("hauptspeise").value;
    var nachspeise = document.getElementById("nachspeise").value;

    if (name === "" || vorspeise === "" || hauptspeise === "" || nachspeise === "") {
        alert("Bitte fülle alle Felder aus.");
        return false; // Formular wird nicht gesendet
    }

    return true; // Formular wird gesendet
}
