# -*- coding: utf-8 -*-

# Obiekt bazy danych skonfigurowany przez aplikację
from telm_webapp.webapp import db_in_app
from telm_webapp.database.models import *

# klasa reprezentująca datę wraz z godziną
from datetime import datetime

def searchInDb( pesel, recordingDate ):

	recordings = ECGRecording.query
	if isinstance(pesel, basestring):
		recordings.join(ECGRecording.patient).filter(ECGPatient.pesel.like('%' + pesel + '%'))
	if isinstance(recordingDate, datetime):
		recordings.filter(ECGRecording.timestamp == recordingDate)
# 		print("byDate")
		
# 	print(type(recordingDate))	
	print(recordings)
	for r in recordings:
		print(r.name)
	return
	
	
# przykład użycia
searchInDb("1", datetime(2015, 6, 12))