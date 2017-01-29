# -*- coding: utf-8 -*-
# skrypt pobiera pliki binarne .dat z wykresami i pliki informacyjne .hea
# uruchamiamy: python downloader.py
import urllib
import urllib2


recording_names = urllib2.urlopen("https://www.physionet.org/physiobank/database/ltstdb/RECORDS").read().split()

for recording_name in recording_names[0:6]:
    # Wspierane pliki z 2 odprowadzeniami
    if recording_name.startswith("s2"):
        header_file = recording_name + ".hea"
        data_file = recording_name + ".dat"
        urllib.urlretrieve(
            "https://physionet.org/physiobank/database/ltstdb/{}.hea".format(recording_name),
           header_file)
        urllib.urlretrieve(
             "https://physionet.org/physiobank/database/ltstdb/{}.dat".format(recording_name),
             data_file)
