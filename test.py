
#import utils.config as co
#co.Config('/home/oleg/projects/rmpd_client/rmpd.conf')
#import mediaplayer.player.guard as gu
#import mediaplayer.player.watcher as watcher
#w = watcher.Watcher()
#w.play('/mnt/storage/music/(OST) Silent Hill film/Silent_Hill_-_(2006)_Complete_Score_CD1_OST/01 - Jeff Danna & Akira Yamaoka - Silent Hill.mp3')

#import mediaplayer.playlist.scheduler as pw
#pw.Watcher()

#import time
#while True:
#    time.sleep(1)
#    print(w._expected_state)

import datetime


class Item(object):
    def __init__(self, b, e, c):
        self._b = datetime.datetime.strptime(b, '%H:%M:%S').time()
        self._e = datetime.datetime.strptime(e, '%H:%M:%S').time()
        self._c = c

    @property
    def begin_time(self):
        return self._b

    @property
    def end_time(self):
        return self._e

    @property
    def playbacks_count(self):
        return self._c

input_items = [
    Item('9:42:01', '20:00:00', 11),
    Item('9:42:03', '20:15:43', 11),
    Item('10:00:00', '18:00:00', 16),
    Item('10:12:00', '18:18:00', 16),
    Item('11:03:03', '14:00:03', 4),
]

def to_sec(tm):
    return tm.hour * 3600 + tm.minute * 60 + tm.second

def from_sec(secs):
    h = int(secs / 3600)
    rem = (secs % 3600)
    m = int(rem / 60)
    s = int(rem % 60)
    return datetime.time(hour=h, minute=m, second=s)


res = [(to_sec(i.begin_time), to_sec(i.end_time)) for i in input_items]

resall = [to_sec(i.begin_time) for i in input_items] + [to_sec(i.end_time) for i in input_items]
resalls = sorted(list(set(resall)))
print(resalls)
print("min:")
print(from_sec(resalls[0]))
print("max:")
print(from_sec(resalls[-1]))

