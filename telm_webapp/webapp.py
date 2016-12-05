# -*- coding: utf-8 -*-

# Flask to  jest framework (biblioteka) do aplikacji webowych. (Flask to klasa pakietu flask).
# render_template to funkcja, która na podstawie szablonu generuje html (importujemy konkretną funkcję z Flaska).
from flask import Flask, render_template
from telm_webapp.database.configuration import db
from telm_webapp.database.models import ECGRecording

# Konstruktor klasy Flask - reprezentuje aplikację webową
app = Flask(__name__)

# Mówimy, jaka to baza danych (sqlite) i mówimy gdzie ona jest
# (lub ma być, bo jak nie ma to tworzymy)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecg-database.sqlite'

# Przypisuje aplikację do bazy danych.
db.app = app
db.init_app(app)
# Udostępniam innym modułom, innemu kodowi bazę danych z przypisaną już aplikacją
db_in_app = db

# "Małpka" = dekorator
# @app.route(<url>) - Widok dla konkretnego adresu url
# "/" oznacza url (widok) główny
@app.route("/")
def recording_list():
    # Pobiera z bazy wszystkie rekordy ECG i zwraca jako tablica obiektów tej samej klasy
    # Query to zapytanie do bazy danych
    recordings = ECGRecording.query.all()
    # Renderuje html na podstawie szablonu
    return render_template('main.html', recordings=recordings)

@app.route("/recordings/<int:recording_id>")
def show_recording(recording_id):
    # Tutaj pobieram z bazy rekord o zadanym id i dostaję obiekt
    recording = ECGRecording.query.get(recording_id)
    return render_template('ecg_view.html', recording=recording)


# Uruchamia aplikację, jeśli plik nie jest importowany, tylko uruchamiany
if __name__ == "__main__":
    app.run()
 