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

def update_booking_count(room_name, zimmer, start_date, end_date, anmerkungen):
    bookings = count_bookings_in_csv()

    # Füge die neue Buchung zur Liste der Buchungen hinzu
    new_booking = [session.get('username'), zimmer, start_date, end_date, anmerkungen]
    bookings.append(new_booking)

    # Schreibe die Buchungen in die neue CSV-Datei
    with open('zimmer_buchung.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Username', 'Zimmernummer', 'Startdatum', 'Enddatum', 'Anmerkungen'])
        writer.writerows(bookings)

    # Schreibe die Buchungen in die neue TXT-Datei
    write_booking_count_to_txt(bookings)


def count_bookings_in_csv():
    bookings = []
    try:
        with open('zimmer_buchung.csv', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                bookings.append([row['Vorname'], row['Nachname'], row['Zimmernummer'], row['Startdatum'], row['Enddatum'], row['Anmerkungen']])
    except FileNotFoundError:
        # Wenn die Datei nicht gefunden wird, geben Sie eine leere Liste zurück
        return bookings
    except Exception as e:
        # Wenn ein anderer Fehler auftritt, geben Sie eine Fehlermeldung aus
        print(f"Fehler beim Lesen der CSV-Datei: {e}")
    return bookings

def write_booking_count_to_txt(bookings):
    with open('zimmer_buchung.txt', 'w') as txtfile:
        for booking in bookings:
            txtfile.write(f"Vorname: {booking[0]}, Nachname: {booking[1]}, Zimmernummer: {booking[2]}, Startdatum: {booking[3]}, Enddatum: {booking[4]}, Anmerkungen: {booking[5]}\n")

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

@app.route('/survey_food', methods=['GET', 'POST'])
def survey_food():
    if request.method == 'POST':
        food_vorname = request.form['food_vorname']
        food_nachname = request.form['food_nachname']
        # Weitere Verarbeitung des Formulars hier
        update_booking_count()  # Aktualisiere die Buchungszählung
        return redirect('/')  # Nach der Übermittlung zur Startseite umleiten
    
    return render_template('index.html')

@app.route('/survey_room', methods=['GET', 'POST'])
def survey_room():
    if request.method == 'POST':
        room_vorname = request.form['room_vorname']
        room_nachname = request.form['room_nachname']
        zimmer = request.form['zimmer']
        start_date = request.form['start-date']
        end_date = request.form['end-date']
        anmerkungen = request.form['anmerkungen']
        
        # Weitere Verarbeitung des Formulars hier
        update_booking_count(room_vornname, zimmer, start_date, end_date, anmerkungen)  # Aktualisiere die Buchungszählung
        return redirect('/')  # Nach der Übermittlung zur Startseite umleiten
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
