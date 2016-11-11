# -*- coding: utf-8 -*-

from telm_webapp.database.configuration import db


# Klasa ECGRecording, która dziedziczy po klasie Model
class ECGRecording(db.Model):

    # Pola w klasie, czyli w tym przypadku kolumny w tabeli:

    # Kolumna typu integer - identyfikator danego przebiegu EKG -
    # klucz główny "primary key"
    id = db.Column(db.Integer, primary_key=True)

    # Kolumna typu string (to może być nazwa, opis)
    name = db.Column(db.String(1024))

    # Kolumna typu czas (np data badania)
    timestamp = db.Column(db.DateTime())

    # Konstruktor który służy do dodawania rzeczy do bazy danych
    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp

    # Dzięki tej metodzie można wypisywać obiekty na konsolę jako string
    def __repr__(self):
        return '<ECGRecording %s>' % self.name
