
import utils.config as co
co.Config('/home/oleg/projects/rmpd_client/rmpd.conf')
import mediaplayer.player.guard as gu
import mediaplayer.player.watcher as watcher
w = watcher.Watcher()
w.play('/mnt/storage/music/(OST) Silent Hill film/Silent_Hill_-_(2006)_Complete_Score_CD1_OST/01 - Jeff Danna & Akira Yamaoka - Silent Hill.mp3')

import mediaplayer.playlist.scheduler as pw
pw.Watcher()

import time
while True:
    time.sleep(1)
    print(w._expected_state)
