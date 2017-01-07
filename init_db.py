# -*- coding: utf-8 -*-
# Ten skrypt tworzy bazę danych. Jest wywoływany tylko raz.
import os

# klasa reprezentująca datę wraz z godziną
from datetime import datetime

# "Gwiazdka" (*) importuje wszystko z danego pliku
# w tym przypadku wszystkie modele
from telm_webapp.database.models import *

# Obiekt bazy danych skonfigurowany przez aplikację
from telm_webapp.webapp import db_in_app


# Stworzenie tabel bazodanowych
db_in_app.create_all()

patient = ECGPatient(name='Magda', surname = 'Jaka', pesel = '93071612312')

recordings_directory = "downloads/"
allFiles = os.listdir(recordings_directory)

recording_paths = [k for k in allFiles if '.dat' in k]

for recording_path in recording_paths:
    recording = ECGRecording(
        name=recording_path,
        timestamp=datetime(2015, 6, 12),
        url=os.path.join(recordings_directory, recording_path),
        plot_count=2)
    patient.recordings.append(recording)


# Pętla po nagraniach, która dodaje kolejne rekordy do sesji (transakcji)
#  i jak już wszystkie doda, to robi commit i dodaje do bazy danych
db_in_app.session.add(patient)
db_in_app.session.commit()
