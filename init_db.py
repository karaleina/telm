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

recording1 = ECGRecording(name='Recording #2', timestamp=datetime(2015, 6, 12))
recording2 = ECGRecording(name='Recording #3', timestamp=datetime(2015, 6, 14))

path = "downloads/"
allFiles = os.listdir(path)

res = [k for k in allFiles if 'plot' in k]

for i in res:
	recording1.plots.append(ECGPlot(url=path + i))	
	
patient.recordings.append(recording1)
patient.recordings.append(recording2)

# Przykładowe wpisy do bazy danych
initial_recordings = [
	patient
]


# Pętla po nagraniach, która dodaje kolejne rekordy do sesji (transakcji)
#  i jak już wszystkie doda, to robi commit i dodaje do bazy danych
for recording in initial_recordings:
    db_in_app.session.add(recording)

db_in_app.session.commit()
