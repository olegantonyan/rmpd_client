requirements:
	sudo pip3 install -r requirements.txt

binary:
	nuitka --recurse-all --remove-output main.py
	mv main.exe /tmp/__main.exe__
	mv /tmp/__main.exe__ ./rmpd
    
