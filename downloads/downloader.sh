for i in {2002..2006}
	do
	curl -o "plot${i}.dat" "https://physionet.org/physiobank/database/ltstdb/s${i}.dat"	
	done
