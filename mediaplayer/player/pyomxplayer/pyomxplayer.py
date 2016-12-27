# -*- coding: utf-8 -*-

from pexpect import spawn, TIMEOUT, EOF
from re import compile
from threading import Thread
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from os import getcwd, path


class OMXPlayer(object):
    exec_path = "omxplayer"
    args = "-o both"

    def __init__(self):
        self._paused = False
        self._subtitles_visible = True
        self._position = 0.0
        self._filename = None
        self._fileinfo = None
        self._fileinfo_parsed = {}
        self._process = None
        self._position_thread = None

    def play(self, mediafile, start_pos=0, *_):
        if not self.isstopped():
            self.stop()
        self._fileinfo = self._get_fileinfo(mediafile)
        # New omxplayer builds will need this flag to report status
        arg = "{a} --pos {p}".format(p=self._seconds_to_hhmmss(start_pos), a=self.args)
        cmd = "{ep} -s {a} {f}".format(ep=self.exec_path, a=arg, f=mediafile)
        self._process = spawn(cmd)
        self._position_thread = Thread(target=self._get_position)
        self._position_thread.start()
        self._filename = mediafile
        while not self._process.isalive():
            sleep(0.05)

    def __del__(self):
        self.stop()

    def quit(self):
        self.stop()

    def isstopped(self):
        for i in range(5):
            try:
                return not self._process or not self._process.isalive()
            except OSError:
                #  sometimes it throws: isalive() encountered condition where "terminated" is 0,
                #  but there was no child process. Did someone else call waitpid() on our process?
                pass

    def pause(self):
        if not self._process:
            return
        if self._process.send('p'):
            self._paused = not self._paused

    def toggle_subtitles(self):
        if not self._process:
            return
        if self._process.send('s'):
            self._subtitles_visible = not self._subtitles_visible

    def stop(self):
        self._filename = None
        self._fileinfo = None
        self._fileinfo_parsed = {}
        self._position = 0.0
        if not self._process:
            return
        self._process.send('q')
        self._process.terminate(force=True)

    def time_pos(self):
        if not self._process:
            return 0.0
        return self._position

    def percent_pos(self):
        try:
            return int(self._position / self.length() * 100)
        except:
            return 0

    def filename(self):
        if not self._process or not self._filename:
            return None
        return path.basename(str(self._filename))

    def length(self):
        if not self._process:
            return 0.0
        self._fileinfo_parsed["duration"] = self._parse_duration(self._fileinfo)
        return self._fileinfo_parsed.get("duration", None)

    def _get_fileinfo(self, filename):
        (r, o) = self._execute_shell("{ep} -i {f}".format(ep=self.exec_path, f=filename))
        return o

    def _parse_duration(self, fileinfo):
        duration_rexp = compile(r"((.|\n)*)(Duration:) (\d+:\d+:\d+.\d+)")
        m = duration_rexp.match(fileinfo)
        p = m.group(4).split(":")
        return float(p[0]) * 3600 + float(p[1]) * 60 + float(p[2])

    def _get_position(self):
        status_rexp = compile(b"M:\s*([\d.]+)\s*V:.*")
        done_rexp = compile(b"have a nice day.*")
        fileprop_rexp = compile(b".*audio streams (\d+) video streams (\d+) chapters (\d+) subtitles (\d+).*")
        videoprop_rexp = compile(b".*Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+).*")
        audioprop_rexp = compile(b"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
        while self._process.isalive():
            try:
                index = self._process.expect(pattern=[status_rexp, done_rexp, fileprop_rexp, videoprop_rexp, audioprop_rexp], timeout=5)
                if index == 1:
                    self.stop()
                    break
                elif index == 0:
                    self._position = float(self._process.match.group(1)) / 1000000
            except EOF:  # OMX hanged
                self.stop()
                break
            except TIMEOUT:  # OMX hanged
                self.stop()
                break

            sleep(0.15)

    def _execute_shell(self, cli):
        # don't what to have any dependencies on main project
        popen_cli = filter(lambda x: True if len(x) > 0 else False, cli.split(" "))
        process = Popen(popen_cli, stdout=PIPE, stderr=STDOUT, cwd=getcwd())
        out, err = process.communicate()
        return process.returncode, out.decode('utf-8')

    def _seconds_to_hhmmss(self, secs):
        secs = int(secs)
        h = int(secs / 3600)
        rem = (secs % 3600)
        m = int(rem / 60)
        s = int(rem % 60)
        return "{hours:02d}:{minutes:02d}:{seconds:02d}".format(hours=h, minutes=m, seconds=s)
