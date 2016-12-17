# -*- coding: utf-8 -*-

from telm_webapp.database.configuration import db


# Klasa ECGRecording, która dziedziczy po klasie Model
class ECGRecording(db.Model):
    __tablename__ = 'ecgrecording'

    # Pola w klasie, czyli w tym przypadku kolumny w tabeli:

    # Kolumna typu integer - identyfikator danego przebiegu EKG -
    # klucz główny "primary key"
    id = db.Column(db.Integer, primary_key=True)

    # Kolumna typu string (to może być nazwa, opis)
    name = db.Column(db.String(1024))

    # Kolumna typu czas (np data badania)
    timestamp = db.Column(db.DateTime())
    id_patient = db.Column(db.Integer, db.ForeignKey('ecgpatient.id'))
    plots = db.relationship("ECGPlot")
    # Konstruktor który służy do dodawania rzeczy do bazy danych
    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp

    # Dzięki tej metodzie można wypisywać obiekty na konsolę jako string
    def __repr__(self):
        return '<ECGRecording %s>' % self.name


# Klasa ECGRecording, która dziedziczy po klasie Model
class ECGPatient(db.Model):
    __tablename__ = 'ecgpatient'

    # Pola w klasie, czyli w tym przypadku kolumny w tabeli:

    # Kolumna typu integer - identyfikator danego przebiegu EKG -
    # klucz główny "primary key"
    id = db.Column(db.Integer, primary_key=True)

    # Kolumna typu string (to może być nazwa, opis)
    name = db.Column(db.String(1024))
    surname = db.Column(db.String(1024))
    pesel = db.Column(db.String(11))
    recordings = db.relationship("ECGRecording")


    # Konstruktor który służy do dodawania rzeczy do bazy danych
    def __init__(self, name, surname, pesel):
        self.name = name
        self.surname = surname
        self.pesel = pesel

    # Dzięki tej metodzie można wypisywać obiekty na konsolę jako string
    def __repr__(self):
        return '<ECGPacjent %s>' % self.name


        # Klasa ECGRecording, która dziedziczy po klasie Model
class ECGPlot(db.Model):
    __tablename__ = 'ecgplot'

    # Pola w klasie, czyli w tym przypadku kolumny w tabeli:

    # Kolumna typu integer - identyfikator danego przebiegu EKG -
    # klucz główny "primary key"
    id = db.Column(db.Integer, primary_key=True)

    # Kolumna typu string (to może być nazwa, opis)
    url = db.Column(db.String(1024))
    id_recording = db.Column(db.Integer, db.ForeignKey('ecgrecording.id'))



    # Konstruktor który służy do dodawania rzeczy do bazy danych
    def __init__(self, url):
        self.url = url


    # Dzięki tej metodzie można wypisywać obiekty na konsolę jako string
    def __repr__(self):
        return '<ECGPlot %s>' % self.url


