
import utils.config as co
co.Config('/home/oleg/projects/rmpd_client/rmpd.conf')
import mediaplayer.player.guard as gu
g = gu.Guard()
g.execute('play', filename='/mnt/storage/music/01_nto_trauma_worakls_remix_myzuka.ru.mp3')

import time

while True:
    time.sleep(1)
