from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import csv

app = Flask(__name__)
app.secret_key = '2fast4you-ePona35!'  # Setzen Sie hier einen sicheren Schlüssel

# Benutzerdaten mit gehashtem Passwort
users = {
    "Seyleen": generate_password_hash("Hamberg!"),
    "Juliane+Andreas": generate_password_hash("Grünstaude!"),
    "Luca+Lukas": generate_password_hash("Körnbach!"),
    "Sabine+Reinhard": generate_password_hash("Körnbach!"),
    "Antonia+Marc": generate_password_hash("Arzell!"),
    "Stefan": generate_password_hash("Hamberg!"),
    "Leni": generate_password_hash("Zell!"),
    "Johanna+Matthias": generate_password_hash("Zell!"),
    "Marina+Michi": generate_password_hash("Tiefenhüll!"),
    "Ivi+Rup": generate_password_hash("Reifenthal!"),
    "Philine+Johannes": generate_password_hash("Lüneburg!"),
    "Anna-Lena": generate_password_hash("Dittlofrod!"),
    "Gitte+Franz": generate_password_hash("Hamberg!"),
    "Larissa": generate_password_hash("Unterufhausen!"),
    "Kathy": generate_password_hash("Augsburg!")
}

# Pfad zur CSV-Datei für die Abstimmungsergebnisse
CSV_FILE_PATH = 'abstimmung.csv'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_hash = users.get(username)
        if user_hash and check_password_hash(user_hash, password):
            session['username'] = username  # Benutzer in der Session speichern
            return redirect(url_for('home'))
        else:
            return "Login fehlgeschlagen. Bitte versuche es erneut.", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Benutzer aus der Session entfernen
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'username' not in session:  # Überprüfen, ob der Benutzer in der Session gespeichert ist
        return redirect(url_for('login'))  # Nicht eingeloggte Benutzer zur Login-Seite umleiten
    return render_template('index.html')  # Eingeloggte Benutzer zur Hauptseite bringen

@app.route('/survey_food', methods=['POST'])
def survey_food():
    if request.method == 'POST':
        # Überprüfen, ob der Benutzer bereits abgestimmt hat
        if 'voted' in session:
            flash('Du hast bereits abgestimmt.', 'error')
            return redirect(url_for('home'))

        # Daten aus dem Formular erhalten
        vorname = request.form['food_vorname']
        nachname = request.form['food_nachname']
        vorspeise = request.form.get('vorspeise', '')
        hauptspeise = request.form.get('hauptspeise', '')
        nachspeise = request.form.get('nachspeise', '')
        special = request.form.get('special', '')
        anmerkungen = request.form.get('anmerkungen', '')

        # Daten in CSV-Datei schreiben
        with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Vorname', 'Nachname', 'Vorspeise', 'Hauptspeise', 'Nachspeise', 'Spezielle Ernährungsform', 'Anmerkungen']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Überprüfen, ob die CSV-Datei leer ist und ggf. die Header schreiben
        if csvfile.tell() == 0:
        writer.writeheader()
        # Schreiben der Daten in die CSV-Datei
        writer.writerow({'Vorname': vorname, 'Nachname': nachname, 'Vorspeise': vorspeise, 'Hauptspeise': hauptspeise, 'Nachspeise': nachspeise, 'Spezielle Ernährungsform': special, 'Anmerkungen': anmerkungen})


        # Daten in TXT-Datei schreiben
        with open('abstimmung.txt', 'a', encoding='utf-8') as txtfile:
        txtfile.write(f'Vorname: {vorname}\n')
        txtfile.write(f'Nachname: {nachname}\n')
        txtfile.write(f'Vorspeise: {vorspeise}\n')
        txtfile.write(f'Hauptspeise: {hauptspeise}\n')
        txtfile.write(f'Nachspeise: {nachspeise}\n')
        txtfile.write(f'Spezielle Ernährungsform: {special}\n')
        txtfile.write(f'Anmerkungen: {anmerkungen}\n')
        txtfile.write('\n')

        # Markiere den Benutzer als abgestimmt, um Mehrfachabstimmung zu verhindern
        session['voted'] = True

        flash('Vielen Dank für deine Abstimmung!', 'success')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
