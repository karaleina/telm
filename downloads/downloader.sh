#!/bin/sh

# skrypt pobiera pliki binarne .dat z wykresami.
# pliki mają nazwy od 20011 do 20651 więc skrypt pobiera pliki 20011, 20021, 20031, itd
# aktualnie jest ustawiony na pobieranie 2 plików co można zmienić.
# uruchamiamy: ./downloader.sh

# uncomment below line for full download 
#for i in `seq 20011 10 20651`

for i in `seq 20011 10 20021`
	do	
	case "$(uname -s)" in

   Darwin)
	curl -o "plot${i}.dat" "https://physionet.org/physiobank/database/ltstdb/s${i}.dat"	
     ;;

   Linux)
     wget "https://physionet.org/physiobank/database/ltstdb/s${i}.dat"
     ;;

   CYGWIN*|MINGW32*|MSYS*)
     echo 'You are running MS Windows - download files manually'
     ;;
	esac
	done
