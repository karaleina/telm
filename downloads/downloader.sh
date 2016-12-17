#!/bin/sh

# uncomment below line for full download 
#for i in `seq 20011 10 30801`

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
