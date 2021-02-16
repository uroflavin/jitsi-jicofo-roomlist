#!/usr/bin/python3
# Wertet auf Anforderung die Aufbereitete jicofo-Raumliste aus und gibt sie als JSON-Object zurück

import time
import os
import sys


# Datei auf Änderungen überwachen und Zeilen zurückgeben
def follow(thelogfile):
	try:
	    '''generator function that yields new lines in a file
	    '''
	    # seek the end of the file
	    thelogfile.seek(0, os.SEEK_END)
	   
	    # start infinite loop
	    while True:
	       # read last line of file
	        line = thelogfile.readline()
	        # sleep if file hasn't been updated
	        if not line:
	            time.sleep(0.1)
	            continue

	        yield line
	except:
		return
	finally:
		pass

# Extrahiert die Rauminformationen aus einer Log-Zeile als Dictionary und liefert die Zeile zurück
def get_room_entry_from_line(line):
    room_entry = {
            "date" : "",
            "time" : "",
            "date_time" : "",
            "room" : "",
            "user" : "SYSTEM",
            "action" : "unknown"
        }

    line_array = line.split(" ")

    if "INFO: " in line:
        date_time = line_array[1] + " " + line_array[2]
        room_entry["date"] = line_array[1]
        room_entry["time"] = line_array[2]
        room_entry["date_time"] = line_array[1] + " " + line_array[2]

        # a room has been entered or left by a user
        if "org.jitsi.jicofo.JitsiMeetConferenceImpl.log() Member " in line:
            # action ist ganz am ende das letzte wort
            room_entry["action"] = "user " + line_array[-1].strip().replace(".","")
            # room steht direct nach dem log() Member 
            room_user_info = line_array[7].strip()
            room_entry["room"] = room_user_info.split("@")[0]
            # user steht nach /im raum
            room_entry["user"] = room_user_info.split("@")[1].split("/")[1]
        # a room has been deleted
        elif "org.jitsi.jicofo.FocusManager.log() Disposed conference for room:" in line:
            room_entry["action"] = "room delete"
            room_entry["room"] = line_array[10].strip().split("@")[0].strip()
        # a room has been created by a user
        # detection is possible by 
        #   1) 'org.jitsi.jicofo.JitsiMeetConferenceImpl.log() Joining the room: '
        #       Room is in the last part
        # or
        #   2) 'org.jitsi.jicofo.FocusManager.log() Created new focus for '
        #       Room is somewhere in the middle of the string
        # or
        #   3) 'org.jitsi.jicofo.auth.AbstractAuthAuthority.log() Authenticated jid:'
        #
        elif "org.jitsi.jicofo.FocusManager.log() Created new focus for " in line:
            # we have to add our own action-name
            room_entry["action"] = "room created"
            # Room is the 10. element 
            room_entry["room"] = line_array[10].strip().split("@")[0].strip()
    
    return room_entry

# Initiales Einlesen der Logdatei, die Datei muss offen sein!
def read_init(thelogfile):
    
    room_log = []
    
    while True:
        # Get next line from file
        line = thelogfile.readline()

        # if line is empty
        # end of file is reached
        if not line:
            break
        
        room_entry = get_room_entry_from_line(line)
        
        if room_entry["action"] != "unknown" and room_entry["action"] != "":
            # Fallunterscheidung bei Raum anlegen, da es doppelte Meldungen gibt
            if room_entry["action"] == "room created":
                # das vermeidet doppelte Meldungen zum Anlegen von Räumen
                # Funktioniert nur, wenn die Authentification auch auf guest.jitsi-example-host.com liegt
                # wird aber in der Regel in der Dokumentation so vorgeschlagen...
                if "@guest." not in line:
                    room_log.append(room_entry)
            # Alle Meldungen außer "room created"
            else:
                room_log.append(room_entry)
                
    return room_log

def append_roomentry_to_file(file,item):
    with open(file, 'a') as logfile:
        logfile.write(item["date"] + "\t" + item["time"] + "\t" + item["room"] + "\t" + item["user"] + "\t" + item["action"] +"\n")


if __name__ == '__main__':
    
    # 1. Argument ist die Eingangsdatei
    logfile_path = sys.argv[1]
    # 2. Argument ist die Ausgabedatei (Raumlog)
    roomlog_path = sys.argv[2]
    logfile = open(logfile_path,"r")
    # Startup info
    print("jitsi-watch-jicofolog is running...")
    # Initialisieren
    room_log = read_init(logfile)

    for item in room_log:
        append_roomentry_to_file(roomlog_path, item)
        print(item["date"] + "\t" + item["time"] + "\t" + item["room"] + "\t" + item["user"] + "\t" + item["action"] )
    
    loglines = follow(logfile)
    # iterate over the generator
    for line in loglines:
        room_entry = get_room_entry_from_line(line)
        
        if room_entry["action"] != "unknown" and room_entry["action"] != "":
            # Fallunterscheidung bei Raum anlegen, da es doppelte Meldungen gibt
            if room_entry["action"] == "room created":
                # das vermeidet doppelte Meldungen zum Anlegen von Räumen
                # Funktioniert nur, wenn die Authentification auch auf guest.jitsi-example-host.com liegt
                # wird aber in der Regel in der Dokumentation so vorgeschlagen...
                if "@guest." not in line:
                    room_log.append(room_entry)
            # Alle Meldungen außer "room created"
            else:
                room_log.append(room_entry)
            
            append_roomentry_to_file(roomlog_path, room_entry)
            print(room_entry["date"] + "\t" + room_entry["time"] + "\t" + room_entry["room"] + "\t" + room_entry["user"] + "\t" + room_entry["action"] )
    