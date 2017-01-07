# -*- coding: utf-8 -*-
# Ten skrypt tworzy bazę danych. Jest wywoływany tylko raz.
import os

# "Gwiazdka" (*) importuje wszystko z danego pliku
# w tym przypadku wszystkie modele
from telm_webapp.database.models import *

# Obiekt bazy danych skonfigurowany przez aplikację
from telm_webapp.parsers.header_parser import HeaderParser
from telm_webapp.webapp import db_in_app


# Stworzenie tabel bazodanowych
db_in_app.create_all()

patient = ECGPatient(name='Magda', surname='Jaka', pesel='93071612312')

recordings_directory = "downloads/"
data_files = os.listdir(recordings_directory)

header_paths = [
    os.path.join(recordings_directory, data_file_path)
    for data_file_path in data_files
    if '.hea' in data_file_path]

header_parser = HeaderParser()

for header_path in header_paths:
    patient.recordings.append(header_parser.parse_header(header_path))


# Pętla po nagraniach, która dodaje kolejne rekordy do sesji (transakcji)
#  i jak już wszystkie doda, to robi commit i dodaje do bazy danych
db_in_app.session.add(patient)
db_in_app.session.commit()
