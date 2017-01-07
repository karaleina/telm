# -*- coding: utf-8 -*-

# Flask to  jest framework (biblioteka) do aplikacji webowych. (Flask to klasa pakietu flask).
# render_template to funkcja, która na podstawie szablonu generuje html (importujemy konkretną funkcję z Flaska).
from flask import Flask, jsonify, render_template, request
from telm_webapp.database.configuration import db
from telm_webapp.database.models import ECGRecording
from telm_webapp.parsers.ecg_recording_data_parser import ECGRecordingDataParser

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
    # Query to zapytanie do bazy danych = "daj mi wszystkie rekordingi jakie są w bazie"
    recordings = ECGRecording.query.all()
    # Renderuje html na podstawie szablonu
    return render_template('main.html', recordings=recordings)


@app.route("/recordings/<int:recording_id>/view")
def show_recording(recording_id):
    # Tutaj pobieram z bazy rekord o zadanym id i dostaję obiekt
    recording = ECGRecording.query.get(recording_id)
    recording_data_with_time = get_raw_recording_data(recording_id, 0, 30)
    return render_template(
        'ecg_view.html',
        recording=recording,
        recording_data=recording_data_with_time)


# Widok służący do zwracania danych z danego przedziału czasu
@app.route("/recordings/<int:recording_id>")
def get_recording_data(recording_id):
    start_time = int(request.args.get('from'))
    end_time = int(request.args.get('to'))
    return jsonify({'recordingData': get_raw_recording_data(recording_id, start_time, end_time)})


def get_raw_recording_data(recording_id, start_time, end_time):
    recording = ECGRecording.query.get(recording_id)

    from_sample = max(0, start_time * recording.frequency)
    to_sample = min(recording.sample_count - 1, end_time * recording.frequency)

    recording_data = ECGRecordingDataParser().parse(recording.url, from_sample, to_sample)
    recording_data_with_time = [
        [(from_sample + index) / float(recording.frequency)] + recording_data_sample
        for index, recording_data_sample in enumerate(recording_data)]

    return recording_data_with_time


# Uruchamia aplikację, jeśli plik nie jest importowany, tylko uruchamiany
if __name__ == "__main__":
    app.run()
 