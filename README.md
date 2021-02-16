# jitsi-jicofo-roomlist
This program filters jicofo logs, typically produced by [jitsi-meet](https://jitsi.org/) and prints a list of existing conference rooms.

It's inspired by an idea of Joost Snellink and the great work of Markus B. Weber - please have a look into [his c-implentation](https://gist.github.com/marijani101/10a905848164af258cd651e8fe3d35de)

## Warning

Be warned: This piece of python-sh\*t-code is currently a prototpye, hacked in 3 hours.

## Pre-Check
You need python3 and this repository checked out on your jitsi-server.

### jitsi-watch-jicofolog.py

jitsi-watch-jicofolog.py is for reading your jicofo-logfile and watch the file for changes.

The original jicofo-log is reduced into a so called 'roomlog'

The file watches your log for changes and updates the roomlog instantly.

#### jitsi-get-roominfo.py

jitsi-get-roominfo.py is reading the file called 'roomlog' and display a basic statistic about the servers jitsi-rooms as a json-string.

On error, you get a error message.

You don't need a running "jitsi-watch-jicofolog.py". You only need the roomlog from this script.

Obviusly, if jitsi-watch-jicofolog.py is not running, you don't get any updated information...

## Using

1) Install python3

2) clone the repo anywhere on your server and cd into the project
```
git clone git@github.com:uroflavin/jitsi-jicofo-roomlist.git

cd jitsi-jicofo-roomlist

```

3) Start creating your roomlog by watching your jicofo.log
This skript is running forever, unless you stop it.

python3 jitsi-watch-jicofolog.py path/to/your/jicofo.log path/to/your/roomlog

e.g.: 

```
python3 jitsi-watch-jicofolog.py /var/log/jitsi/jicofo.log  /var/log/jitsi/jicofo.roomstat.log 

```

To keep jitsi-watch-jicofolog.py running in background, use [nohup or something similar](https://linuxize.com/post/how-to-run-linux-commands-in-background/)

e.g.: 

```
nohup python3 jitsi-watch-jicofolog.py /var/log/jitsi/jicofo.log /var/log/jitsi/jicofo.roomstat.log &
```

4) Whenever you want, take a look into your roomlog

python3 jitsi-get-roominfo.py path/to/your/roomlog

e.g.:
```
python3 jitsi-get-roominfo.py /var/log/jitsi/jicofo.roomstat.log 
```

5) To clean your roomlog, simply delete the roomlog-file, created by jitsi-watch-jicofolog.py

e.g.
```
rm /var/log/jitsi/jicofo.roomstat.log 
```

## A word about security

Do not expose the response from roominfo directly and public on any server, unless you know what you are doing.

There is no userdata exposed, but you get info about running sessions aka rooms.

## TODO

 * Improve Documentation
 * Improve Stability
 * Improve Usability
 * Translate Code-Comments to english


