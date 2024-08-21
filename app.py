from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = '2fast4you-ePona35!'  # Setzen Sie hier einen sicheren Schlüssel

# Benutzerdaten mit gehashtem Passwort
users = {
    "Seyleen": generate_password_hash("Hamberg!-"),
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

# Pfad zur TXT-Datei für die Abstimmungsergebnisse
FOOD_TXT_FILE_PATH = 'Mittagessen.txt'

def log_activity(username, ip_address, device_info):
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    real_ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    log_entry = f'Datum: {timestamp}\nBenutzer: {username}\nIP-Adresse: {real_ip_address}\nGerät: {device_info}\n\n'

    LOG_FILE_PATH = 'activity.log'  # Pfad zur Aktivitätsprotokolldatei

    if not os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'w', encoding='utf-8') as log_file:
            log_file.write("Aktivitätsprotokoll\n\n")

    with open(LOG_FILE_PATH, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_hash = users.get(username)
        if user_hash and check_password_hash(user_hash, password):
            session['username'] = username
            log_activity(username, request.remote_addr, request.user_agent.string)
            return redirect(url_for('home'))
        else:
            flash("Login fehlgeschlagen. Bitte versuche es erneut.", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/survey_food', methods=['POST'])
def survey_food():
    if request.method == 'POST':
        now = datetime.now()
        timestamp = now.strftime("%d.%m.%Y %H:%M:%S")
        ip_address = request.remote_addr
        name = request.form['name']
        #vorspeise = request.form['vorspeise']
        hauptspeise = request.form['hauptspeise']
        #nachspeise = request.form['nachspeise']
        sonstiges = request.form['sonstiges']  # Hinzufügen des Feldes "Sonstiges"
        
        # Hinzufügen der Umfrageergebnisse zur TXT-Datei
        with open(FOOD_TXT_FILE_PATH, 'a', encoding='utf-8') as txtfile:
            txtfile.write(f'Datum: {timestamp}\n')
            txtfile.write(f'IP-Adresse: {ip_address}\n')
            txtfile.write(f'Name: {name}\n')
            #txtfile.write(f'Vorspeise: {vorspeise}\n')
            txtfile.write(f'Hauptspeise: {hauptspeise}\n')
            #txtfile.write(f'Nachspeise: {nachspeise}\n')
            txtfile.write(f'Sonstiges: {sonstiges}\n\n')
        
        flash('Gewünschtes Mittagessen übermittelt', 'success')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
