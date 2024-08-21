from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

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

if __name__ == '__main__':
    app.run(debug=True)
