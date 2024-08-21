from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import csv
from collections import defaultdict

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
    "Johannes": generate_password_hash("Augsburg!")
}

def update_dish_count():
    gerichte_zähler = count_dishes_in_csv()
    
    # Schreibe die Zählung in die neue CSV-Datei
    with open('dish_count.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Gericht', 'Anzahl', 'Vegetarisch', 'Vegan'])
        for gericht, info in gerichte_zähler.items():
            writer.writerow([gericht, info['Anzahl'], info['Vegetarisch'], info['Vegan']])

    # Schreibe die Zählung in die neue TXT-Datei
    write_dish_count_to_txt(gerichte_zähler)

def count_dishes_in_csv():
    gerichte_zähler = defaultdict(lambda: {'Anzahl': 0, 'Vegetarisch': 0, 'Vegan': 0, 'Normal': 0})
    with open('survey_results.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                vorspeisen = row['Vorspeisen'].split(', ')
                hauptspeisen = row['Hauptspeisen'].split(', ')
                nachspeisen = row['Nachspeisen'].split(', ')
                special = row['Special'].split(', ')
            except KeyError:
                continue
            for gericht in vorspeisen + hauptspeisen + nachspeisen:
                if gericht:
                    gerichte_zähler[gericht]['Anzahl'] += 1
            if 'vegetarisch' in special or 'vegan' in special:
                for gericht in vorspeisen + hauptspeisen + nachspeisen:
                    if gericht:
                        gerichte_zähler[gericht]['Vegetarisch'] += 1
                        gerichte_zähler[gericht]['Vegan'] += 1 if 'vegan' in special else 0
            else:
                for gericht in vorspeisen + hauptspeisen + nachspeisen:
                    if gericht:
                        gerichte_zähler[gericht]['Normal'] += 1
    return gerichte_zähler




def write_dish_count_to_txt(gerichte_zähler):
    with open('dish_count.txt', 'w') as txtfile:
        for gericht, info in gerichte_zähler.items():
            vegetarisch = 'Ja' if info['Vegetarisch'] else 'Nein'
            vegan = 'Ja' if info['Vegan'] else 'Nein'
            txtfile.write(f"{gericht}: {info['Anzahl']}, vegetarisch: {vegetarisch}, vegan: {vegan}\n")

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

@app.route('/', methods=['GET', 'POST'])
def survey_food():
    if request.method == 'POST':
        food_name = request.form['name']
        lastname = request.form['lastname']
        vorspeisen = request.form.getlist('vorspeise')
        hauptspeisen = request.form.getlist('hauptspeise')
        nachspeisen = request.form.getlist('nachspeise')
        special = request.form.getlist('special')
        anmerkungen = request.form['anmerkungen']
        
        with open('survey_results.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Vorname', 'Nachname', 'Vorspeisen', 'Hauptspeisen', 'Nachspeisen', 'Special', 'Anmerkungen']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:  # Überprüfen, ob die Datei leer ist
                writer.writeheader()
            writer.writerow({'Vorname': food_name, 'Nachname': lastname, 
                             'Vorspeisen': ', '.join(vorspeisen), 
                             'Hauptspeisen': ', '.join(hauptspeisen), 
                             'Nachspeisen': ', '.join(nachspeisen),
                             'Special': ', '.join(special),
                             'Anmerkungen': anmerkungen})
        
        update_dish_count()  # Aktualisiere die Zählung der Gerichte
        return render_template('index.html')
    
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def survey_room():
    if request.method == 'POST':
        # Daten aus dem Formular extrahieren
        room_name = request.form['room_name']
        zimmer = request.form['zimmer']
        start_date = request.form['start-date']
        end_date = request.form['end-date']
        anmerkungen = request.form['anmerkungen']
        
        # Die Daten in die CSV-Datei schreiben
        with open('zimmerbuchung.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Vorname', 'Nachname', 'Zimmer', 'Startdatum', 'Enddatum', 'Anmerkungen']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:  # Überprüfen, ob die Datei leer ist
                writer.writeheader()
            writer.writerow({'Vorname': room_name, 'Zimmer': zimmer, 
                             'Startdatum': start_date, 'Enddatum': end_date, 'Anmerkungen': anmerkungen})
        
        return render_template('index.html')  # Nach der Übermittlung zur Startseite umleiten
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
