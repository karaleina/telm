# -*- coding: utf-8 -*-
# Ten skrypt tworzy bazę danych. Jest wywoływany tylko raz.

# klasa reprezentująca datę wraz z godziną
from datetime import datetime

# "Gwiazdka" (*) importuje wszystko z danego pliku
# w tym przypadku wszystkie modele
from telm_webapp.database.models import *

# Obiekt bazy danych skonfigurowany przez aplikację
from telm_webapp.webapp import db_in_app


# Stworzenie tabel bazodanowych
db_in_app.create_all()

# Przykładowe wpisy do bazy danych
initial_recordings = [
    ECGRecording(name='Recording #1', timestamp=datetime(2013, 5, 24)),
    ECGRecording(name='Recording #2', timestamp=datetime(2015, 6, 12))
]

# Pętla po nagraniach, która dodaje kolejne rekordy do sesji (transakcji)
#  i jak już wszystkie doda, to robi commit i dodaje do bazy danych
for recording in initial_recordings:
    db_in_app.session.add(recording)

db_in_app.session.commit()
