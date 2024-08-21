from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import csv
from datetime import datetime
import os

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
    "Kathy": generate_password_hash("Augsburg!"),
    "Johannes": generate_password_hash("Augsburg!"),
    "Lisi": generate_password_hash("Starnberg!"),
    "Lara-Kary": generate_password_hash("München!")
}

# Pfad zur CSV-Datei für die Abstimmungsergebnisse
FOOD_CSV_FILE_PATH = 'essen.csv'
ROOM_CSV_FILE_PATH = 'zimmer.csv'

# Pfad zur TXT-Datei für die Abstimmungsergebnisse
FOOD_TXT_FILE_PATH = 'essen.txt'
ROOM_TXT_FILE_PATH = 'zimmer.txt'

# Pfad zur TXT-Datei für das Aktivitätsprotokoll
LOG_FILE_PATH = 'activity_log.txt'

# Definiere eine globale Variable für die Anzahl der Anmeldungen
login_count = 0

def log_activity(username, ip_address, device_info):
    global login_count  # Zugriff auf die globale Variable
    login_count += 1  # Inkrementiere die Anzahl der Anmeldungen
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    # Extrahiere die tatsächliche IP-Adresse aus den Proxy-Headern
    real_ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    
    log_entry = f'Datum: {timestamp}\nLogin(s): {login_count}\nBenutzer: {username}\nIP-Adresse: {real_ip_address}\nGerät: {device_info}\n\n'

    # Überprüfen, ob die Log-Datei existiert, wenn nicht, erstellen
    if not os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'w', encoding='utf-8') as log_file:
            log_file.write("Aktivitätsprotokoll\n\n")

    # Log-Eintrag zur Datei hinzufügen
    with open(LOG_FILE_PATH, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_hash = users.get(username)
        if user_hash and check_password_hash(user_hash, password):
            session['username'] = username  # Benutzer in der Session speichern
            log_activity(username, request.remote_addr, request.user_agent.string)
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
        # Erfassen der aktuellen Zeit und Datum in deutscher Schriftweise
        now = datetime.now()
        timestamp = now.strftime("%d.%m.%Y %H:%M:%S")

        # Erfassen der IP-Adresse des Abstimmers
        ip_address = request.remote_addr

        # Daten aus dem Formular erhalten
        vorname = request.form['food_vorname']
        nachname = request.form['food_nachname']
        vorspeise = request.form.get('vorspeise', '')
        hauptspeise = request.form.get('hauptspeise', '')
        nachspeise = request.form.get('nachspeise', '')
        special = request.form.get('special', '')
        anmerkungen = request.form.get('anmerkungen', '')

        # Daten in CSV-Datei schreiben
        with open(FOOD_CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Datum', 'IP-Adresse', 'Vorname', 'Nachname', 'Vorspeise', 'Hauptspeise', 'Nachspeise', 'Spezielle Ernährungsform', 'Anmerkungen']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'Datum': timestamp, 'IP-Adresse': ip_address, 'Vorname': vorname, 'Nachname': nachname, 'Vorspeise': vorspeise, 'Hauptspeise': hauptspeise, 'Nachspeise': nachspeise, 'Spezielle Ernährungsform': special, 'Anmerkungen': anmerkungen})

        # Daten in TXT-Datei schreiben
        with open(FOOD_TXT_FILE_PATH, 'a', encoding='utf-8') as txtfile:
            txtfile.write(f'Datum: {timestamp}\n')
            txtfile.write(f'IP-Adresse: {ip_address}\n')
            txtfile.write(f'Vorname: {vorname}\n')
            txtfile.write(f'Nachname: {nachname}\n')
            txtfile.write(f'Vorspeise: {vorspeise}\n')
            txtfile.write(f'Hauptspeise: {hauptspeise}\n')
            txtfile.write(f'Nachspeise: {nachspeise}\n')
            txtfile.write(f'Spezielle Ernährungsform: {special}\n')
            txtfile.write(f'Anmerkungen: {anmerkungen}\n')
            txtfile.write('\n')

        flash('Gewünschtes Essen übermittelt', 'success')
        return redirect(url_for('home'))

@app.route('/survey_room', methods=['POST'])
def survey_room():
    if request.method == 'POST':
        # Erfassen der aktuellen Zeit und Datum in deutscher Schriftweise
        now = datetime.now()
        timestamp = now.strftime("%d.%m.%Y %H:%M:%S")

        # Erfassen der IP-Adresse des Abstimmers
        ip_address = request.remote_addr

        # Erfassen des Benutzer-Agenten
        device_info = request.user_agent.string

        # Daten aus dem Formular erhalten
        name = request.form['room_name']
        zimmer = request.form['zimmer']
        start_date = request.form['start-date']
        end_date = request.form['end-date']
        anmerkungen = request.form.get('anmerkungen', '')

        # Convert the date strings to datetime objects for comparison
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

        # Validate the dates
        if start_date_obj < now:  # Check if start date is in the past
            flash('Das Startdatum muss am jetzigen Tag oder in der Zukunft liegen.', 'error')
            return redirect(url_for('home'))
        elif end_date_obj < start_date_obj:  # Check if end date is older than start date
            flash('Das Enddatum darf nicht älter als das Startdatum sein.', 'error')
            return redirect(url_for('home'))

        # Daten in CSV-Datei schreiben
        with open(ROOM_CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Datum', 'IP-Adresse', 'Gerät', 'Name', 'Zimmer', 'Startdatum', 'Enddatum', 'Anmerkungen']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'Datum': timestamp, 'IP-Adresse': ip_address, 'Gerät': device_info, 'Name': name, 'Zimmer': zimmer, 'Startdatum': start_date, 'Enddatum': end_date, 'Anmerkungen': anmerkungen})

        # Daten in TXT-Datei schreiben
        with open(ROOM_TXT_FILE_PATH, 'a', encoding='utf-8') as txtfile:
            txtfile.write(f'Datum: {timestamp}\n')
            txtfile.write(f'IP-Adresse: {ip_address}\n')
            txtfile.write(f'Gerät: {device_info}\n')
            txtfile.write(f'Name: {name}\n')
            txtfile.write(f'Zimmer: {zimmer}\n')
            txtfile.write(f'Startdatum: {start_date}\n')
            txtfile.write(f'Enddatum: {end_date}\n')
            txtfile.write(f'Anmerkungen: {anmerkungen}\n')
            txtfile.write('\n')

        flash('Zimmerbuchung übermittelt', 'success')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
