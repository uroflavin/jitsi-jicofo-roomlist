#!/usr/bin/python3
# Wertet auf Anforderung die Aufbereitete jicofo-Raumliste aus und gibt sie als JSON-Object zurück
import sys 
import json

def get_current_room_info(file):
    room = {
            "date" : "",
            "time" : "",
            "date_time" : "",
            "room" : "",
            "user" : "SYSTEM",
            "action" : "unknown"
        } 
    
    rooms =  {}
    
    with open(file, 'r') as logfile:
        while True:
            # Get next line from file
            line = logfile.readline()
            # if line is empty
            # end of file is reached
            if not line:
                break
            
            line_split = line.split("\t")
            total_rooms = 0
            total_users = 0
            
            if len(line_split) == 5:
                
                room["room"] = line_split[2].strip()
                room["action"] = line_split[4].strip()

                if room["action"] == "room created":
                    rooms[room["room"]] = 0                    
                    total_rooms += 1
                elif room["action"] == "room delete":
                    total_rooms -= 1
                    if room["room"] in rooms:
                        del rooms[room["room"]]
                elif room["action"] == "user joined":
                    if room["room"] in rooms:
                        rooms[room["room"]] += 1
                        total_users += 1
                elif room["action"] == "user leaving":
                    if room["room"] in rooms:
                        rooms[room["room"]] -= 1
                        total_users -= 1
    return {"rooms" : rooms,
             "user_count" : total_users,
             "room_count" : total_rooms,
             "message" : "ok"}

try:
    # 1. Argument ist die Eingangsdatei
    room_log = sys.argv[1]
    # Aufbereiten
    room_info = get_current_room_info(room_log)
    # Ausgeben
    print(json.dumps(room_info))
except:
    print("{\"error\" : ‘Error'}")