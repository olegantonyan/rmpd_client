
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
import time


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

    def is_appropriate_at(self, thetime):
        fit_time = lambda: self.begin_time <= thetime.time() <= self.end_time
        return fit_time()

input_items = [
    Item('9:00:00', '20:00:00', 11),
    Item('10:30:00', '20:00:00', 11),
    Item('12:00:00', '18:00:00', 16),
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

ranges = [ (value, resalls[index + 1]) for index, value in enumerate(resalls) if index + 1 != len(resalls) ]
rangest = [ (from_sec(i[0]), from_sec(i[1])) for i in ranges]

def rtos(i):
    s = str(i[0].hour) + ":" + str(i[0].minute) + ":" + str(i[0].second)
    f = str(i[1].hour) + ":" + str(i[1].minute) + ":" + str(i[1].second)
    return( s + " - " + f)

print("ranges")
for i in rangest:
    print(rtos(i))

ranges_with_items = []
for i in ranges:
    t = (i[0] + i[1]) / 2
    s = from_sec(t)
    key = rtos(to_sec( s ))
    print(key)
    #for j in input_items:
    #    if j.is_appropriate_at(s):
    #        ranges_with_items.append( (i, j) )
